# KLayout script to export a .GDS file from a .DEF-formatted design.
#
# Source: The OpenROAD Project.
# https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/flow/util/def2stream.py
#
# License: BSD 3-Clause.
#
#Copyright (c) 2018, The Regents of the University of California
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#* Redistributions of source code must retain the above copyright notice, this
#  list of conditions and the following disclaimer.
#
#* Redistributions in binary form must reproduce the above copyright notice,
#  this list of conditions and the following disclaimer in the documentation
#  and/or other materials provided with the distribution.
#
#* Neither the name of the copyright holder nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pya
import re
import json
import copy
import os
import sys

# SC_ROOT provided by CLI
sys.path.append(SC_ROOT)

from schema import Schema
from tools.klayout.klayout_show import show

def gds_export(design_name, in_def, in_files, out_file, tech_file, foundry_lefs,
              macro_lefs, config_file='', seal_file='', timestamps=True):
  # Expand layers in json
  def expand_cfg_layers(cfg):
    layers = cfg['layers']
    expand = [layer for layer in layers if 'layers' in layers[layer]]
    for layer in expand:
      for i, (name, num) in enumerate(zip(layers[layer]['names'],
                                          layers[layer]['layers'])):
        new_layer = copy.deepcopy(layers[layer])
        del new_layer['names']
        new_layer['name'] = name
        del new_layer['layers']
        new_layer['layer'] = num
        layers[name] = new_layer
      del layers[layer]

  def read_cfg():
    print('INFO: Reading config file: ' + config_file)
    with open(config_file, 'r') as f:
      cfg = json.load(f)

    expand_cfg_layers(cfg)
    cfg = cfg['layers'] # ignore the rest

    # Map gds layers & datatype to KLayout indices
    # These are arrays for the different mask numbers
    for layer, vals in cfg.items():
      layer = vals['layer']
      for key in ('opc', 'non-opc'):
        if key not in vals:
          continue
        data = vals[key]
        if isinstance(data['datatype'], int):
          data['datatype'] = [data['datatype']] # convert to array
        data['klayout'] = [main_layout.find_layer(layer, datatype)
                          for datatype in data['datatype']]

    return cfg

  #match a line like:
  # - LAYER M2 + MASK 2 + OPC RECT ( 3000 3000 ) ( 5000 5000 ) ;
  rect_pat = re.compile(r'''
    \s*\-\ LAYER\ (?P<layer>\S+)  # The layer name
    (?:                           # Non-capturing group
    \s+\+\ MASK\ (?P<mask>\d+)    # Mask, None if absent
    )?
    (?P<opc>                      # OPC, None if absent
    \s+\+\ OPC
    )?
    \s+RECT\
    \(\ (?P<xlo>\d+)\ (?P<ylo>\d+)\ \)\   # rect lower-left pt
    \(\ (?P<xhi>\d+)\ (?P<yhi>\d+)\ \)\ ; # rect upper-right pt
    ''',
                        re.VERBOSE)

  def read_fills(top):
    if config_file == '':
      print('WARNING: no fill config file specified')
      return
    # KLayout doesn't support FILL in DEF so we have to side load them :(
    cfg = read_cfg()
    in_fills = False
    units = None
    with open(in_def) as fp:
      for line in fp:
        if in_fills:
          if re.match('END FILLS', line):
            break # done with fills; don't care what follows
          m = re.match(rect_pat, line)
          if not m:
            raise Exception('Unrecognized fill: ' + line)
          opc_type = 'opc' if m.group('opc') else 'non-opc'
          mask = m.group('mask')
          if not mask: #uncolored just uses first entry
            mask = 0
          else:
            mask = int(mask) - 1 # DEF is 1-based indexing
          layer = cfg[m.group('layer')][opc_type]['klayout'][mask]
          xlo = int(m.group('xlo')) / units
          ylo = int(m.group('ylo')) / units
          xhi = int(m.group('xhi')) / units
          yhi = int(m.group('yhi')) / units
          top.shapes(layer).insert(pya.DBox(xlo, ylo, xhi, yhi))
        elif re.match('FILLS \d+ ;', line):
          in_fills = True
        elif not units:
          m = re.match('UNITS DISTANCE MICRONS (\d+)', line)
          if m:
            units = float(m.group(1))

  # Load technology file
  tech = pya.Technology()
  tech.load(tech_file)
  layoutOptions = tech.load_layout_options
  layoutOptions.lefdef_config.macro_resolution_mode = 1
  pathed_files = set()
  for fn in layoutOptions.lefdef_config.lef_files:
    if fn[0:2] == './':
      pathed_files.add(foundry_lefs + fn[1:])
    else:
      pathed_files.add(fn)

  for lef in macro_lefs:
    pathed_files.add(lef)

  layoutOptions.lefdef_config.lef_files = list(pathed_files)
  layoutOptions.lefdef_config.read_lef_with_def = False

  # Load def file
  main_layout = pya.Layout()
  main_layout.read(in_def, layoutOptions)

  # Clear cells
  top_cell_index = main_layout.cell(design_name).cell_index()

  print("[INFO] Clearing cells...")
  for i in main_layout.each_cell():
    if i.cell_index() != top_cell_index:
      if not i.name.startswith("VIA"):
        i.clear()

  # Load in the gds to merge
  print("[INFO] Merging GDS/OAS files...")
  for fil in in_files:
    print("\t{0}".format(fil))
    main_layout.read(fil)

  # Copy the top level only to a new layout
  print("[INFO] Copying toplevel cell '{0}'".format(design_name))
  top_only_layout = pya.Layout()
  top_only_layout.dbu = main_layout.dbu
  top = top_only_layout.create_cell(design_name)
  top.copy_tree(main_layout.cell(design_name))

  read_fills(top)

  print("[INFO] Checking for missing GDS/OAS...")
  missing_cell = False
  for i in top_only_layout.each_cell():
    if i.is_empty():
      missing_cell = True
      print("[ERROR] LEF Cell '{0}' has no matching GDS/OAS cell. Cell will be empty".format(i.name))

  if not missing_cell:
    print("[INFO] All LEF cells have matching GDS/OAS cells")

  print("[INFO] Checking for orphan cell in the final layout...")
  orphan_cell = False
  for i in top_only_layout.each_cell():
    if i.name != design_name and i.parent_cells() == 0:
      orphan_cell = True
      print("[ERROR] Found orphan cell '{0}'".format(i.name))
      errors += 1

  if seal_file:

    top_cell = top_only_layout.top_cell()

    print("[INFO] Reading seal GDS/OAS file...")
    print("\t{0}".format(seal_file))
    top_only_layout.read(seal_file)

    for cell in top_only_layout.top_cells():
      if cell != top_cell:
        print("[INFO] Merging '{0}' as child of '{1}'".format(cell.name, top_cell.name))
        top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans()))

  # Write out the GDS
  print("[INFO] Writing out GDS/OAS '{0}'".format(out_file))
  write_options = pya.SaveLayoutOptions()
  write_options.gds2_write_timestamps = timestamps
  top_only_layout.write(out_file, write_options)

schema = Schema(manifest='sc_manifest.json')

# Extract info from manifest
sc_step = schema.get('arg', 'step')
sc_index = schema.get('arg', 'index')
sc_pdk = schema.get('option', 'pdk')

sc_stackup = schema.get('pdk', sc_pdk, 'stackup')[0]
sc_mainlib = schema.get('asic', 'logiclib', step=sc_step, index=sc_index)[0]

tech_file = schema.get('pdk', sc_pdk, 'layermap', 'klayout', 'def', 'gds', sc_stackup)[0]

design = schema.get('option', 'entrypoint')
if not design:
    design = schema.get('design')

if schema.valid('input', 'layout', 'def') and schema.get('input', 'layout', 'def', step=sc_step, index=sc_index):
  in_def = schema.get('input', 'layout', 'def', step=sc_step, index=sc_index)[0]
else:
  in_def = os.path.join('inputs', f'{design}.def')
out_gds = os.path.join('outputs', f'{design}.gds')

libs = schema.get('asic', 'logiclib', step=sc_step, index=sc_index)
if 'macrolib' in schema.getkeys('asic'):
  libs += schema.get('asic', 'macrolib', step=sc_step, index=sc_index)

in_gds = []
for lib in libs:
  in_gds.extend(schema.get('library', lib, 'output', sc_stackup, 'gds', step=sc_step, index=sc_index))

foundry_lef = os.path.dirname(schema.get('library', sc_mainlib, 'output', sc_stackup, 'lef', step=sc_step, index=sc_index)[0])

macro_lefs = []
if 'macrolib' in schema.getkeys('asic'):
  for lib in schema.get('asic', 'macrolib', step=sc_step, index=sc_index):
    macro_lefs.extend(schema.get('library', lib, 'output', sc_stackup, 'lef', step=sc_step, index=sc_index))

flow = schema.get('option', 'flow')

sc_task = schema.get('flowgraph', flow, sc_step, sc_index, 'task')

sc_klayout_vars = schema.getkeys('tool', 'klayout', 'task', sc_task, 'var')
if 'timestamps' in sc_klayout_vars:
  sc_timestamps = schema.get('tool', 'klayout', 'task', sc_task, 'var', 'timestamps', step=sc_step, index=sc_index) == ['true']
else:
  sc_timestamps = False

if 'screenshot' in sc_klayout_vars:
  sc_screenshot = schema.get('tool', 'klayout', 'task', sc_task, 'var', 'screenshot', step=sc_step, index=sc_index) == ['true']
else:
  sc_screenshot = True

gds_export(design, in_def, in_gds, out_gds, tech_file, foundry_lef, macro_lefs,
           config_file='', seal_file='', timestamps=sc_timestamps)

if sc_screenshot:
  show(schema, out_gds, f'outputs/{design}.png', screenshot=True)
