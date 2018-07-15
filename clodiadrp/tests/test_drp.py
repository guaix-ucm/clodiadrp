from numina.core import BaseRecipe

from ..loader import drp_load


def test_recipes_are_defined():

    current_drp = drp_load()

    assert 'default' in current_drp.pipelines

    for pipeval in current_drp.pipelines.values():
        for key, val in pipeval.recipes.items():
            recipe = pipeval.get_recipe_object(key)
            assert isinstance(recipe, BaseRecipe)


def test_val():
    import clodiadrp.recipes.flat as f

    r = f.Flat()
    l = r.requirements()['master_bias']
    print('call1',r.custom_validator(2))
    print('call2', r.requirements()['master_bias'].v_funcs[0](None, 2))
    #rinput = r.create_input(master_bias='1', obresult=2)
    #print(rinput)
    assert l == 1