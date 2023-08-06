"""
This is the schema class for allowed amounts
"""

from ..pt_schema import Pt_schema
from .aa_header import Aa_header
from .aa_network import Aa_network
from .out_code import Out_code
from .out_amount import Out_amount
from pyspark.sql import DataFrame
from ..pt_functions import F, col, col_sk_code, cols_code

class Allowed_amounts(Pt_schema):

    def _set_tables(self):
        self.ingest_tables = {'aa_header': Aa_header(self.mth, self.catalog_name, self.stage_db_name),
                              'aa_network': Aa_network(self.mth, self.catalog_name, self.stage_db_name)}
        self.analytic_tables = {'out_code': Out_code(self.mth, self.catalog_name, self.stage_db_name),
                                'out_amount': Out_amount(self.mth, self.catalog_name, self.stage_db_name)}

    @property
    def aa_header(self) -> DataFrame:
        return self.ingest_tables['aa_header'].df

    @property
    def aa_network(self) -> DataFrame:
        return self.ingest_tables['aa_network'].df

    @property
    def out_code(self) -> DataFrame:
        return self.analytic_tables['out_code'].df

    @property
    def out_amount(self) -> DataFrame:
        return self.analytic_tables['out_amount'].df

    def run_ingest(self):
        dbfs_path = f'dbfs:/user/hive/warehouse/pt_raw.db/_raw/mth={self._mth}/schema={self.schema}/'
        file_df = self._spark.read.format("binaryFile") \
            .option("pathGlobFilter", "*.json") \
            .load(dbfs_path).select(col('path').alias('file_path'),
                                    F.element_at(F.split(col('path'), '/'), -1).alias('file_name')) \
            .join(self._spark.table("pt_stage.aa_header"), "file_name", "left_anti")
        self.run_ingest_df(file_df)

    def run_analytic(self):
        file_name_df = self.aa_header.select('file_name').distinct() \
            .join(self.out_code.select(col('file_name')).distinct(),
                  "file_name", "left_anti")
        self.run_analytic_df(file_name_df)

    def run_analytic_df(self, file_name_df: DataFrame):
        self._spark.sparkContext.setLocalProperty("callSite.short", f"{self.schema}_analytic")
        header = F.broadcast(
            self.aa_header
                .join(file_name_df, "file_name", "left_semi")
                .groupBy(col('file_name'), col('mth'))
                .agg(F.first(col('reporting_entity_name'), ignorenulls=True).alias('reporting_entity_name'),
                     F.first(col('reporting_entity_type'), ignorenulls=True).alias('reporting_entity_type'),
                     F.first(col('plan_name'), ignorenulls=True).alias('name'),
                     F.first(col('plan_id'), ignorenulls=True).alias('id'),
                     F.first(col('plan_id_type'), ignorenulls=True).alias('id_type'),
                     F.first(col('plan_market_type'), ignorenulls=True).alias('market_type'),
                     F.first(col('last_updated_on'), ignorenulls=True).alias('last_updated_on'))
                .select(col('mth'),
                        col('file_name'),
                        col('reporting_entity_name'),
                        col('reporting_entity_type'),
                        F.struct(col('name'),
                                 col('id'),
                                 col('id_type'),
                                 col('market_type')).alias('plan'))
                .alias('header'))

        network = self.aa_network.repartition(800).alias('network') \
            .join(file_name_df, "file_name", "left_semi") \
            .join(header, "file_name", "left") \
            .select(col('network.mth').alias('mth'),
                    col('file_name'),
                    col('reporting_entity_name'),
                    col('reporting_entity_type'),
                    col('plan'),
                    col_sk_code(),
                    cols_code(),
                    col("allowed_amounts"))

        out_code = network.select(col('mth'),
                                  col('file_name'),
                                  col('reporting_entity_name'),
                                  col('reporting_entity_type'),
                                  col('plan'),
                                  col('sk_code'),
                                  col('code.*'))

        out_amount = network.withColumn('allowed_amount', F.explode(col("allowed_amounts"))) \
            .select(col('mth'),
                    col('file_name'),
                    col('reporting_entity_name'),
                    col('sk_code'),
                    col('allowed_amount'))

        self.analytic_tables['out_amount'].run_analytic_merge(out_amount)
        self.analytic_tables['out_code'].run_analytic_merge(out_code)
