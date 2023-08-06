"""
In provider is an analytic table form of in network rates data containing provider details

"""

from ..pt_analytic_table import AnalyticTable
from ..pt_types import provider_groups, StringType, IntegerType

class In_provider(AnalyticTable):

    _schema = 'in-network-rates'
    _merge_join_cols = ['mth', 'reporting_entity_name', 'sk_provider']

    definition = \
        [("reporting_entity_name", StringType(), False, "Reporting Entity Name"),
         ("sk_provider", IntegerType(), False, "SK of provider details"),
         ("provider_groups", provider_groups, True, "Group of providers as organized by publisher")]
