"""
in_provider is included in the provider reference schema even through it is already in the in_network_rates schema.
This is one of two exceptions where a table is created with initial inserts by on schema, and updated by another.

To insure consistency of the table, this class will be a sub class of the in-network-rates table with appropriate
overwrites of the merge functions that relate to the provider-reference schema workflow
"""

from ..in_network_rates.in_provider import In_provider as Inr_in_provider


class In_provider(Inr_in_provider):

    _schema = 'provider-reference'



