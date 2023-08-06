from ..pt_ingest_table import IngestTable
from ..pt_types import reporting_plans, file_location, in_network_files, StringType, LongType

class Toc_reporting(IngestTable):

    _schema = 'table-of-contents'
    header_key = "reporting_structure"

    definition = [("file_name",             StringType(),     False, "File name of table of contents json"),
                  ("batch_id",              LongType(),       True,  "Streaming ingest batchId"),
                  ("reporting_plans",       reporting_plans,  True,  "Legal name of the entity publishing"),
                  ("in_network_files",      in_network_files, True,  "Type of the legal entity"),
                  ("allowed_amount_file",   file_location,    True,  "The plan name and plan sponsor/company.")]
