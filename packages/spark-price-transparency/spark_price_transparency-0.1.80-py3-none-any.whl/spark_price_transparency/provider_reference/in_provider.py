"""
in_provider is included in the provider reference schema even through it is already in the in_network_rates schema.
This is one of two exceptions where a table is created with initial inserts by on schema, and updated by another.

To insure consistency of the table, this class will be a sub class of the in-network-rates table with appropriate
overwrites of the merge functions that relate to the provider-reference schema workflow
"""

from ..pt_types import StringType, IntegerType, provider_groups
from ..pt_analytic_table import AnalyticTable
from ..pt_table import Pt_table
from pyspark.sql import DataFrame

class In_provider(AnalyticTable):

    _schema = 'provider-reference'
    _merge_join_cols = ['mth', 'reporting_entity_name', 'sk_provider']

    definition = \
        [("reporting_entity_name", StringType(), False, "Reporting Entity Name"),
         ("sk_provider", IntegerType(), False, "SK of provider details"),
         ("provider_groups", provider_groups, True, "Group of providers as organized by publisher")]
