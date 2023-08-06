from ..table_stream_tgt import TableStreamTgt
from pyspark.sql.types import ArrayType, StructType, StructField, StringType, FloatType, LongType


class Inr_network(TableStreamTgt):

    header_key: str = "in_network_rates"

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

    definition = \
        [("file_name",                 StringType(),     False, "File name of in network rate json"),
         ("batch_id",                  LongType(),       True,  "Streaming ingest batchId"),
         ("negotiation_arrangement",   StringType(),     True,  "Reimburse arrangement: ffs, bundle, or capitation"),
         ("name",                      StringType(),     True,  "Name of the item/service offered"),
         ("billing_code",              StringType(),     True,  "Plan or issuer code for in-network providers"),
         ("billing_code_type",         StringType(),     True,  "Common billing code types."),
         ("billing_code_type_version", StringType(),     True,  "Version of billing code or year of plan"),
         ("negotiated_rates",          negotiated_rates, True, "Array of negotiated rate & details"),
         ("bundled_codes",             billing_array,    True, "Codes if negotiation_arrangement is a bundle"),
         ("covered_services",          billing_array,    True, "Codes is negotiation_arrangement is capitation")]
