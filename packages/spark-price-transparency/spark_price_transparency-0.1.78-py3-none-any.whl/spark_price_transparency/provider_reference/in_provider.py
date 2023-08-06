"""
in_provider is included in the provider reference schema even through it is already in the in_network_rates schema.
This is one of two exceptions where a table is created with initial inserts by on schema, and updated by another.

To insure consistency of the table, this class will be a sub class of the in-network-rates table with appropriate
overwrites of the merge functions that relate to the provider-reference schema workflow
"""

from ..in_network_rates.in_provider import In_provider as Inr_in_provider
from ..pt_types import StringType, IntegerType, provider_groups

class In_provider(Inr_in_provider):

    _schema = 'provider-reference'
    _merge_join_cols = ['mth', 'reporting_entity_name', 'sk_provider']

    definition = \
        [("reporting_entity_name", StringType(), False, "Reporting Entity Name"),
         ("sk_provider", IntegerType(), False, "SK of provider details"),
         ("provider_groups", provider_groups, True, "Group of providers as organized by publisher")]
