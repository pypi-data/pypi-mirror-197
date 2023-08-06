"""
This is the base table class that will include all common delta table operations
"""

from pyspark.sql import DataFrame
from pyspark.sql.session import SparkSession
from delta.tables import DeltaTable
from pyspark.sql.types import DateType
from datetime import date
from pyspark.sql.functions import col, lit

class Pt_table:

    _spark: SparkSession
    _mth: int
    _catalog_name: str
    _stage_db_name: str
    _schema: str
    definition: [(str, DateType, bool, str)] = []

    def __init__(self, mth: int = None, catalog_name='hive_metastore', stage_db_name='pt_stage'):
        self._spark = SparkSession.builder.getOrCreate()
        self._mth = int(date.today().strftime('%Y%m')) if mth is None else mth
        self._catalog_name = catalog_name
        self._stage_db_name = stage_db_name

    @property
    def schema(self):
        return self._schema

    @property
    def tbl_name(self):
        return self.__class__.__name__.lower()

    @property
    def db_tbl_name(self):
        return '.'.join([self._stage_db_name, self.tbl_name])

    @property
    def cat_db_tbl_name(self):
        return '.'.join([self._catalog_name, self._stage_db_name, self.tbl_name])

    @property
    def mth(self):
        return self._mth

    @mth.setter
    def mth(self, value):
        mth = int(value)
        self._mth = mth
        print(f'pt_stage.{self.schema.replace("-","_")}.mth set to {mth}.')

    @mth.deleter
    def mth(self):
        mth = int(date.today().strftime('%Y%m'))
        self._mth = mth
        print(f'pt_stage.{self.schema.replace("-","_")}.mth reset to {mth}')

    @property
    def df(self) -> DataFrame:
        return self._spark.table(self.db_tbl_name).filter(col('mth') == lit(self._mth))

    @property
    def table(self) -> DeltaTable:
        return DeltaTable.forName(self._spark, self.db_tbl_name)

    def create_table(self) -> None:
        dt = DeltaTable.createIfNotExists(self._spark).tableName(self.db_tbl_name)
        dt.addColumn("mth", dataType="INT", nullable=False)
        for c in self.definition:
            dt.addColumn(*c[:-1], comment=c[-1])
        dt.partitionedBy("mth")
        dt.execute()

    def drop_table(self) -> None:
        self._spark.sql(f'DROP TABLE IF EXISTS {self.db_tbl_name}')

    def create_view(self) -> None:
        self.df.createOrReplaceTempView(self.tbl_name)

    def purge_table(self) -> None:
        self._spark.sql(f'DELETE FROM {self.db_tbl_name} WHERE 1=1')
        DeltaTable.forName(self._spark, self.db_tbl_name).vacuum()
