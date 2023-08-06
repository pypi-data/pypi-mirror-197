from ..pt_files import Pt_files
from pyspark.sql import DataFrame

class Provider_reference(Pt_files):

    _meta_ingest_tbl = "pt_stage.in_pr_loc"
