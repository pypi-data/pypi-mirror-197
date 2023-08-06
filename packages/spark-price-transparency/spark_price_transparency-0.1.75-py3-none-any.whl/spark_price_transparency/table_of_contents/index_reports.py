"""
Index reports is the analytic form for table of contents data
It is necessary since it will have all of the files that need to be ingested for any given payer
"""

from ..pt_analytic_table import AnalyticTable
from ..pt_types import StringType, reporting_plans

class Index_reports(AnalyticTable):

    definition = \
        [("file_name",             StringType(),    True, "Table of Contents data source file name"),
         ("reporting_entity_name", StringType(),    True, "Entity Name of the TOC reporting entity"),
         ("reporting_entity_type", StringType(),    True, "Entity Type of the TOC reporting entity"),
         ("file_type",             StringType(),    True, "File Type; 'in-network-rates' or 'allowed-amounts'"),
         ("location",              StringType(),    True, "URL of file"),
         ("reporting_plans",       reporting_plans, True, "Location file plans detail")]
