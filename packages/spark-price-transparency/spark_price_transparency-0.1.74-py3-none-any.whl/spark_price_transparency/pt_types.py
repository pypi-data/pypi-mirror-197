"""
This is to consolidate all of the types used in table definitions & transforms
"""

from pyspark.sql.types import *

planType = StructType([StructField("name", StringType(), True),
                       StructField("id", StringType(), True),
                       StructField("id_type", StringType(), True),
                       StructField("market_type", StringType(), True)])

billingCodeType = StructType([StructField("code", StringType(), True),
                              StructField("type", StringType(), True),
                              StructField("version", StringType(), True)])

billingCodesType = ArrayType(billingCodeType)

provider_groups = ArrayType(StructType([
    StructField("npi", ArrayType(StringType()), True),
    StructField("tin", StructType([
        StructField("type", StringType(), True),
        StructField("value", StringType(), True)]), True)]))

serviceCodeType = ArrayType(StringType())
billCodeModifierType = ArrayType(StringType())

reporting_plans = ArrayType(StructType([
    StructField("plan_name", StringType(), True),
    StructField("plan_id", StringType(), True),
    StructField("plan_id_type", StringType(), True),
    StructField("plan_market_type", StringType(), True)]))

file_location = StructType([
    StructField("description", StringType(), True),
    StructField("location", StringType(), True)])

in_network_files = ArrayType(file_location)

provider_group = StructType([StructField("npi", ArrayType(StringType()), True),
                             StructField("tin", StructType([
                                 StructField("type", StringType(), True),
                                 StructField("value", StringType(), True)]), True)])

providers = ArrayType(StructType([
    StructField("billed_charge", FloatType(), True),
    StructField("npi", ArrayType(StringType()), True)]))

payments = ArrayType(StructType([
    StructField("allowed_amount", FloatType(), True),
    StructField("billing_code_modifier", ArrayType(StringType()), True),
    StructField("providers", providers, True)]))

allowed_amounts = ArrayType(StructType([
    StructField("tin", StructType([
        StructField("type", StringType(), True),
        StructField("value", StringType(), True)
    ]), True),
    StructField("service_code", ArrayType(StringType()), True),
    StructField("billing_class", StringType(), True),
    StructField("payments", payments, True)]))

negotiated_rates = ArrayType(StructType([
    StructField("negotiated_prices", ArrayType(StructType([
        StructField("negotiated_type", StringType(), True),
        StructField("negotiated_rate", FloatType(), True),
        StructField("expiration_date", StringType(), True),
        StructField("service_code", ArrayType(StringType()), True),
        StructField("billing_class", StringType(), True),
        StructField("billing_code_modifier", ArrayType(StringType()), True)])), True),
    StructField("provider_groups", ArrayType(StructType([
        StructField("npi", ArrayType(StringType()), True),
        StructField("tin", StructType([
            StructField("type", StringType(), True),
            StructField("value", StringType(), True)
        ]), True)
    ])), True),
    StructField("provider_references", ArrayType(LongType()), True)]))

billing_array = ArrayType(StructType([
    StructField("billing_code", StringType(), True),
    StructField("billing_code_type", StringType(), True),
    StructField("billing_code_type_version", StringType(), True)]))
