from siliconcompiler.tools.klayout import klayout
from siliconcompiler.tools.klayout.klayout import setup as setup_tool

def make_docs(chip):
    klayout.make_docs(chip)
    chip.set('tool', 'klayout', 'task', 'show', 'var', 'show_filepath', '<path>')

def general_gui_setup(chip, task, exit):
    # Generic tool setup.
    setup_tool(chip)

    tool = 'klayout'
    step = chip.get('arg','step')
    index = chip.get('arg','index')
    clobber = False

    script = 'klayout_show.py'
    chip.set('tool', tool, 'task', task, 'script', script, step=step, index=index, clobber=clobber)

    pdk = chip.get('option', 'pdk')
    stackup = chip.get('option', 'stackup')
    if chip.valid('pdk', pdk, 'var', 'klayout', 'hide_layers', stackup):
        layers_to_hide = chip.get('pdk', pdk, 'var', 'klayout', 'hide_layers', stackup)
        chip.add('tool', tool, 'task', task, 'var', 'hide_layers', layers_to_hide, step=step, index=index)
    if chip.valid('tool', tool, 'task', task, 'var', 'show_filepath'):
        chip.add('tool', tool, 'task', task, 'require', ",".join(['tool', tool, 'task', task, 'var', 'show_filepath']), step=step, index=index)
    else:
        incoming_ext = find_incoming_ext(chip)
        chip.add('tool', tool, 'task', task, 'require', ",".join(['tool', tool, 'task', task, 'var', 'show_filetype']), step=step, index=index)
        chip.set('tool', tool, 'task', task, 'var', 'show_filetype', incoming_ext, step=step, index=index)
        chip.add('tool', tool, 'task', task, 'input', f'{chip.design}.{incoming_ext}', step=step, index=index)

    chip.set('tool', tool, 'task', task, 'var', 'show_exit', "true" if exit else "false", step=step, index=index, clobber=False)

    ## Help
    chip.set('tool', tool, 'task', task, 'var', 'hide_layers', 'List of layers to hide', field='help')
    chip.set('tool', tool, 'task', task, 'var', 'show_filepath', 'File to open', field='help')
    chip.set('tool', tool, 'task', task, 'var', 'show_filetype', 'File type to look for in the inputs', field='help')
    chip.set('tool', tool, 'task', task, 'var', 'show_exit', 'true/false: true will cause kLayout to exit when complete', field='help')

def setup(chip):
    '''
    Show a layout in kLayout
    '''

    # Generic tool setup.
    setup_tool(chip)

    task = 'show'
    general_gui_setup(chip, task, False)

    tool = 'klayout'
    step = chip.get('arg','step')
    index = chip.get('arg','index')
    clobber = False

    option = ['-nc', '-rm']
    chip.set('tool', tool, 'task', task, 'option', option, step=step, index=index, clobber=clobber)

###############

def find_incoming_ext(chip):

    step = chip.get('arg', 'step')
    index = chip.get('arg', 'index')
    flow = chip.get('option', 'flow')

    supported_ext = ('gds', 'oas', 'def')

    for input_step, input_index in chip.get('flowgraph', flow, step, index, 'input'):
        for ext in supported_ext:
            show_file = chip.find_result(ext, step=input_step, index=input_index)
            if show_file:
                return ext

    # Nothing found, just add last one
    return supported_ext[-1]
