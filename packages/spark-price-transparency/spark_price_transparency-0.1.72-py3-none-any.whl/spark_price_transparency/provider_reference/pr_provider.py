from ..pt_ingest_table import IngestTable
from ..pt_types import provider_group, StringType, LongType

class Pr_provider(IngestTable):

    _schema = 'provider-reference'
    header_key = 'provider_groups'

    definition = [("file_name",       StringType(),   False, "Negotiated Price Provider Details"),
                  ("batch_id",        LongType(),     True,  "Streaming ingest batchId"),
                  ("provider_groups", provider_group, True, "Negotiated Price Provider Details")]
