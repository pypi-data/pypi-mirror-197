"""
This is the schema class for in provider reference
"""

from ..pt_schema import Pt_schema
from .pr_provider import Pr_provider
from .in_provider import In_provider
from .in_rate import In_rate
from pyspark.sql import DataFrame
from ..pt_types import provider_groups_schema
from ..pt_functions import F, col, lit


class Provider_reference(Pt_schema):

    def _set_tables(self):
        self.ingest_tables = {'pr_provider': Pr_provider(self.mth, self.catalog_name, self.stage_db_name)}
        self.analytic_tables = {'in_provider': In_provider(self.mth, self.catalog_name, self.stage_db_name),
                                'in_rate': In_rate(self.mth, self.catalog_name, self.stage_db_name)}

    @property
    def pr_provider(self) -> DataFrame:
        return self.ingest_tables['pr_provider'].df

    @property
    def in_provider(self) -> DataFrame:
        return self.ingest_tables['in_provider'].df

    @property
    def in_rate(self) -> DataFrame:
        return self.ingest_tables['in_rate'].df

    def run_ingest(self):
        dbfs_path = f'dbfs:/user/hive/warehouse/pt_raw.db/_raw/mth={self._mth}/schema={self.schema}/'
        file_path_df = self._spark.read.json(dbfs_path, provider_groups_schema) \
            .withColumn('file_path', F.input_file_name()) \
            .withColumn('file_name', F.element_at(F.split(F.input_file_name(), '/'), -1)) \
            .join(self._spark.table('pt_stage.in_pr_loc').filter(col('mth') == lit(self.mth))
                      .select(F.element_at(F.split(F.element_at(
                              F.split(col('location'), '\\?'), 1), '/'), -1).alias('file_name'),
                              col('reporting_entity_name'),
                              col('sk_pr_loc')), 'file_name', 'left') \
            .select(col('file_path'),
                    col('file_name'),
                    col('reporting_entity_name'),
                    col('sk_pr_loc'),
                    col('provider_groups'))
        self.run_ingest_df(file_path_df)

    def run_ingest_df(self, file_path_df: DataFrame):
        pass

    def run_analytic(self):
        pass

    def run_analytic_df(self, file_name_df: DataFrame):
        pass
