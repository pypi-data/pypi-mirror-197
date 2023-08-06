"""
This is the schema class for allowed amounts
"""

from ..pt_schema import Pt_schema
from .aa_header import Aa_header
from .aa_network import Aa_network
from pyspark.sql import DataFrame
from ..pt_functions import F, col, lit

class Allowed_amounts(Pt_schema):

    def _set_tables(self):
        self.ingest_tables = {'aa_header': Aa_header(self.mth, self.catalog_name, self.stage_db_name),
                              'aa_network': Aa_network(self.mth, self.catalog_name, self.stage_db_name)}
        self.analytic_tables = {}

    @property
    def aa_header(self) -> DataFrame:
        return self.ingest_tables['aa_header'].df

    @property
    def aa_network(self) -> DataFrame:
        return self.ingest_tables['aa_network'].df

    def run_ingest(self):
        dbfs_path = f'dbfs:/user/hive/warehouse/pt_raw.db/_raw/mth={self._mth}/schema={self.schema}/'
        file_df = self._spark.read.format("binaryFile") \
            .option("pathGlobFilter", "*.json") \
            .load(dbfs_path).select(col('path').alias('file_path'),
                                    F.element_at(F.split(col('path'), '/'), -1).alias('file_name')) \
            .join(self._spark.table("pt_stage.aa_header"), "file_name", "left_anti")
        self.run_ingest_df(file_df)
