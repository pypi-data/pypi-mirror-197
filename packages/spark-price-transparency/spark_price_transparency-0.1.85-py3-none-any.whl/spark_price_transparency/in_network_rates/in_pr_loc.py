"""
in_pr_loc table is used to store the location data for provider
it is generated only from inr_network and is consumed only to
import pr data into provider reference schema
"""

from ..pt_analytic_table import AnalyticTable
from pyspark.sql.types import StringType, IntegerType

class In_pr_loc(AnalyticTable):

    _schema = 'in-network-rates'
    _merge_join_cols = ['file_name', 'mth', 'reporting_entity_name', 'sk_pr_loc']

    definition = \
        [("file_name", StringType(), True, "Name of source in-network-rates file."),
         ("reporting_entity_name", StringType(), False, "Reporting Entity Name"),
         ("tgt_file_name", StringType(), False, "Target File Name used for unique file identification"),
         ("sk_pr_loc", IntegerType(), False, "SK of provider group location details"),
         ("location", StringType(), True, "Location of remote provider groups file")]
