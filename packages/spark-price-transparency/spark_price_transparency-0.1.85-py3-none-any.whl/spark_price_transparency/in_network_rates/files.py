from ..pt_files import Pt_files
from pyspark.sql.functions import col, lit
from pyspark.sql import functions as F


class In_network_rates(Pt_files):

    _meta_ingest_tbl = "pt_stage.inr_header"

    def run_import(self):
        self._spark.sparkContext.setLocalProperty("callSite.short", f"{self.schema}_import")
        file_df = self._spark.table('pt_stage.index_reports').filter(col('')) \
            .select(col('location').alias('url'),
                    F.element_at(
                     F.split(
                      F.element_at(
                       F.split(
                        F.element_at(
                         F.split(col('location'), "\\?"), 1), '/'), -1), '\\.'), 1).alias('file_name')) \
            .join(self._spark.read.format("binaryFile").option("pathGlobFilter", "*").load(self.dbfs_path)
                  .select(F.element_at(
                           F.split(F.element_at(F.split(col('path'), '/'), -1), '\\.'), 1).alias('file_name')),
                  "file_name", "left_anti")
        self.run_import_df(file_df)
