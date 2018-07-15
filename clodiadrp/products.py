

import operator

import numina.types.frame

import clodiadrp.datamodel
import numina.util.namespace
import numina.core.tagexpr as tagexpr
import numina.types.product

try:
    from functools import reduce
except ImportError:
    pass


class TagsNamespace(numina.util.namespace.Namespace):
    def p_(self, name):
        return tagexpr.Placeholder(name)

class TaggedMixin(object):
    def __init__(self,  *args, **kwargs):
        super(TaggedMixin, self).__init__()
        datamodel = kwargs['datamodel']
        self.tag_ids = getattr(self, "tags_headers", [])
        self.tag_ids.extend(kwargs.get('tags', []))
        tg = {key: tagexpr.TagRepr(key) for key in self.tag_ids}
        self.tags = TagsNamespace(**tg)
        self.tags_dict = tg


class QueryAttribute(object):
    def __init__(self, name, tipo, description=""):
        self.name = name
        self.type = tipo
        self.description = description


tag_table = {
    'filter': QueryAttribute('filter', str),
    'grism': QueryAttribute('grism', str),
    'insconf': QueryAttribute('insconf', str)
}


class ClodiaFrame(numina.types.frame.DataFrameType):

    def __init__(self, *args, **kwds):
        kwds['datamodel'] = clodiadrp.datamodel.ClodiaDatamodel

        expr = []

        my_tag_table = getattr(self, '__tag_table__', tag_table)

        if hasattr(self, '__tags__'):
            objtags = [my_tag_table[t] for t in self.__tags__]
            expr = query_expr_from_attr(objtags)

        if 'query_expr' in kwds:
            expr = kwds['query_expr']

        if 'tags' in kwds:
            # Create expresion from tags
            objtags = [my_tag_table[t] for t in kwds['tags']]
            expr = query_expr_from_attr(objtags)

        self.query_expr = expr
        self.names_t = expr.tags()
        self.names_f = expr.fields()

        super().__init__(datamodel=kwds['datamodel'])

    def tag_names(self):
        return self.names_t


class ProcessedImage(ClodiaFrame):
    """A processed frame"""
    pass


class ProcessedImageProduct(numina.types.product.DataProductMixin, ProcessedImage):
    """A processed frame"""
    pass


class MasterBias(ProcessedImageProduct):
    """Master Bias calibration image of CLODIA"""
    __tags__ = []


class MasterFlat(ProcessedImageProduct):
    """Master Flat calibration image of CLODIA"""
    __tags__ = ['filter']
    __tag_table__ = tag_table


class MasterFlatX(ProcessedImageProduct):
    """Master Flat calibration image of CLODIA"""
    def __init__(self):
        super().__init__(tags=['filter', 'grism'])


class SkyImage(ProcessedImage): #, DataProductTag):
    """Sky background image"""
    pass


def query_expr_from_attr(attrs):
    # Create a query descriptor from a sequence for fields
    if len(attrs) == 0:
        return tagexpr.ConstExprTrue
    exprs = []
    #for name, dtype in descs:
    for attr in attrs:
        metadata = {'type': attr.type, 'description': attr.description}
        lhs = tagexpr.TagRepr(attr.name, metadata=metadata)
        rhs = tagexpr.Placeholder(attr.name)
        expr = (lhs == rhs)
        exprs.append(expr)
    return reduce(operator.and_, exprs)


if __name__ == '__main__':
    #print('A')
    #a = MasterFlat()
    #print('B')
    b = MasterFlatX()
    # b = MasterBias()
    expr = b.query_expr
    print('expr, fields', expr.fields())
    print('expr, places', expr.places())

    exprc = expr.fill_tags({'filter': 'U', 'grism': 'J', 'dum': 'B'})
    print(exprc.fields())
    print(exprc.tags())

    constrains = []
    for subtree in tagexpr.filter_tree(tagexpr.condition_terminal, exprc):
        cons = tagexpr.adapter(subtree)
        if cons is not None:
            constrains.append(cons)

    print(constrains)

    # def search_prod(self, name, datatype, tags):
    #
    #     query_expr = datatype.query_expr
    #     expr = query_expr.fill_tags(tags)
    #
    #
    # def convert(expr):
    #     map(tagexpr.adapter, tagexpr.filter_tree(tagexpr.condition_terminal, expr))))
    #     return cons
