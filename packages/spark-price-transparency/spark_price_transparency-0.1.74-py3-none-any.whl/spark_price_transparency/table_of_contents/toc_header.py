from ..pt_ingest_table import IngestTable
from pyspark.sql.types import StringType, LongType


class Toc_header(IngestTable):

    _schema = 'table-of-contents'

    definition = [("file_name", StringType(), False, "File name of table of contents json"),
                  ("batch_id", LongType(), True, "Streaming ingest batchId"),
                  ("reporting_entity_name", StringType(), True, "Legal name of the entity publishing"),
                  ("reporting_entity_type", StringType(), True, "Type of the legal entity")]
