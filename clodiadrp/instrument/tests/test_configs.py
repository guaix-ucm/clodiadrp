import pytest
import numina.core.pipeline

import clodiadrp.loader


@pytest.mark.parametrize('cfgid', [
        '6211acd9-e75b-4b91-a59d-cb0e4a78dd24',
        'eb8a30e4-4aa1-4f4d-90cb-af1bb21edf50',
    ])
def test_conf1(cfgid):
    drp = clodiadrp.loader.drp_load()

    assert cfgid in drp.configurations

    cfg = drp.configurations[cfgid]
    assert isinstance(cfg, numina.core.pipeline.InstrumentConfiguration)
    assert cfg.instrument == 'CLODIA'
    assert cfg.uuid == cfgid

    assert 'detector' in cfg.components

    for key, val in cfg.components.items():
        assert isinstance(val, numina.core.pipeline.ComponentConfigurations)
        assert val.component == key