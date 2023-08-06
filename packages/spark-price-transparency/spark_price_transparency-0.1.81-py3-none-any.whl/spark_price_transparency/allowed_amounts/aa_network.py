from ..pt_ingest_table import IngestTable
from ..pt_types import allowed_amounts, StringType, LongType

class Aa_network(IngestTable):

    _schema = 'allowed-amount'
    header_key: str = "out_of_network"

    definition = \
        [("file_name",                 StringType(),     False, "File name of in network rate json"),
         ("batch_id",                  LongType(),       True,  "Streaming ingest batchId"),
         ("name",                      StringType(),     True,  "Name of the item/service offered"),
         ("billing_code",              StringType(),     True,  "Plan or issuer code for in-network providers"),
         ("billing_code_type",         StringType(),     True,  "Common billing code types."),
         ("billing_code_type_version", StringType(),     True,  "Version of billing code or year of plan"),
         ("allowed_amounts",           allowed_amounts,  True,  "Array of allowed amounts")]
