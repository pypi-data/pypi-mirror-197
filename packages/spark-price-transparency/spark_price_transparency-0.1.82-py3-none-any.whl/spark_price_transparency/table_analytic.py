
from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession
from delta.tables import DeltaTable
from pyspark.sql.types import StructType, DateType

class TableAnalytic:

    spark: SparkSession
    definition: [(str, DateType, bool, str)] = []
    df: DataFrame
    table: DeltaTable

    def __init__(self, spark):
        self.spark: SparkSession = spark
        self.tbl_name = self.__class__.__name__.lower()
        self.wh_tbl_name = '.'.join(['pt_stage', self.tbl_name])

    def get_df(self) -> DataFrame:
        return self.spark.table(self.wh_tbl_name)

    def get_table(self) -> DeltaTable:
        return DeltaTable.forName(self.spark, self.wh_tbl_name)

    def create_table(self) -> None:
        dt = DeltaTable.createIfNotExists(self.spark).tableName(self.wh_tbl_name)
        for c in self.definition:
            dt.addColumn(*c[:-1], comment=c[-1])
        dt.execute()

    def drop_table(self) -> None:
        self.spark.sql(f'DROP TABLE IF EXISTS {self.wh_tbl_name}')

    def create_view(self) -> None:
        self.df.createOrReplaceTempView(self.tbl_name)

    def purge_table(self) -> None:
        self.spark.sql(f'DELETE FROM {self.wh_tbl_name} WHERE 1=1')
        DeltaTable.forName(self.spark, self.wh_tbl_name).vacuum()

    def set_table(self) -> None:
        self.table = self.get_table()

    def set_df(self) -> None:
        self.df = self.get_df()