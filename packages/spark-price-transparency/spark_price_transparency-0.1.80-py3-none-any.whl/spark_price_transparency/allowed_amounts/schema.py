"""
This is the schema class for allowed amounts
"""

from ..pt_schema import Pt_schema
from .aa_header import Aa_header
from .aa_network import Aa_network

class Allowed_amounts(Pt_schema):

    def _set_tables(self):
        self.ingest_tables = {'aa_header': Aa_header(self.mth, self.catalog_name, self.stage_db_name),
                              'aa_network': Aa_network(self.mth, self.catalog_name, self.stage_db_name)}
        self.analytic_tables = {}
