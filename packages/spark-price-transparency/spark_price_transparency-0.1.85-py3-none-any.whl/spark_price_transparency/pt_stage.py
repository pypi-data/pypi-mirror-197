
from pyspark.sql.session import SparkSession
from .table_of_contents.schema import Table_of_contents
from .in_network_rates.schema import In_network_rates
from .allowed_amounts.schema import Allowed_amounts
from .provider_reference.schema import Provider_reference
from datetime import date

class PTStage:

    _spark: SparkSession
    _mth: int
    _catalog_name: str
    _stage_db_name: str
    table_of_contents: Table_of_contents
    in_network_rates: In_network_rates
    provider_reference: Provider_reference
    allowed_amounts: Allowed_amounts

    def __init__(self, mth: int = None, catalog_name='hive_metastore', stage_db_name='pt_stage'):
        self._spark = SparkSession.builder.getOrCreate()
        self._mth = mth
        self._catalog_name = catalog_name
        self._stage_db_name = stage_db_name
        self.in_network_rates = In_network_rates(self.mth, self.catalog_name, self.stage_db_name)
        self.table_of_contents = Table_of_contents(self.mth, self.catalog_name, self.stage_db_name)
        self.allowed_amounts = Allowed_amounts(self.mth, self.catalog_name, self.stage_db_name)
        self.provider_reference = Provider_reference(self.mth, self.catalog_name, self.stage_db_name)

    @property
    def mth(self):
        return self._mth

    @mth.setter
    def mth(self, value):
        mth = int(value)
        self._mth = mth
        print(f'pt_raw.mth set to {mth}.')
        self.table_of_contents.mth = mth
        # self.in_network_rates.mth = mth
        # self.provider_reference.mth = mth
        # self.allowed_amount.mth = mth

    @mth.deleter
    def mth(self):
        mth = int(date.today().strftime('%Y%m'))
        self._mth = mth
        print(f"pt_raw.mth reset to {mth}")
        del self.table_of_contents.mth
        # del self.in_network_rates.mth
        # del self.provider_reference.mth
        # del self.allowed_amount.mth

    @property
    def catalog_name(self):
        return self._catalog_name

    @property
    def stage_db_name(self):
        return self._stage_db_name

    def create_stage_database(self):
        # TODO: check if database already exists
        self._spark.sql(f'CREATE DATABASE IF NOT EXISTS {self.stage_db_name}')

    def initialize_pt_stage(self):
        self.create_stage_database()
        self.table_of_contents.create_tables()
        self.in_network_rates.create_tables()
        self.allowed_amounts.create_tables()
        self.provider_reference.create_tables()
