from pyspark.sql.session import SparkSession
from datetime import date
from .pt_raw import PTRaw
from .pt_stage import PTStage

class Guide:

    _spark: SparkSession
    _mth: int
    catalog_name: str
    _raw_db_name: str
    _stage_db_name: str
    pt_raw: PTRaw
    pt_stage: PTStage

    def __init__(self, mth: int = None, catalog_name='hive_metastore', raw_db_name='pt_raw', stage_db_name='pt_stage'):
        self._spark = SparkSession.builder.getOrCreate()
        self._mth = mth if mth is not None else int(date.today().strftime('%Y%m'))
        self._catalog_name = catalog_name
        self._raw_db_name = raw_db_name
        self._stage_db_name = stage_db_name
        self.pt_raw = PTRaw(mth=self.mth)
        self.pt_stage = PTStage(mth=self.mth)

    @property
    def mth(self):
        return self._mth

    @mth.setter
    def mth(self, value):
        mth = int(value)
        self._mth = mth
        print(f'guide.mth set to {mth}.')

    @mth.deleter
    def mth(self):
        mth = int(date.today().strftime('%Y%m'))
        self._mth = mth
        print(f'guide.mth reset to {mth}')

    def initialize(self):
        self.pt_raw.initialize_pt_raw()
        self.pt_stage.initialize_pt_stage()
