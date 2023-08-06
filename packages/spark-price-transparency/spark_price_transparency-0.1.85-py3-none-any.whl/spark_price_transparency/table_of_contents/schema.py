"""
This is the schema class for in table of contents
"""

from ..pt_schema import Pt_schema
from .toc_header import Toc_header
from .toc_reporting import Toc_reporting
from .index_reports import Index_reports
from pyspark.sql.functions import col, lit
from pyspark.sql import functions as F
from pyspark.sql import DataFrame


class Table_of_contents(Pt_schema):

    def _set_tables(self):
        self.ingest_tables = {'toc_header': Toc_header(self.mth, self.catalog_name, self.stage_db_name),
                              'toc_reporting': Toc_reporting(self.mth, self.catalog_name, self.stage_db_name)}
        self.analytic_tables = {'index_reports': Index_reports(self.mth, self.catalog_name, self.stage_db_name)}

    @property
    def toc_header(self) -> DataFrame:
        return self.ingest_tables['toc_header'].df

    @property
    def toc_reporting(self) -> DataFrame:
        return self.ingest_tables['toc_reporting'].df

    @property
    def index_reports(self) -> DataFrame:
        return self.ingest_tables['index_reports'].df

    def run_ingest(self):
        dbfs_path = f'dbfs:/user/hive/warehouse/pt_raw.db/_raw/mth={self._mth}/schema={self.schema}/'
        file_df = self._spark.read.format("binaryFile") \
                      .option("pathGlobFilter", "*.json") \
                      .load(dbfs_path).select(col('path').alias('file_path'),
                                              F.element_at(F.split(col('path'), '/'), -1).alias('file_name')) \
                      .join(self._spark.table("pt_stage.toc_header"), "file_name", "left_anti")
        self.run_ingest_df(file_df)

    def run_analytic(self):
        file_name_df = self.ingest_tables['toc_header'].df.select('file_name') \
            .join(self.analytic_tables['index_reports'].df.select(col('file_name')),
                  "file_name", "left_anti").distinct()
        self.run_analytic_df(file_name_df)

    def run_analytic_df(self, file_name_df: DataFrame):
        self._spark.sparkContext.setLocalProperty("callSite.short", f"{self.schema}_analytic")
        header = self.ingest_tables['toc_header'].df \
            .join(file_name_df, "file_name", "left_semi") \
            .groupBy(lit(self.mth).alias('mth'),
                     col('file_name')) \
            .agg(F.first(col('reporting_entity_name'), ignorenulls=True).alias('reporting_entity_name'),
                 F.first(col('reporting_entity_type'), ignorenulls=True).alias('reporting_entity_type')) \
            .alias('header')

        reporting = self.ingest_tables["toc_reporting"].df \
            .withColumn('file_type', F.explode(F.array(lit('in-network-rates'), lit('allowed-amounts')))) \
            .withColumn('file_detail',
                        F.explode(F.when(col('file_type') == lit('in-network-rates'), col('in_network_files'))
                                  .otherwise(F.array(col('allowed_amount_file'))))) \
            .select(col('file_name'),
                    col('file_type'),
                    col('file_detail.location').alias('location'),
                    col('reporting_plans')) \
            .alias('reporting')

        index_reports = F.broadcast(header).join(reporting, 'file_name', 'left')
        self.analytic_tables['index_reports'].run_analytic_merge(index_reports)
