from ..pt_table import Pt_table
from ..pt_types import provider_group, StringType

class Pr_provider(Pt_table):

    _schema = 'provider-reference'

    definition = [("file_name",             StringType(),   False, "Name of provider-reference file"),
                  ("reporting_entity_name", StringType(),   True,  "Legal name of the entity publishing"),
                  ("provider_groups",       provider_group, True,  "Negotiated Price Provider Details")]
