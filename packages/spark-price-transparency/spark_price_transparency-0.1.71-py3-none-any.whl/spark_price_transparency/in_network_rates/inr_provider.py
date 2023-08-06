from ..pt_ingest_table import IngestTable
from ..pt_types import provider_groups, StringType, LongType

class Inr_provider(IngestTable):

    _schema = 'in-network-rates'
    header_key = "provider_references"

    definition = \
        [("file_name",         StringType(),    False, "File name of in network rate json"),
         ("batch_id",          LongType(),      True,  "Streaming ingest batchId"),
         ("provider_group_id", LongType(),      True,  "Publisher defined id reference code"),
         ("provider_groups",   provider_groups, True,  "Group of providers as organized by publisher"),
         ("location",          StringType(),    True,  "URL of download if not provided in provider_groups")]
