# Write LEF
write_abstract_lef "outputs/${sc_design}.lef"

if { [lindex [dict get $sc_cfg tool $sc_tool task $sc_task {var} write_cdl] 0] == "true" } {
  # Write CDL
  set sc_cdl_masters []
  foreach lib "$sc_targetlibs $sc_macrolibs" {
    #CDL files
    if {[dict exists $sc_cfg library $lib output $sc_stackup cdl]} {
      foreach cdl_file [dict get $sc_cfg library $lib output $sc_stackup cdl] {
        lappend sc_cdl_masters $cdl_file
      }
    }
  }
  write_cdl -masters $sc_cdl_masters "outputs/${sc_design}.cdl"
}

# generate SPEF
# just need to define a corner
define_process_corner -ext_model_index 0 X
foreach pexcorner $sc_pex_corners {
  set sc_pextool "${sc_tool}-openrcx"
  set pex_model [lindex [dict get $sc_cfg pdk $sc_pdk pexmodel $sc_pextool $sc_stackup $pexcorner] 0]
  extract_parasitics -ext_model_file $pex_model
  write_spef "outputs/${sc_design}.${pexcorner}.spef"
}

set lib_pex [dict create]
foreach scenario $sc_scenarios {
  set libcorner [dict get $sc_cfg constraint timing $scenario libcorner]
  set pexcorner [dict get $sc_cfg constraint timing $scenario pexcorner]

  dict set lib_pex $libcorner $pexcorner
}

# read in spef for timing corners
foreach corner $sc_corners {
  set pexcorner [dict get $lib_pex $corner]
  read_spef -corner $corner \
    "outputs/${sc_design}.${pexcorner}.spef"
}

# Write timing models
foreach corner $sc_corners {
  write_timing_model -library_name "${sc_design}_${corner}" \
    -corner $corner \
    "outputs/${sc_design}.${corner}.lib"
}
