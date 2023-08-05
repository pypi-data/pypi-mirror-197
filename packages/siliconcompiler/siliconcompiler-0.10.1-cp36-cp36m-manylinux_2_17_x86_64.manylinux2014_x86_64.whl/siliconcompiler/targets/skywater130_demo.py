import siliconcompiler
from siliconcompiler.targets import utils

from siliconcompiler.pdks import skywater130
from siliconcompiler.flows import asicflow, asictopflow, signoffflow
from siliconcompiler.libs import sky130hd
from siliconcompiler.checklists import oh_tapeout

####################################################
# Target Setup
####################################################

def setup(chip, syn_np=1, floorplan_np=1, physyn_np=1, place_np=1, cts_np=1, route_np=1):
    '''
    Skywater130 Demo Target
    '''

    asic_flow_args = {
        "syn_np": syn_np,
        "floorplan_np": floorplan_np,
        "physyn_np": physyn_np,
        "place_np": place_np,
        "cts_np": cts_np,
        "route_np": route_np
    }

    #1. Load PDK, flow, libs
    chip.use(skywater130)
    chip.use(asicflow, **asic_flow_args)
    chip.use(asictopflow)
    chip.use(signoffflow)
    chip.use(sky130hd)
    chip.use(oh_tapeout)

    #2. Setup default show tools
    utils.set_common_showtools(chip)

    #3. Set default targets
    chip.set('option', 'mode', 'asic')
    chip.set('option', 'flow', 'asicflow', clobber=False)
    chip.set('option', 'pdk', 'skywater130')
    chip.set('option', 'stackup', '5M1LI')

    #4. Set project specific design choices
    chip.set('asic', 'logiclib', 'sky130hd')

    #5. get project specific design choices
    chip.set('asic', 'delaymodel', 'nldm')
    chip.set('constraint', 'density', 10)
    chip.set('constraint', 'coremargin', 4.6)

    #6. Timing corners
    chip.set('constraint', 'timing', 'slow', 'libcorner', 'slow')
    chip.set('constraint', 'timing', 'slow', 'pexcorner', 'maximum')
    chip.set('constraint', 'timing', 'slow', 'mode', 'func')
    chip.set('constraint', 'timing', 'slow', 'check', ['setup', 'hold'])

    chip.set('constraint', 'timing', 'fast', 'libcorner', 'fast')
    chip.set('constraint', 'timing', 'fast', 'pexcorner', 'minimum')
    chip.set('constraint', 'timing', 'fast', 'mode', 'func')
    chip.set('constraint', 'timing', 'fast', 'check', ['setup', 'hold'])

    chip.set('constraint', 'timing', 'typical', 'libcorner', 'typical')
    chip.set('constraint', 'timing', 'typical', 'pexcorner', 'typical')
    chip.set('constraint', 'timing', 'typical', 'mode', 'func')
    chip.set('constraint', 'timing', 'typical', 'check', ['power'])

#########################
if __name__ == "__main__":
    target = siliconcompiler.Chip('<target>')
    setup(target)
    target.write_manifest('skywater130_demo.json')
