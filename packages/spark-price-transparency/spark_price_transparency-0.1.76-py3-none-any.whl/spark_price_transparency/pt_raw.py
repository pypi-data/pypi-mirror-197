from pyspark.sql.session import SparkSession
import os
from datetime import date
from pyspark.sql.functions import col
from pyspark.sql import functions as F
from .table_of_contents.files import Table_of_contents
from .in_network_rates.files import In_network_rates
from .provider_reference.files import Provider_reference
from .allowed_amounts.files import Allowed_amounts

class PTRaw:

    _spark: SparkSession
    _mth: int
    _catalog_name: str
    _raw_db_name: str
    table_of_contents: Table_of_contents
    in_network_rates = In_network_rates
    provider_reference = Provider_reference
    allowed_amounts = Allowed_amounts

    def __init__(self, mth: int = None, catalog_name='hive_metastore', raw_db_name='pt_raw'):
        self._spark = SparkSession.builder.getOrCreate()
        self._mth = mth if mth is not None else int(date.today().strftime('%Y%m'))
        self._catalog_name = catalog_name
        self._raw_db_name = raw_db_name
        self.table_of_contents = Table_of_contents(self.mth, self.catalog_name, self.raw_db_name)
        self.in_network_rates = In_network_rates(self.mth, self.catalog_name, self.raw_db_name)
        self.provider_reference = Provider_reference(self.mth, self.catalog_name, self.raw_db_name)
        self.allowed_amounts = Allowed_amounts(self.mth, self.catalog_name, self.raw_db_name)

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
    def raw_db_name(self):
        return self._raw_db_name

    @property
    def locationUri(self):
        """
        We want to always get location Uri from the catalog so that we don't risk use of a custom location
        For now we will only accepts pt_raw as the raw database name
        """
        database = [d for d in self._spark.catalog.listDatabases() if d.name == "pt_raw"]
        if len(database) == 0:
            print(f'WARNING: pt_stage database does not exist. Run Guide.initialize_pt()' +
                  ' or PTRaw.initialize_pt_raw().')
            location_uri = None
        else:
            location_uri = database[0].locationUri
        return location_uri

    @property
    def locationPath(self):
        return self.locationUri.replace('dbfs:', '/dbfs')

    def create_raw_database(self):
        # TODO: check if database already exists
        if self.locationUri is None:
            self._spark.sql(f'CREATE DATABASE IF NOT EXISTS pt_stage')
            print(f'Database pt_raw created.')
        else:
            print(f'Database pt_raw already exists.')

    def create_raw_directory(self):
        """
        The raw directory is required for a location to put raw files. Since it will not be a table,
        we will provide it with a _ prefix to avoid potential managed table conflicts
        Currently this path is not argumented.
        Currently this path generation is done only by local fs os operations to avoid dependency on dbutils.
        """
        path = self.locationPath + '/_raw'
        if os.path.exists(path):
            print(f'{path} already exists.')
        else:
            os.mkdir(path)
            print(f'{path} created.')

    def create_raw_mth_directory(self):
        """
        This will simply create a new month with sub directories to put more files.
        """
        path = self.locationPath + f'/_raw/mth={self.mth}'
        if os.path.exists(path):
            print(f'{path} already exists.')
        else:
            os.mkdir(path)
            print(f'{path} created.')
            os.mkdir(path + '/schema=table-of-contents')
            print(f'{path}/schema=table-of-contents created.')
            os.mkdir(path + '/schema=in-network-rates')
            print(f'{path}/schema=in-network-rates created.')
            os.mkdir(path + '/schema=provider-reference')
            print(f'{path}/schema=provider-reference created.')
            os.mkdir(path + '/schema=allowed-amount')
            print(f'{path}/schema=allowed-amount created.')
        pass

    def initialize_pt_raw(self):
        self.create_raw_database()
        self.create_raw_directory()
        self.create_raw_mth_directory()

    @property
    def files(self):
        """
        Files will be real time definition of files in the raw directory.
        This is intended to help with the state of ingest.
        """
        return self._spark.read.format("binaryFile") \
            .option("pathGlobFilter", "*.json") \
            .load(self.locationUri + '/_raw') \
            .drop('content') \
            .select(col('mth'),
                    col('schema'),
                    F.element_at(F.split(col('path'), '/'), -1).alias('file_name'),
                    col('path').alias('file_path'),
                    col('length'),
                    col('modificationTime'))
