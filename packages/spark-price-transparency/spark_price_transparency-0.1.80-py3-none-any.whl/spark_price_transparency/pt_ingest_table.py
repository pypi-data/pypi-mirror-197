from pyspark.sql import DataFrame
from pyspark.sql.types import StructType
from pyspark.sql.functions import col, lit, from_json, explode

from .pt_table import Pt_table

from typing import Callable

class IngestTable(Pt_table):

    header_key: str = ''

    def get_json_schema(self) -> StructType:
        schema = StructType()
        for kv in [{'field': argv[0], 'data_type': argv[1], 'nullable': argv[2]} for argv in self.definition
                   if argv[0] not in ['file_name', 'batch_id']]:
            schema.add(**kv)
        return schema

    def get_batch_merge_function(self) -> Callable:
        header_key = self.header_key
        schema = self.get_json_schema()
        table_tgt = self.table
        mth = self.mth

        def merge_function(df: DataFrame, batch_id: int):
            src = df.filter(col('header_key') == lit(header_key)) \
                    .select(col('file_name'),
                            explode(col('json_payload')).alias('json_exploded')) \
                    .select(col('file_name'),
                            from_json(col('json_exploded'), schema).alias('exploded_struct')) \
                    .select(lit(mth).alias('mth'),
                            col('file_name'),
                            lit(batch_id).alias('batch_id'),
                            col('exploded_struct.*')).alias('src')
            table_tgt.merge(src, "1 != 1") \
                     .whenNotMatchedInsertAll() \
                     .execute()
        return merge_function
