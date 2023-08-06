"""
This is to consolidate all of the functions used in transforms
"""

from pyspark.sql.functions import col, lit
from pyspark.sql import functions as F
from .pt_types import billingCodesType

def cols_arrangement():
    return F.when(col('negotiation_arrangement') == lit('ffs'),
                  F.struct(col('negotiation_arrangement').alias('arrangement'),
                           col('name'),
                           col('description'),
                           F.struct(col('billing_code').alias('code'),
                                    col('billing_code_type').alias('type'),
                                    col('billing_code_type_version').alias('version')).alias('issuer_billing_code'),
                           F.array(F.struct(col('billing_code').alias('code'),
                                            col('billing_code_type').alias('type'),
                                            col('billing_code_type_version').alias('version'))
                                   ).alias('billing_codes'))) \
          .when(col('negotiation_arrangement') == lit('bundle'),
                F.struct(col('negotiation_arrangement').alias('arrangement'),
                         col('name'),
                         col('description'),
                         F.struct(col('billing_code').alias('code'),
                                  col('billing_code_type').alias('type'),
                                  col('billing_code_type_version').alias('version')).alias('issuer_billing_code'),
                         col('bundled_codes').cast(billingCodesType.simpleString()).alias('billing_codes'))) \
          .when(col('negotiation_arrangement') == lit('capitation'),
                F.struct(col('negotiation_arrangement').alias('arrangement'),
                         col('name'),
                         col('description'),
                         F.struct(col('billing_code').alias('code'),
                                  col('billing_code_type').alias('type'),
                                  col('billing_code_type_version').alias('version')).alias('issuer_billing_code'),
                         col('covered_services').cast(billingCodesType.simpleString()).alias('billing_codes')
                         )).alias('arrangement')

def col_sk_coverage():
    return F.hash(cols_arrangement()).alias('sk_coverage')

def col_sk_provider():
    """ A surrogate key is needed to provide ease of look up for report provider it requires:
     - provider_groups
     - location
    """
    return F.when(col('provider_groups').isNotNull(), F.hash(col('provider_groups'))).alias('sk_provider')

def col_sk_pr_loc():
    """ A provider reference location surrogate key
    """
    return F.when(col('location').isNotNull(), F.hash(col('location'))).alias('sk_pr_loc')
