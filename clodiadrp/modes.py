

from numina.core.query import Result, basic_mode_builder


def mosaic_builder(mode, partial_ob, backend):
    """OB builder for ClodiaMosaic"""
    query_res = Result('final', node='children', ignore_fail=True)

    return basic_mode_builder(mode, partial_ob, backend,
                options=query_res)
