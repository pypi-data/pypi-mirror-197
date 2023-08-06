from ..pt_files import Pt_files
from pyspark.sql import DataFrame
from ..pt_functions import col, lit
from pandas import DataFrame as Pdf
import pandas as pd

class Provider_reference(Pt_files):

    _meta_ingest_tbl = "pt_stage.in_pr_loc"

    def run_import(self):
        loc_files = self._spark.table('pt_stage.in_pr_loc').filter(col('mth') == lit(self.mth)) \
            .select(col('location').alias('url'), col('tgt_file_name')).alias('loc') \
            .join(self.files.select(col('file_name').alias('tgt_file_name')), 'tgt_file_name', 'left_anti').collect()
        for r in loc_files:
            self.run_import_url(r.url, r.tgt_file_name)

    def run_import_df(self, url_df: DataFrame):
        if 'url' in url_df.columns:
            pass
        elif 'location' in url_df.columns:
            url_df = url_df.withColumnRenamed('location', 'url')
        else:
            url_df = url_df.withColumnRenamed(url_df.columns[0], 'url')
        loc_files = self._spark.table('pt_stage.in_pr_loc').filter(col('mth') == lit(self.mth)).alias('loc') \
            .join(url_df.alias('url'), col('url.url') == col('loc.location'), 'inner') \
            .select('url', 'url.tgt_file_name').collect()
        for r in loc_files:
            self.run_import_url(r.url, r.tgt_file_name)

    def run_import_pdf(self, url_pdf: Pdf):
        if 'url' in url_pdf.columns:
            pass
        elif 'location' in url_pdf.columns:
            url_pdf.rename(columns={"location": "url"})
        else:
            url_pdf.rename(columns={url_pdf.columns[0]: "url"})
        self.run_import_df(self._spark.createDataFrame(url_pdf[['url', ]]))

    def run_import_urls(self, urls: [str]):
        self.run_import_pdf(pd.DataFrame(urls, columns=['url', ]))
