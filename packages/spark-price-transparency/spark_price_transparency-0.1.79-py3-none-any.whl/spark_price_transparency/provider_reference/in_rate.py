"""
In rate is an analytic table form of in network rate data
however, it is included in the provider-reference schema so that
the sk_provider field can be updated after the source provider reference files are imported and ingested

"""
from ..pt_analytic_table import AnalyticTable
from ..pt_types import serviceCodeType, billCodeModifierType, StringType, IntegerType, FloatType, DateType

class In_rate(AnalyticTable):

    _schema = 'provider-reference'
    _merge_join_cols = ['mth', 'reporting_entity_name', 'sk_pr_loc']

    definition = \
        [("file_name", StringType(),     True,  "The source in-network-rates file."),
         ("reporting_entity_name", StringType(),     True,  "Legal name of the entity publishing"),
         ("sk_coverage", IntegerType(), True, "SK of coverage details"),
         ("sk_provider", IntegerType(), True, "SK of provider details"),
         ("sk_pr_loc", IntegerType(), True, "SK of provider group location details"),
         ("negotiated_type", StringType(), True, "negotiated, derived, fee schedule, percentage, or per diem"),
         ("negotiated_rate", FloatType(), True, "Dollar or percentage based on the negotiation_type"),
         ("expiration_date", DateType(), True, "Date agreement for the negotiated_price ends"),
         ("service_code", serviceCodeType, True, "CMS two-digit code(s) placed on a professional claim"),
         ("billing_class", StringType(), True, "professional or institutional"),
         ("billing_code_modifier", billCodeModifierType, True, "Billing Code Modifiers")]
