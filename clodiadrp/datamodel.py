

import numina.datamodel


class QueryFieldType(object):
    def __init__(self, name, type_, description="FILTER used in observation"):
        self.name = name
        self.type = type_
        self.description = description


class ClodiaDatamodel(numina.datamodel.DataModel):
    tag_table = {
        'filter': QueryFieldType('filter', str),
        'insconf': QueryFieldType('insconf', str)
    }
