"""
The Schema Class is logically tied to the price transparency guide schemas
It is intended to provide a standard class that will contain
all table stream target tables and analytic tables

It will also
"""

from .pt_table import Pt_table
from .pt_analytic_table import AnalyticTable
from .pt_ingest_table import IngestTable

from pyspark.sql.session import SparkSession
from subprocess import Popen, PIPE
from pyspark.sql import DataFrame
from typing import Callable
from pandas import DataFrame as Pdf
from datetime import date

import time

class Pt_schema:

    _spark: SparkSession
    _mth: int
    _catalog_name: str
    _stage_db_name: str
    ingest_tables: {str: IngestTable}
    analytic_tables: {str: AnalyticTable}

    def __init__(self, mth: int = None, catalog_name='hive_metastore', stage_db_name='pt_stage'):
        self._spark = SparkSession.builder.getOrCreate()
        self._mth = mth if mth is not None else int(date.today().strftime('%Y%m'))
        self._catalog_name = catalog_name
        self._stage_db_name = stage_db_name
        self._set_tables()

    @property
    def schema(self):
        return self.__class__.__name__.lower().replace('_', '-')

    @property
    def catalog_name(self):
        return self._catalog_name

    @property
    def stage_db_name(self):
        return self._stage_db_name

    @property
    def mth(self):
        return self._mth

    @mth.setter
    def mth(self, value):
        mth = int(value)
        self._mth = mth
        print(f'schema set to {mth}.')

    @mth.deleter
    def mth(self):
        mth = int(date.today().strftime('%Y%m'))
        self._mth = mth
        print(f'schema reset to {mth}')

    def _set_tables(self):
        """
        Method is intended to be overwritten for each specific pt_schema subclass
        :return: None
        """
        self.analytic_tables = {}
        self.ingest_tables = {}
        return None

    def get_tables(self) -> [Pt_table]:
        return list(self.ingest_tables.values()) + list(self.analytic_tables.values())

    def create_tables(self):
        # TODO: parallelize table create
        for t in self.get_tables():
            t.create_table()

    def drop_tables(self):
        # TODO: parallelize drop table
        for t in self.get_tables():
            t.drop_table()

    def create_views(self) -> None:
        # TODO: parallelize create views
        for t in self.get_tables():
            t.create_view()

    def purge_tables(self) -> None:
        # TODO: parallelize purge tables
        for t in self.get_tables():
            t.purge_table()

    def get_insertIntoIngestTables(self):
        batch_merge_functions: [Callable] = [t.get_batch_merge_function() for t in list(self.ingest_tables.values())]

        def insertIntoIngestTables(microBatchOutputDF, batchId):
            # This approach feels expensive, will need to compare vs persist & filter
            microBatchOutputDF.persist()
            for batch_merge in batch_merge_functions:
                batch_merge(microBatchOutputDF, batchId)
            microBatchOutputDF.unpersist()
        return insertIntoIngestTables

    def file_ingest_query(self, file_path: str):
        # TODO: make queryName include payer description from file name
        # TODO: derive checkpoint location from raw file location
        source_cp = 'dbfs:/tmp/pt/_checkpoint'
        process = Popen('rm -rf /dbfs/tmp/pt/_checkpoint', shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        if stdout != stderr:
            print(stderr)
        return self._spark.readStream.option("buffersize", 67108864).format("payer-mrf") \
                   .option("payloadAsArray", "true").load(file_path) \
                   .writeStream.queryName(f"{self.schema}_ingest") \
                   .option("checkpointLocation", source_cp) \
                   .foreachBatch(self.get_insertIntoIngestTables()).start()

    def run_ingest_file(self, file_path: str):
        # Method for single file ingest stop stream on complete
        def stop_on_file_complete(query, wait_time=10):
            while query.isActive:
                msg, is_data_available, is_trigger_active = query.status.values()
                if not is_data_available and not is_trigger_active and msg != "Initializing sources":
                    query.stop()
                time.sleep(5)
            query.awaitTermination(wait_time)
        stop_on_file_complete(self.file_ingest_query(file_path), wait_time=10)

    def run_ingest_files(self, file_paths: [str]):
        for file_path in file_paths:
            self.run_ingest_file(file_path=file_path)

    def run_ingest_pdf(self, file_path_pdf: Pdf):
        file_col = 'file_path' if 'file_path' in file_path_pdf.columns else file_path_pdf.columns[0]
        file_paths = file_path_pdf[file_col].values.tolist()
        self.run_ingest_files(file_paths=file_paths)

    def run_ingest_df(self, file_path_df: DataFrame):
        file_col = 'file_path' if 'file_path' in file_path_df.columns else file_path_df.columns[0]
        file_paths = [str(row[0]) for row in file_path_df.select(file_col).collect()]
        self.run_ingest_files(file_paths=file_paths)

    def run_analytic_file(self, file_name: str):
        self.run_analytic_files(file_names=[file_name, ])

    def run_analytic_files(self, file_names: [str]):
        self.run_analytic_df(self._spark.createDataFrame(data=[(f,) for f in file_names], schema=['file_name', ]))

    def run_analytic_pdf(self, file_name_pdf: Pdf):
        file_col = 'file_name' if 'file_name' in file_name_pdf.columns else file_name_pdf.columns[0]
        self.run_analytic_df(self._spark.createDataFrame(file_name_pdf[[file_col]]))

    def run_analytic_df(self, file_name_df: DataFrame):
        # This method must be overwritten in the schema subclass
        pass
