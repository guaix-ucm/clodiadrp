

import clodiadrp.products as prod
import functools


def test_product():
    t = prod.MasterFlat()

    @functools.singledispatch
    def myfun(ob):
        return 0

    @myfun.register(str)
    def _(obj):
        return "AAAs"

    print(myfun(1))
    print(myfun("a"))

    assert hasattr(t, "tags")
    assert hasattr(t.tags, 'filter')
    assert isinstance(t.tags.filter, prod.TagRepr)
    assert isinstance(t.tags.filter.name, str)
