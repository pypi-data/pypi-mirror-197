"""
This is the schema class for in provider reference
"""

from ..pt_schema import Pt_schema
from .pr_provider import Pr_provider
from .in_provider import In_provider
from .in_rate import In_rate
from pyspark.sql import DataFrame
from ..pt_types import provider_groups_schema
from ..pt_functions import F, col, lit, col_sk_provider
from pandas import DataFrame as Pdf
import pandas as pd
from ..pt_table import Pt_table

class Provider_reference(Pt_schema):

    def _set_tables(self):
        self.ingest_tables = {'pr_provider': Pr_provider(self.mth, self.catalog_name, self.stage_db_name)}
        self.analytic_tables = {'in_provider': In_provider(self.mth, self.catalog_name, self.stage_db_name),
                                'in_rate': In_rate(self.mth, self.catalog_name, self.stage_db_name)}

    def get_tables(self) -> [Pt_table]:
        # We want the table operations to only run for pr_provider since in_provider and in_rate are already in INR
        return [self.ingest_tables['pr_provider'], ]

    @property
    def pr_provider(self) -> DataFrame:
        return self.ingest_tables['pr_provider'].df

    @property
    def in_provider(self) -> DataFrame:
        return self.analytic_tables['in_provider'].df

    @property
    def in_rate(self) -> DataFrame:
        return self.analytic_tables['in_rate'].df

    def run_ingest(self):
        dbfs_path = f'dbfs:/user/hive/warehouse/pt_raw.db/_raw/mth={self._mth}/schema={self.schema}/'
        src_df = self._spark.read.json(dbfs_path, provider_groups_schema) \
            .withColumn('file_name', F.element_at(F.split(F.input_file_name(), '/'), -1)) \
            .join(self.pr_provider, 'file_name', 'left_anti').alias('pr') \
            .join(self._spark.table('pt_stage.in_pr_loc').filter(col('mth') == lit(self.mth)).alias('loc'),
                  col('pr.file_name') == col('loc.tgt_file_name'), "left") \
            .select(col('mth'),
                    col('pr.file_name'),
                    col('reporting_entity_name'),
                    col('sk_pr_loc'),
                    col_sk_provider(),
                    col('provider_groups'))
        self.ingest_tables['pr_provider'].run_ingest_merge(src_df)

    def run_ingest_df(self, file_path_df: DataFrame):
        dbfs_path = f'dbfs:/user/hive/warehouse/pt_raw.db/_raw/mth={self._mth}/schema={self.schema}/'
        file_col = 'file_path' if 'file_path' in file_path_df.columns else file_path_df.columns[0]
        src_df = file_path_df.withColumnRenamed(file_col, 'file_path') \
            .join(self._spark.read.json(dbfs_path, provider_groups_schema)
                  .withColumn('file_path', F.input_file_name(), 'file_path', 'left_semi')) \
            .withColumn('file_name', F.element_at(F.split(F.input_file_name(), '/'), -1)) \
            .join(self.pr_provider, 'file_name', 'left_anti').alias('pr') \
            .join(self._spark.table('pt_stage.in_pr_loc').filter(col('mth') == lit(self.mth)).alias('loc'),
                  col('pr.file_name') == col('loc.tgt_file_name'), "left") \
            .select(col('mth'),
                    col('pr.file_name'),
                    col('reporting_entity_name'),
                    col('sk_pr_loc'),
                    col_sk_provider(),
                    col('provider_groups'))
        self.ingest_tables['pr_provider'].run_ingest_merge(src_df)

    def run_ingest_pdf(self, file_path_pdf: Pdf):
        self.run_ingest_df(self._spark.createDataFrame(file_path_pdf))

    def run_ingest_files(self, file_paths: [str]):
        self.run_ingest_pdf(pd.DataFrame(file_paths, columns=['file_path', ]))

    def run_ingest_file(self, file_path: str):
        self.run_ingest_files([file_path, ])

    def run_analytic_df(self, file_name_df: DataFrame):
        src_df = self.pr_provider.join(file_name_df, "file_name", "left_semi").distinct()
        self.analytic_tables['in_rate'].run_analytic_merge(src_df, False)
        self.analytic_tables['in_provider'].run_analytic_merge(src_df, False)

    def run_analytic(self):
        src_df = self.pr_provider.drop("file_name") \
                     .join(self.in_provider, ['mth', 'reporting_entity_name', 'sk_provider'], "left_anti").distinct()
        self.analytic_tables['in_rate'].run_analytic_merge(src_df, False)
        self.analytic_tables['in_provider'].run_analytic_merge(src_df, False)
