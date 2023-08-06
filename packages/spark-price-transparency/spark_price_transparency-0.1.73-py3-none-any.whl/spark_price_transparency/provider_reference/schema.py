"""
This is the schema class for in provider reference
"""

from ..pt_schema import Pt_schema
from .pr_provider import Pr_provider


class Provider_reference(Pt_schema):

    def _set_tables(self):
        self.ingest_tables = {'pr_provider': Pr_provider(self.mth, self.catalog_name, self.stage_db_name)}
        self.analytic_tables = {}

    def run_file_analytic_merge(self, file_name):
        # TODO: Run analytic merges in parallel
        pass
        # self.analytic_tables['in_provider'].run_file_analytic_merge(file_name)
        # self.analytic_tables['in_coverage'].run_file_analytic_merge(file_name)
        # self.analytic_tables['in_rate'].run_file_analytic_merge(file_name)
