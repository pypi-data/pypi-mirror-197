from ..pt_ingest_table import IngestTable
from ..pt_types import negotiated_rates, billing_array, StringType, LongType

class Inr_network(IngestTable):

    _schema = 'in-network-rates'
    header_key: str = "in_network"

    definition = \
        [("file_name",                 StringType(),     False, "File name of in network rate json"),
         ("batch_id",                  LongType(),       True,  "Streaming ingest batchId"),
         ("negotiation_arrangement",   StringType(),     True,  "Reimburse arrangement: ffs, bundle, or capitation"),
         ("name",                      StringType(),     True,  "Name of the item/service offered"),
         ("billing_code",              StringType(),     True,  "Plan or issuer code for in-network providers"),
         ("billing_code_type",         StringType(),     True,  "Common billing code types."),
         ("billing_code_type_version", StringType(),     True,  "Version of billing code or year of plan"),
         ("description",               StringType(),     True,  "Brief description of the item/service"),
         ("negotiated_rates",          negotiated_rates, True,  "Array of negotiated rate & details"),
         ("bundled_codes",             billing_array,    True,  "Codes if negotiation_arrangement is a bundle"),
         ("covered_services",          billing_array,    True,  "Codes is negotiation_arrangement is capitation")]
