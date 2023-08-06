"""
Base files class which includes all run import methods and meta definitions
"""

from pyspark.sql.session import SparkSession
from datetime import date
from pyspark.sql.functions import col, lit
from pyspark.sql import functions as F
from pyspark.sql import DataFrame
import subprocess
from os.path import exists as path_exists
from os.path import isfile as file_exists
from subprocess import check_output
import re
from pandas import DataFrame as Pdf


def get_file_meta(file):
    """
    File parsing taken from https://github.com/CMSgov/price-transparency-guide#file-naming-convention
    """
    file_regex = r"((\d{4}-\d{2}(?:-\d{2})?)\_(.*)\_" + \
                 r"(in-network-rates|allowed-amounts|prescription-drugs|provider-reference|index)" + \
                 r"\_?([^\.]*))\.([^(?:\?|$)]*)(?:\??[^$]*)"
    file_name, dte, payer_plan, schema, index, ext = re.search(file_regex, file).groups()
    if schema == 'index':
        schema = 'table-of-contents'
    mth = int(dte[:4] + dte[5:7])
    indexed = index != ''
    return {'name': file_name, 'dte': dte, 'mth': mth, 'ext': ext,
            'indexed': indexed, 'index': int(index.split('_')[-1]) if indexed else 0,
            'schema': schema, 'payer_plan': payer_plan}

def sh(args):
    return str(check_output(args)).split('\\n')

class Pt_files:

    _spark: SparkSession
    _mth: int
    _meta_ingest_tbl: str
    _catalog_name: str
    _raw_db_name: str

    def __init__(self, mth: int = None, catalog_name='hive_metastore', raw_db_name='pt_raw'):
        self._spark = SparkSession.builder.getOrCreate()
        self._mth = int(date.today().strftime('%Y%m')) if mth is None else mth
        self._catalog_name = catalog_name
        self._raw_db_name = raw_db_name

    @property
    def schema(self):
        return self.__class__.__name__.lower().replace('_', '-')

    @property
    def mth(self):
        return self._mth

    @mth.setter
    def mth(self, value):
        mth = int(value)
        self._mth = mth
        print(f'pt_raw.{self.schema.replace("-","_")}.mth set to {mth}.')

    @mth.deleter
    def mth(self):
        mth = int(date.today().strftime('%Y%m'))
        self._mth = mth
        print(f'pt_raw.{self.schema.replace("-","_")}.mth reset to {mth}')

    @property
    def catalog_name(self):
        return self._catalog_name

    @property
    def raw_db_name(self):
        return self._raw_db_name

    @property
    def path(self) -> str:
        return f'/dbfs/user/hive/warehouse/pt_raw.db/_raw/mth={self.mth}/schema={self.schema}/'

    @property
    def dbfs_path(self) -> str:
        return f'dbfs:/user/hive/warehouse/pt_raw.db/_raw/mth={self.mth}/schema={self.schema}/'

    @property
    def files(self) -> DataFrame:
        """
        Files will be real time definition of files in the raw directory.
        This is intended to help with the state of ingest.
        """
        return self._spark.read.format("binaryFile") \
                   .option("pathGlobFilter", "*.json") \
                   .load(self.dbfs_path) \
                   .drop('content') \
                   .select(lit(self.mth).alias("mth"),
                           lit(self.schema).alias("schema"),
                           F.element_at(F.split(col('path'), '/'), -1).alias('file_name'),
                           col('path').alias('file_path'),
                           col('length'),
                           col('modificationTime')).alias('files')

    @property
    def meta(self) -> DataFrame:
        """
        meta delta tables will be
        """
        # TODO: write condition for inr_header existing
        #  spark.catalog.tableExists("non_existing_table")
        return self.files \
                   .join(self._spark.table(self._meta_ingest_tbl).groupBy(col('file_name'))
                             .agg(F.first(col('reporting_entity_name'),
                                          ignorenulls=True).alias('reporting_entity_name')).alias('header'),
                         "file_name", "left") \
                   .select(col('files.*'),
                           F.when(col('header.file_name').isNotNull(),
                                  lit(True)).otherwise(lit(False)).alias('ingested'),
                           col('reporting_entity_name'))

    def run_import_url(self, url: str, tgt_file_name: str = None):
        # file_meta = get_file_meta(url.split('/')[-1])
        file_parts = url.split('?')[0].split('/')[-1].split('.')
        name = file_parts[0]
        ext = '.'.join(file_parts[1:])
        if tgt_file_name:
            tgt = self.path + tgt_file_name
        else:
            tgt = self.path + name + '.json'
        if not path_exists(self.path):
            sh(['mkdir', '-p', self.path])
        if file_exists(tgt):
            print(tgt + ' already exists.')
            return
        if ext == 'json.gz':
            with open(tgt, "w") as f:
                wget_process = subprocess.Popen(('wget', '-O', '-', '-o', '/dev/null', url), stdout=subprocess.PIPE)
                subprocess.call(('gunzip', '-c'), stdin=wget_process.stdout, stdout=f)
                wget_process.wait()
        elif ext == 'zip':
            zip_tgt = self.path + '/' + name + '.zip'
            wget_process = subprocess.Popen(('wget', '-O', zip_tgt, url))
            wget_process.wait()
            unzip_process = subprocess.Popen(('unzip', zip_tgt))
            unzip_process.wait()
            rm_process = subprocess.Popen(('rm', '-rf', zip_tgt))
            rm_process.wait()
        else:
            wget_process = subprocess.Popen(('wget', '-O', tgt, url))
            wget_process.wait()
        return

    def run_import_urls(self, urls: [str]):
        for url in urls:
            self.run_import_url(url=url)

    def run_import_pdf(self, url_pdf: Pdf):
        url_col = 'url' if 'url' in url_pdf.columns else url_pdf.columns[0]
        urls = url_pdf[url_col].values.tolist()
        self.run_import_urls(urls=urls)

    def run_import_df(self, url_df: DataFrame):
        self._spark.sparkContext.setLocalProperty("callSite.short", f"{self.schema}_import")
        url_col = 'url' if 'url' in url_df.columns else url_df.columns[0]
        urls = [str(row[0]) for row in url_df.select(url_col).collect()]
        self.run_import_urls(urls=urls)
