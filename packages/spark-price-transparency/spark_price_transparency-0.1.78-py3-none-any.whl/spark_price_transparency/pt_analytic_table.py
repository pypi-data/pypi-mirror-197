from .pt_table import Pt_table
from pyspark.sql import DataFrame


class AnalyticTable(Pt_table):

    _merge_join_cols: [str]

    def run_update(self):
        """
        This method is intended to be over written
        """
        pass

    def run_analytic_merge(self, src_df: DataFrame, insert_only=True):
        """
        Delta merge wrapper with option to insert only overwrite on merge
        """
        join_condition = "false" if insert_only else \
            ' AND '.join([f'(src.{c} = tgt.{c})' for c in self._merge_join_cols])
        self.table.alias('tgt').merge(source=src_df.alias('src'),
                                      condition=join_condition) \
            .whenMatchedUpdateAll() \
            .whenNotMatchedInsertAll().execute()
