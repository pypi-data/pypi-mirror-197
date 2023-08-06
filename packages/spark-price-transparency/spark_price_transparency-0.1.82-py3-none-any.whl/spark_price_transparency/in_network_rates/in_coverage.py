"""
In coverage is an analytic table form of in network rate data containing coverage details

"""


from ..pt_analytic_table import AnalyticTable
from ..pt_types import billingCodeType, billingCodesType, planType, StringType, IntegerType

class In_coverage(AnalyticTable):

    _schema = 'in-network-rates'
    _merge_join_cols = ['file_name', 'mth', 'reporting_entity_name', 'sk_coverage']

    definition = \
        [("file_name",             StringType(),     True,  "Coverage source in-network-rate file"),
         ("reporting_entity_name", StringType(),     True,  "Legal name of the entity publishing"),
         ("reporting_entity_type", StringType(),     True,  "Type of the legal entity"),
         ("plan",                  planType,         True,  "Plan details from in-network-rate file"),
         ("sk_coverage",           IntegerType(),    True,  "SK of coverage details and primary key for in_coverage"),
         ("arrangement",           StringType(),     True,  "ffs, bundle, or capitation"),
         ("name",                  StringType(),     True,  "This is name of the item/service that is offered"),
         ("issuer_billing_code",   billingCodeType,  True,  "Issuer billing code details"),
         ("billing_codes",         billingCodesType, True,  "Array of billing code details")]
