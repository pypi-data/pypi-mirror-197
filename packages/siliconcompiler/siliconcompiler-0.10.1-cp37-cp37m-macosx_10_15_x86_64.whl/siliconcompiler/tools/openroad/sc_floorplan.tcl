########################################################
# FLOORPLANNING
########################################################

# Function adapted from OpenROAD:
# https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/ca3004b85e0d4fbee3470115e63b83c498cfed85/flow/scripts/macro_place.tcl#L26
proc design_has_unplaced_macros {} {
  foreach inst [[ord::get_db_block] getInsts] {
    if {[$inst isBlock] && ![$inst isFixed]} {
      return true
    }
  }
  return false
}

proc design_has_unplaced_ios {} {
  foreach inst [[ord::get_db_block] getInsts] {
    if {[$inst isPad] && ![$inst isFixed]} {
      return true
    }
  }
  return false
}

###########################
# Setup Global Connections
###########################

if { [dict exists $sc_cfg tool $sc_tool task $sc_task {file} global_connect] } {
  foreach global_connect [dict get $sc_cfg tool $sc_tool task $sc_task {file} global_connect] {
    puts "Sourcing global connect configuration: ${global_connect}"
    source $global_connect
  }
}

###########################
# Initialize floorplan
###########################

if {[dict exists $sc_cfg input asic floorplan]} {
  set def [lindex [dict get $sc_cfg input asic floorplan] 0]
  puts "Reading floorplan DEF: ${def}"
  read_def -floorplan_initialize $def
} else {
  #NOTE: assuming a two tuple value as lower left, upper right
  set sc_diearea   [dict get $sc_cfg constraint outline]
  set sc_corearea  [dict get $sc_cfg constraint corearea]
  if {$sc_diearea != "" && $sc_corearea != ""} {
    # Use die and core sizes
    set sc_diesize  "[lindex $sc_diearea 0] [lindex $sc_diearea 1]"
    set sc_coresize "[lindex $sc_corearea 0] [lindex $sc_corearea 1]"

    initialize_floorplan -die_area $sc_diesize \
      -core_area $sc_coresize \
      -site $sc_site
  } else {
    # Use density
    initialize_floorplan -aspect_ratio [dict get $sc_cfg constraint aspectratio] \
      -utilization [dict get $sc_cfg constraint density] \
      -core_space [dict get $sc_cfg constraint coremargin] \
      -site $sc_site
  }
}

###########################
# Track Creation
###########################

# source tracks from file if found, else else use schema entries
if {[dict exists $sc_cfg library $sc_mainlib option file openroad_tracks]} {
  set tracks_file [lindex [dict get $sc_cfg library $sc_mainlib option file openroad_tracks] 0]
  puts "Sourcing tracks configuration: ${tracks_file}"
  source $tracks_file
} else {
  make_tracks
}

set do_automatic_pins 1
if { [dict exists $sc_cfg tool $sc_tool task $sc_task file padring] && \
     [llength [dict get $sc_cfg tool $sc_tool task $sc_task file padring]] > 0 } {
  set do_automatic_pins 0

  ###########################
  # Generate pad ring
  ###########################
  set padring_file [lindex [dict get $sc_cfg tool $sc_tool task $sc_task {file} padring] 0]
  puts "Sourcing padring configuration: ${padring_file}"
  source $padring_file

  if { [design_has_unplaced_ios] } {
    foreach inst [[ord::get_db_block] getInsts] {
      if {[$inst isPad] && ![$inst isFixed]} {
        utl::warn FLW 1 "[$inst getName] has not been placed"
      }
    }
    utl::error FLW 1 "Design contains unplaced IOs"
  }
}

###########################
# Pin placement
###########################

# Build pin ordering if specified
set pin_order [dict create 1 [dict create] 2 [dict create] 3 [dict create] 4 [dict create]]
set pin_placement [list ]
if {[dict exists $sc_cfg constraint pin]} {
  dict for {name params} [dict get $sc_cfg constraint pin] {
    set order [dict get $params order]
    set side  [dict get $params side]
    set place [dict get $params placement]

    if { [llength $place] != 0 } {
      # Pin has placement information

      if { [llength $order] != 0 } {
        # Pin also has order information
        utl::error FLW 1 "Pin $name has placement specified in constraints, but also order."
      }
      lappend pin_placement $name
    } else {
      # Pin doesn't have placement

      if { [llength $side] == 0 || [llength $order] == 0 } {
        # Pin information is incomplete

        utl::error FLW 1 "Pin $name doesn't have enough information to perform placement."
      }

      dict lappend pin_order [lindex $side 0] [lindex $order 0] $name
    }
  }
}

foreach pin $pin_placement {
  set params [dict get $sc_cfg constraint pin $pin]
  set layer  [dict get $params layer]
  set side   [dict get $params side]
  set place  [dict get $params placement]
  if { [llength $layer] != 0 } {
    set layer [sc_get_layer_name [lindex $layer 0]]
  } elseif { [llength $side] != 0 } {
    # Layer not set, but side is, so use that to determine layer
    set side [lindex $side 0]
    switch -regexp $side {
      "1|3" {
        set layer [lindex $sc_hpinmetal 0]
      }
      "2|4" {
        set layer [lindex $sc_vpinmetal 0]
      }
      default {
        utl::error FLW 1 "Side number ($side) is not supported."
      }
    }
  } else {
    utl::error FLW 1 "$name needs to either specify side or layer parameter."
  }

  set x_loc [lindex $place 0]
  set y_loc [lindex $place 1]

  place_pin -pin_name $name \
    -layer $layer \
    -location "$x_loc $y_loc" \
    -force_to_die_boundary
}

dict for {side pins} $pin_order {
  if { [dict size $pins] == 0 } {
    continue
  }
  set ordered_pins []
  dict for {index pin} $pins {
    lappend ordered_pins {*}$pin
  }

  set layer  [dict get $params layer]
  if { [llength $layer] != 0 } {
    set layer [sc_get_layer_name [lindex $layer 0]]
  } elseif { [llength $side] != 0 } {
    # Layer not set, but side is, so use that to determine layer
    switch -regexp $side {
      "1|3" {
        set layer [lindex $sc_hpinmetal 0]
      }
      "2|4" {
        set layer [lindex $sc_vpinmetal 0]
      }
      default {
        utl::error FLW 1 "Side number ($side) is not supported."
      }
    }
  } else {
    utl::error FLW 1 "$name needs to either specify side or layer parameter."
  }

  set edge_length 0
  switch -regexp $side {
    "1|3" {
      set edge_length [expr [lindex [ord::get_die_area] 3] - [lindex [ord::get_die_area] 1]]
    }
    "2|4" {
      set edge_length [expr [lindex [ord::get_die_area] 2] - [lindex [ord::get_die_area] 0]]
    }
    default {
      utl::error FLW 1 "Side number ($side) is not supported."
    }
  }

  set spacing [expr $edge_length / ([llength $ordered_pins] + 1)]

  for {set i 0} { $i < [llength $ordered_pins] } { incr i } {
    set name [lindex $ordered_pins $i]
    switch -regexp $side {
      "1" {
        set x_loc [lindex [ord::get_die_area] 1]
        set y_loc [expr ($i + 1) * $spacing]
      }
      "2" {
        set x_loc [expr ($i + 1) * $spacing]
        set y_loc [lindex [ord::get_die_area] 3]
      }
      "3" {
        set x_loc [lindex [ord::get_die_area] 2]
        set y_loc [expr ($i + 1) * $spacing]
      }
      "4" {
        set x_loc [expr ($i + 1) * $spacing]
        set y_loc [lindex [ord::get_die_area] 1]
      }
      default {
        utl::error FLW 1 "Side number ($side) is not supported."
      }
    }

    place_pin -pin_name $name \
      -layer $layer \
      -location "$x_loc $y_loc" \
      -force_to_die_boundary
  }
}

###########################
# Macro placement
###########################

# If manual macro placement is provided use that first
if {[dict exists $sc_cfg constraint component]} {
  dict for {name params} [dict get $sc_cfg constraint component] {
    set location [dict get $params placement]
    set rotation [dict get $params rotation]
    set flip     [dict get $params flip]
    if { [dict exists $params partname] } {
      set cell   [dict get $params partname]
    } else {
      set cell ""
    }
    if { [dict exists $params halo] } {
      utl::warn FLW 1 "Halo is not supported in OpenROAD"
    }

    set transform_r [odb::dbTransform]
    $transform_r setOrient "R${rotation}"
    set transform_f [odb::dbTransform]
    if { $flip == "true" } {
      $transform_f setOrient [odb::dbTransform "MY"]
    }
    set transform_final [odb::dbTransform]
    odb::dbTransform_concat $transform_r $transform_f $transform_final

    set inst [[ord::get_db_block] findInst $name]
    if { $inst == "NULL" } {
      utl::error FLW 1 "Could not find instance: $name"
    }
    set master [$inst getMaster]
    set height [ord::dbu_to_microns [$master getHeight]]
    set width [ord::dbu_to_microns [$master getWidth]]

    # TODO: determine snapping method and apply
    set x_loc [expr [lindex $location 0] - $width / 2]
    set y_loc [expr [lindex $location 1] - $height / 2]

    set place_args []
    if { $cell != "" } {
      lappend place_args "-cell" $cell
    }

    place_cell -inst_name $name \
      -origin "$x_loc $y_loc" \
      -orient [$transform_final getOrient] \
      -status FIRM \
      {*}$place_args
  }
}

if { $do_automatic_pins } {
  ###########################
  # Automatic Pin Placement
  ###########################

  if {[dict exists $sc_cfg tool $sc_tool task $sc_task var pin_thickness_h]} {
    set h_mult [lindex [dict get $sc_cfg tool $sc_tool task $sc_task var pin_thickness_h] 0]
    set_pin_thick_multiplier -hor_multiplier $h_mult
  }
  if {[dict exists $sc_cfg tool $sc_tool task $sc_task var pin_thickness_v]} {
    set v_mult [lindex [dict get $sc_cfg tool $sc_tool task $sc_task var pin_thickness_v] 0]
    set_pin_thick_multiplier -ver_multiplier $v_mult
  }
  if {[dict exists $sc_cfg tool $sc_tool task $sc_task {file} ppl_constraints]} {
    foreach pin_constraint [dict get $sc_cfg tool $sc_tool task $sc_task {file} ppl_constraints] {
      puts "Sourcing pin constraints: ${pin_constraint}"
      source $pin_constraint
    }
  }
  place_pins -hor_layers $sc_hpinmetal \
    -ver_layers $sc_vpinmetal \
    -random
}

# Need to check if we have any macros before performing macro placement,
# since we get an error otherwise.
if {[design_has_unplaced_macros]} {
  ###########################
  # TDMS Placement
  ###########################

  global_placement -density $openroad_gpl_place_density \
    -pad_left $openroad_gpl_padding \
    -pad_right $openroad_gpl_padding

  ###########################
  # Macro placement
  ###########################

  macro_placement -halo $openroad_mpl_macro_place_halo \
    -channel $openroad_mpl_macro_place_channel

  # Note: some platforms set a "macro blockage halo" at this point, but the
  # technologies we support do not, so we don't include that step for now.
}
if { [design_has_unplaced_macros] } {
  utl::error FLW 1 "Design contains unplaced macros."
}

###########################
# Insert tie cells
###########################

foreach tie_type "high low" {
  if {[has_tie_cell $tie_type]} {
    insert_tiecells [get_tie_cell $tie_type]
  }
}
global_connect

###########################
# Tap Cells
###########################

if { [dict exists $sc_cfg tool $sc_tool task $sc_task {file} ifp_tapcell] } {
  set tapcell_file [lindex [dict get $sc_cfg tool $sc_tool task $sc_task {file} ifp_tapcell] 0]
  puts "Sourcing tapcell file: ${tapcell_file}"
  source $tapcell_file
  global_connect
}

###########################
# Power Network
###########################

if {$openroad_pdn_enable == "true" && \
    [dict exists $sc_cfg tool $sc_tool task $sc_task {file} pdn_config]} {
  foreach pdnconfig [dict get $sc_cfg tool $sc_tool task $sc_task {file} pdn_config] {
    puts "Sourcing PDNGEN configuration: ${pdnconfig}"
    source $pdnconfig
  }
  pdngen -failed_via_report "reports/${sc_design}_pdngen_failed_vias.rpt"
}

###########################
# Check Power Network
###########################

foreach net [[ord::get_db_block] getNets] {
  set type [$net getSigType]
  if {$type == "POWER" || $type == "GROUND"} {
    set net_name [$net getName]
    if { ![$net isSpecial] } {
      utl::warn FLW 1 "$net_name is marked as a supply net, but is not marked as a special net"
    }
    if { $openroad_psm_enable == "true" } {
      puts "Check supply net: $net_name"
      check_power_grid -net $net_name
    }
  }
}

###########################
# Remove buffers inserted by synthesis
###########################

remove_buffers
