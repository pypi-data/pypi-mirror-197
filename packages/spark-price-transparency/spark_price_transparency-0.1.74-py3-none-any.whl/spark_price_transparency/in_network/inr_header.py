from ..table_stream_tgt import TableStreamTgt
from pyspark.sql import types as T
from pyspark.sql.types import StringType, LongType


class Inr_header(TableStreamTgt):

    definition = [("file_name",             StringType(),   False, "File name of in network rate json"),
                  ("batch_id",              LongType(),     True,  "Streaming ingest batchId"),
                  ("reporting_entity_name", StringType(),   True, "Legal name of the entity publishing"),
                  ("reporting_entity_type", StringType(),   True,  "Type of the legal entity"),
                  ("plan_name",             StringType(),   True,  "Allowed values: EIN, HIOS, <NULL>"),
                  ("plan_id",               StringType(),   True,  "10-digit HIOS, 5-digit HIOS identifier, or EIN"),
                  ("plan_market_type",      StringType(),   True,  "Allowed values: group, individual, <NULL>"),
                  ("last_updated_on",       StringType(),   True,  "Date file was last updated (YYYY-MM-DD)"),
                  ("version",               StringType(),   True,  "Schema version of file")]
