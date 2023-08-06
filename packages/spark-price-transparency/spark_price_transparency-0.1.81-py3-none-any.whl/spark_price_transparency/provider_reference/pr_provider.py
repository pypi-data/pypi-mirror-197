"""
pr_provider is very different than the typical ingest tables
Since we don't want to pay the overhead of a streaming job for the small json files,
we are going to write all of the methods in schema to make it appear as the other ingest
processes, but actually do a batch merge instead. This is help maintain
method conventions which will be appreciated by users.
"""

from ..pt_table import Pt_table
from ..pt_types import provider_groups, StringType, IntegerType
from pyspark.sql import DataFrame

class Pr_provider(Pt_table):

    _schema = 'provider-reference'
    _merge_join_cols = ['mth', 'file_name']

    definition = [("file_name",             StringType(),   False,  "Name of provider-reference file"),
                  ("reporting_entity_name", StringType(),   True,   "Legal name of the entity publishing"),
                  ("sk_pr_loc",             IntegerType(),  False,  "SK of provider group location details"),
                  ("sk_provider",           IntegerType(),  True,   "SK of provider details"),
                  ("provider_groups",       provider_groups, True,  "Negotiated Price Provider Details")]

    def run_ingest_merge(self, src_df: DataFrame, insert_only=True):
        """
        Delta merge wrapper with option to insert only overwrite on merge
        """
        join_condition = "false" if insert_only else \
            ' AND '.join([f'(src.{c} = tgt.{c})' for c in self._merge_join_cols])
        self.table.alias('tgt').merge(source=src_df.alias('src'),
                                      condition=join_condition) \
            .whenMatchedUpdateAll() \
            .whenNotMatchedInsertAll().execute()
