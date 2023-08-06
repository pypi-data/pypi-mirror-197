"""
out_amount is an analytic of charged amounts to out of network providers from allowed-amounts file

"""
from ..pt_analytic_table import AnalyticTable
from ..pt_types import StringType, IntegerType, allowed_amount

class Out_amount(AnalyticTable):

    _schema = 'allowed-amounts'
    _merge_join_cols = ['file_name', 'mth', 'reporting_entity_name', 'sk_code', 'name', 'plan']

    definition = \
        [("file_name",             StringType(),      True,  "Coverage source in-network-rate file"),
         ("reporting_entity_name", StringType(),      True,  "Legal name of the entity publishing"),
         ("sk_code",               IntegerType(),     True,  "SK of code details"),
         ("allowed_amount",        allowed_amount,    True,  "Issuer paid (allowed) amount reported")]
