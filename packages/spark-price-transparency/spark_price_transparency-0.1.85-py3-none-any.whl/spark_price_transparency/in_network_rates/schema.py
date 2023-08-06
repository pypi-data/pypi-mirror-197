"""
This is the schema class for in network rates
"""

from ..pt_schema import Pt_schema
from .inr_header import Inr_header
from .inr_network import Inr_network
from .inr_provider import Inr_provider
from .in_coverage import In_coverage
from .in_rate import In_rate
from .in_provider import In_provider
from .in_pr_loc import In_pr_loc
from pyspark.sql import DataFrame
from ..pt_functions import col, F, cols_arrangement, col_sk_coverage, \
                                   col_sk_provider, col_sk_pr_loc, col_tgt_file_name

class In_network_rates(Pt_schema):

    def _set_tables(self):
        self.ingest_tables = {'inr_header': Inr_header(self.mth, self.catalog_name, self.stage_db_name),
                              'inr_network': Inr_network(self.mth, self.catalog_name, self.stage_db_name),
                              'inr_provider': Inr_provider(self.mth, self.catalog_name, self.stage_db_name)}
        self.analytic_tables = {'in_coverage': In_coverage(self.mth, self.catalog_name, self.stage_db_name),
                                'in_rate': In_rate(self.mth, self.catalog_name, self.stage_db_name),
                                'in_provider': In_provider(self.mth, self.catalog_name, self.stage_db_name),
                                'in_pr_loc': In_pr_loc(self.mth, self.catalog_name, self.stage_db_name)}

    @property
    def inr_header(self) -> DataFrame:
        return self.ingest_tables['inr_header'].df

    @property
    def inr_network(self) -> DataFrame:
        return self.ingest_tables['inr_network'].df

    @property
    def inr_provider(self) -> DataFrame:
        return self.ingest_tables['inr_provider'].df

    @property
    def in_coverage(self) -> DataFrame:
        return self.analytic_tables['in_coverage'].df

    @property
    def in_rate(self) -> DataFrame:
        return self.analytic_tables['in_rate'].df

    @property
    def in_provider(self) -> DataFrame:
        return self.analytic_tables['in_provider'].df

    def run_ingest(self):
        dbfs_path = f'dbfs:/user/hive/warehouse/pt_raw.db/_raw/mth={self._mth}/schema={self.schema}/'
        file_df = self._spark.read.format("binaryFile") \
                      .option("pathGlobFilter", "*.json") \
                      .load(dbfs_path).select(col('path').alias('file_path'),
                                              F.element_at(F.split(col('path'), '/'), -1).alias('file_name')) \
                      .join(self._spark.table("pt_stage.inr_header"), "file_name", "left_anti")
        self.run_ingest_df(file_df)

    def run_analytic(self):
        file_name_df = self.inr_header.select('file_name').distinct() \
            .join(self.in_coverage.select(col('file_name')).distinct(),
                  "file_name", "left_anti")
        self.run_analytic_df(file_name_df)

    def run_analytic_df(self, file_name_df: DataFrame):
        self._spark.sparkContext.setLocalProperty("callSite.short", f"{self.schema}_analytic")
        file_name_df.cache()
        header = F.broadcast(
            self.inr_header
                .join(file_name_df, "file_name", "left_semi")
                .groupBy(col('file_name'), col('mth'))
                .agg(F.first(col('reporting_entity_name'), ignorenulls=True).alias('reporting_entity_name'),
                     F.first(col('reporting_entity_type'), ignorenulls=True).alias('reporting_entity_type'),
                     F.first(col('plan_name'), ignorenulls=True).alias('name'),
                     F.first(col('plan_id'), ignorenulls=True).alias('id'),
                     F.first(col('plan_id_type'), ignorenulls=True).alias('id_type'),
                     F.first(col('plan_market_type'), ignorenulls=True).alias('market_type'),
                     F.first(col('last_updated_on'), ignorenulls=True).alias('last_updated_on'))
            .alias('header'))

        network = self.inr_network.repartition(1200) \
            .join(file_name_df, "file_name", "left_semi") \
            .withColumn('arrangement', cols_arrangement()) \
            .withColumn('sk_coverage', col_sk_coverage()) \
            .alias('network')

        provider = self.inr_provider \
            .join(file_name_df, "file_name", "left_semi") \
            .select(col('file_name'),
                    col('mth'),
                    col('provider_group_id'),
                    col_sk_provider(),
                    col_sk_pr_loc(),
                    col("provider_groups"),
                    col("location")) \
            .distinct().alias('provider')

        in_coverage = header.select(col('mth'),
                                    col('file_name'),
                                    col('reporting_entity_name'),
                                    col('reporting_entity_type'),
                                    F.struct(col('name'),
                                             col('id'),
                                             col('id_type'),
                                             col('market_type')).alias('plan')).alias('header') \
            .join(network.select(col('file_name'),
                                 col('sk_coverage'),
                                 col('arrangement.*')),
                  'file_name', 'left').distinct()

        rate = network.join(header, 'file_name', 'left') \
            .withColumn('negotiated_rate', F.explode('negotiated_rates')) \
            .select('file_name', 'reporting_entity_name', 'network.mth', 'sk_coverage',
                    'negotiated_rate.*').alias('network') \
            .join(provider, [col('network.file_name') == col('provider.file_name'),
                             F.array_contains(col('provider_references'), col('provider.provider_group_id'))], "left") \
            .select('network.file_name',
                    'network.reporting_entity_name',
                    'network.mth',
                    'network.sk_coverage',
                    col('network.provider_groups').alias('network_provider_groups'),
                    F.coalesce('network.provider_groups', 'provider.provider_groups').alias('provider_groups'),
                    'location',
                    'negotiated_prices') \
            .withColumn('sk_provider', col_sk_provider()) \
            .withColumn('sk_pr_loc', col_sk_pr_loc())

        in_rate = rate.withColumn('negotiated_price', F.explode('negotiated_prices')) \
            .select(col('file_name'),
                    col('reporting_entity_name'),
                    col('mth'),
                    col('sk_coverage'),
                    col('sk_provider'),
                    col('sk_pr_loc'),
                    col('sk_provider'),
                    col('negotiated_price.*')) \
            .withColumn('expiration_date', F.to_date(col('expiration_date'), "yyyy-MM-dd"))

        in_provider_network = rate.filter(col('network_provider_groups').isNotNull()) \
            .select('mth',
                    'reporting_entity_name',
                    'sk_provider',
                    'provider_groups').distinct()

        in_provider_provider = provider.filter(col('provider_groups').isNotNull()) \
            .join(header, 'file_name', 'left') \
            .select('provider.mth',
                    'reporting_entity_name',
                    'sk_provider',
                    'provider_groups').distinct()

        in_pr_loc = provider.filter(col('location').isNotNull()) \
            .join(header, 'file_name', 'left') \
            .select(col('provider.mth'),
                    col('file_name'),
                    col('reporting_entity_name'),
                    col_tgt_file_name(),
                    col('sk_pr_loc'),
                    col('location')).distinct()

        # TODO: evaluate performance of running run_analytic_merges in parallel
        self.analytic_tables['in_rate'].run_analytic_merge(in_rate)
        self.analytic_tables['in_provider'].run_analytic_merge(in_provider_network)
        self.analytic_tables['in_provider'].run_analytic_merge(in_provider_provider)
        self.analytic_tables['in_pr_loc'].run_analytic_merge(in_pr_loc)
        # NOTE: Coverage is last since it is the where we identify if files were part of prior run_analytic
        self.analytic_tables['in_coverage'].run_analytic_merge(in_coverage)
        file_name_df.unpersist()
