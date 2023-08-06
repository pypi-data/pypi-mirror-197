"""
out_code is an analytic of billing code details from allowd-amounts data

"""
from ..pt_analytic_table import AnalyticTable
from ..pt_types import StringType, IntegerType, planType, billingCodeType

class Out_code(AnalyticTable):

    _schema = 'allowed-amounts'
    _merge_join_cols = ['file_name', 'mth', 'reporting_entity_name', 'sk_code', 'name', 'plan']

    definition = \
        [("file_name",             StringType(),     True,  "Coverage source in-network-rate file"),
         ("reporting_entity_name", StringType(),     True,  "Legal name of the entity publishing"),
         ("reporting_entity_type", StringType(),     True,  "Type of the legal entity"),
         ("plan",                  planType,         True,  "Plan details from Allowed-Amounts file"),
         ("sk_code",               IntegerType(),    True,  "SK of code details"),
         ("name",                  StringType(),     True,  "This is name of the item/service that is offered"),
         ("billing_code",          billingCodeType,  True,  "Issuer billing code details")]
