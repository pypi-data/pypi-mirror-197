"""
This is to consolidate all of the functions used in transforms
"""

from pyspark.sql.functions import col, lit
from pyspark.sql import functions as F
from pyspark.sql import Column
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

def col_tgt_file_name() -> Column:
    return F.concat(F.element_at(F.split(F.element_at(F.split(F.element_at(F.split(
        col('location'), '\\?'), 1), '/'), -1), '\\.'), 1), lit("_"),
        F.regexp_replace(F.regexp_replace(col("reporting_entity_name"), "[^0-9a-zA-Z ]", ""), " ", "-"),
        lit('.json')).alias('tgt_file_name')


def cols_code():
    return F.struct(col('name'),
                    F.struct(col('billing_code').alias('code'),
                             col('billing_code_type').alias('type'),
                             col('billing_code_type_version').alias('version')).alias('billing_code')).alias('code')


def col_sk_code():
    return F.hash(cols_code()).alias('sk_code')
