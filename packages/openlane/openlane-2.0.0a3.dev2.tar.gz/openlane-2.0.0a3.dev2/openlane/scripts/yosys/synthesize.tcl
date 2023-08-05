# Copyright 2020-2023 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
yosys -import

# inputs expected as env vars
set buffering $::env(SYNTH_BUFFERING)
set sizing $::env(SYNTH_SIZING)
set vtop $::env(DESIGN_NAME)
set sclib $::env(LIB_SYNTH)
if {[info exists ::env(DFF_LIB_SYNTH)]} {
    set dfflib $::env(DFF_LIB_SYNTH)
} else {
    set dfflib $sclib
}

if { [info exists ::env(SYNTH_DEFINES) ] } {
    foreach define $::env(SYNTH_DEFINES) {
        log "Defining $define"
        verilog_defines -D$define
    }
}

set vIdirsArgs ""
if {[info exist ::env(VERILOG_INCLUDE_DIRS)]} {
    foreach dir $::env(VERILOG_INCLUDE_DIRS) {
        lappend vIdirsArgs "-I$dir"
    }
    set vIdirsArgs [join $vIdirsArgs]
}

if { $::env(SYNTH_READ_BLACKBOX_LIB) } {
    log "Reading $::env(LIB_SYNTH) as a blackbox"
    foreach lib $::env(LIB_SYNTH) {
        read_liberty -lib -ignore_miss_dir -setattr blackbox $lib
    }
}

if { [info exists ::env(EXTRA_LIBS) ] } {
    foreach lib $::env(EXTRA_LIBS) {
        read_liberty -lib -ignore_miss_dir -setattr blackbox $lib
    }
}

if { [info exists ::env(EXTRA_VERILOG_MODELS)] } {
    foreach verilog_file $::env(EXTRA_VERILOG_MODELS) {
        read_verilog -sv -lib {*}$vIdirsArgs $verilog_file
    }
}


# ns expected (in sdc as well)
set clock_period [expr {$::env(CLOCK_PERIOD)*1000}]

set driver  $::env(SYNTH_DRIVING_CELL)
set cload   $::env(SYNTH_CAP_LOAD)
# input pin cap of IN_3VX8
set max_FO $::env(MAX_FANOUT_CONSTRAINT)
if {![info exist ::env(MAX_TRANSITION_CONSTRAINT)]} {
    set ::env(MAX_TRANSITION_CONSTRAINT) [expr {0.1*$clock_period}]
} else {
    set ::env(MAX_TRANSITION_CONSTRAINT) [expr {$::env(MAX_TRANSITION_CONSTRAINT) * 1000}]
}
set max_Tran $::env(MAX_TRANSITION_CONSTRAINT)


# Mapping parameters
set A_factor  0.00
set B_factor  0.88
set F_factor  0.00

# Don't change these unless you know what you are doing
set stat_ext    ".stat.rpt"
set chk_ext    ".chk.rpt"
set gl_ext      ".gl.v"
set constr_ext  ".$clock_period.constr"
set timing_ext  ".timing.txt"
set abc_ext     ".abc"


# Create SDC File
set sdc_file $::env(STEP_DIR)/synthesis.sdc
set outfile [open ${sdc_file} w]
puts $outfile "set_driving_cell ${driver}"
puts $outfile "set_load ${cload}"
close $outfile


# Assemble Scripts (By Strategy)
set abc_rs_K    "resub,-K,"
set abc_rs      "resub"
set abc_rsz     "resub,-z"
set abc_rw_K    "rewrite,-K,"
set abc_rw      "rewrite"
set abc_rwz     "rewrite,-z"
set abc_rf      "refactor"
set abc_rfz     "refactor,-z"
set abc_b       "balance"

set abc_resyn2        "${abc_b}; ${abc_rw}; ${abc_rf}; ${abc_b}; ${abc_rw}; ${abc_rwz}; ${abc_b}; ${abc_rfz}; ${abc_rwz}; ${abc_b}"
set abc_share         "strash; multi,-m; ${abc_resyn2}"
set abc_resyn2a       "${abc_b};${abc_rw};${abc_b};${abc_rw};${abc_rwz};${abc_b};${abc_rwz};${abc_b}"
set abc_resyn3        "balance;resub;resub,-K,6;balance;resub,-z;resub,-z,-K,6;balance;resub,-z,-K,5;balance"
set abc_resyn2rs      "${abc_b};${abc_rs_K},6;${abc_rw};${abc_rs_K},6,-N,2;${abc_rf};${abc_rs_K},8;${abc_rw};${abc_rs_K},10;${abc_rwz};${abc_rs_K},10,-N,2;${abc_b},${abc_rs_K},12;${abc_rfz};${abc_rs_K},12,-N,2;${abc_rwz};${abc_b}"

set abc_choice        "fraig_store; ${abc_resyn2}; fraig_store; ${abc_resyn2}; fraig_store; fraig_restore"
set abc_choice2      "fraig_store; balance; fraig_store; ${abc_resyn2}; fraig_store; ${abc_resyn2}; fraig_store; ${abc_resyn2}; fraig_store; fraig_restore"

set abc_map_old_cnt			"map,-p,-a,-B,0.2,-A,0.9,-M,0"
set abc_map_old_dly         "map,-p,-B,0.2,-A,0.9,-M,0"
set abc_retime_area         "retime,-D,{D},-M,5"
set abc_retime_dly          "retime,-D,{D},-M,6"
set abc_map_new_area        "amap,-m,-Q,0.1,-F,20,-A,20,-C,5000"

set abc_area_recovery_1       "${abc_choice}; map;"
set abc_area_recovery_2       "${abc_choice2}; map;"

set map_old_cnt			    "map,-p,-a,-B,0.2,-A,0.9,-M,0"
set map_old_dly			    "map,-p,-B,0.2,-A,0.9,-M,0"
set abc_retime_area   	"retime,-D,{D},-M,5"
set abc_retime_dly    	"retime,-D,{D},-M,6"
set abc_map_new_area  	"amap,-m,-Q,0.1,-F,20,-A,20,-C,5000"

if {$buffering==1} {
    set abc_fine_tune		"buffer,-N,${max_FO},-S,${max_Tran};upsize,{D};dnsize,{D}"
} elseif {$sizing} {
    set abc_fine_tune       "upsize,{D};dnsize,{D}"
} else {
    set abc_fine_tune       ""
}


set delay_scripts [list \
    "+read_constr,${sdc_file};fx;mfs;strash;refactor;${abc_resyn2};${abc_retime_dly}; scleanup;${abc_map_old_dly};retime,-D,{D};&get,-n;&st;&dch;&nf;&put;${abc_fine_tune};stime,-p;print_stats -m" \
    \
    "+read_constr,${sdc_file};fx;mfs;strash;refactor;${abc_resyn2};${abc_retime_dly}; scleanup;${abc_choice2};${abc_map_old_dly};${abc_area_recovery_2}; retime,-D,{D};&get,-n;&st;&dch;&nf;&put;${abc_fine_tune};stime,-p;print_stats -m" \
    \
    "+read_constr,${sdc_file};fx;mfs;strash;refactor;${abc_resyn2};${abc_retime_dly}; scleanup;${abc_choice};${abc_map_old_dly};${abc_area_recovery_1}; retime,-D,{D};&get,-n;&st;&dch;&nf;&put;${abc_fine_tune};stime,-p;print_stats -m" \
    \
    "+read_constr,${sdc_file};fx;mfs;strash;refactor;${abc_resyn2};${abc_retime_area};scleanup;${abc_choice2};${abc_map_new_area};${abc_choice2};${abc_map_old_dly};retime,-D,{D};&get,-n;&st;&dch;&nf;&put;${abc_fine_tune};stime,-p;print_stats -m" \
    "+read_constr,${sdc_file};&get -n;&st;&dch;&nf;&put;&get -n;&st;&syn2;&if -g -K 6;&synch2;&nf;&put;&get -n;&st;&syn2;&if -g -K 6;&synch2;&nf;&put;&get -n;&st;&syn2;&if -g -K 6;&synch2;&nf;&put;&get -n;&st;&syn2;&if -g -K 6;&synch2;&nf;&put;&get -n;&st;&syn2;&if -g -K 6;&synch2;&nf;&put;buffer -c -N ${max_FO};topo;stime -c;upsize -c;dnsize -c;;stime,-p;print_stats -m" \
]

set area_scripts [list \
    "+read_constr,${sdc_file};fx;mfs;strash;refactor;${abc_resyn2};${abc_retime_area};scleanup;${abc_choice2};${abc_map_new_area};retime,-D,{D};&get,-n;&st;&dch;&nf;&put;${abc_fine_tune};stime,-p;print_stats -m" \
    \
    "+read_constr,${sdc_file};fx;mfs;strash;refactor;${abc_resyn2};${abc_retime_area};scleanup;${abc_choice2};${abc_map_new_area};${abc_choice2};${abc_map_new_area};retime,-D,{D};&get,-n;&st;&dch;&nf;&put;${abc_fine_tune};stime,-p;print_stats -m" \
    \
    "+read_constr,${sdc_file};fx;mfs;strash;refactor;${abc_choice2};${abc_retime_area};scleanup;${abc_choice2};${abc_map_new_area};${abc_choice2};${abc_map_new_area};retime,-D,{D};&get,-n;&st;&dch;&nf;&put;${abc_fine_tune};stime,-p;print_stats -m" \
    "+read_constr,${sdc_file};strash;dch;map -B 0.9;topo;stime -c;buffer -c -N ${max_FO};upsize -c;dnsize -c;stime,-p;print_stats -m" \
]

set all_scripts [list {*}$delay_scripts {*}$area_scripts]

set strategy_parts [split $::env(SYNTH_STRATEGY)]

proc synth_strategy_format_err { } {
    upvar area_scripts area_scripts
    upvar delay_scripts delay_scripts
    log -stderr "\[ERROR] Misformatted SYNTH_STRATEGY (\"$::env(SYNTH_STRATEGY)\")."
    log -stderr "\[ERROR] Correct format is \"DELAY|AREA 0-[expr [llength $delay_scripts]-1]|0-[expr [llength $area_scripts]-1]\"."
    exit 1
}

if { [llength $strategy_parts] != 2 } {
    synth_strategy_format_err
}

set strategy_type [lindex $strategy_parts 0]
set strategy_type_idx [lindex $strategy_parts 1]

if { $strategy_type != "AREA" && $strategy_type != "DELAY" } {
    log -stderr "\[ERROR] AREA|DELAY tokens not found. ($strategy_type)"
    synth_strategy_format_err
}

if { $strategy_type == "DELAY" && $strategy_type_idx >= [llength $delay_scripts] } {
    log -stderr "\[ERROR] strategy index ($strategy_type_idx) is too high."
    synth_strategy_format_err
}

if { $strategy_type == "AREA" && $strategy_type_idx >= [llength $area_scripts] } {
    log -stderr "\[ERROR] strategy index ($strategy_type_idx) is too high."
    synth_strategy_format_err
}

if { $strategy_type == "DELAY" } {
    set strategy_script [lindex $delay_scripts $strategy_type_idx]
    set strategy_name "DELAY $strategy_type_idx"
} else {
    set strategy_script [lindex $area_scripts $strategy_type_idx]
    set strategy_name "AREA $strategy_type_idx"
}

# Get Adder Type
set adder_type $::env(SYNTH_ADDER_TYPE)
if { !($adder_type in [list "YOSYS" "FA" "RCA" "CSA"]) } {
    log -stderr "\[ERROR] Misformatted SYNTH_ADDER_TYPE (\"$::env(SYNTH_ADDER_TYPE)\")."
    log -stderr "\[ERROR] Correct format is \"YOSYS|FA|RCA|CSA\"."
    exit 1
}

# Start Synthesis
for { set i 0 } { $i < [llength $::env(VERILOG_FILES)] } { incr i } {
    read_verilog -sv {*}$vIdirsArgs [lindex $::env(VERILOG_FILES) $i]
}

if { [info exists ::env(SYNTH_PARAMETERS) ] } {
    foreach define $::env(SYNTH_PARAMETERS) {
        set param_and_value [split $define "="]
        lassign $param_and_value param value
        chparam -set $param $value $vtop
    }
}

select -module $vtop
show -format dot -prefix $::env(STEP_DIR)/hierarchy
select -clear

hierarchy -check -top $vtop

# Infer tri-state buffers.
set tbuf_map false
if { [info exists ::env(TRISTATE_BUFFER_MAP)] } {
    if { [file exists $::env(TRISTATE_BUFFER_MAP)] } {
        set tbuf_map true
        tribuf
    } else {
        log "WARNING: TRISTATE_BUFFER_MAP is defined but could not be found: $::env(TRISTATE_BUFFER_MAP)"
    }
}

# Handle technology mapping of RCS/CSA adders
if { $adder_type == "RCA"} {
    if { [info exists ::env(RIPPLE_CARRY_ADDER_MAP)] && [file exists $::env(RIPPLE_CARRY_ADDER_MAP)] } {
        techmap -map $::env(RIPPLE_CARRY_ADDER_MAP)
    }
} elseif { $adder_type == "CSA"} {
    if { [info exists ::env(CARRY_SELECT_ADDER_MAP)] && [file exists $::env(CARRY_SELECT_ADDER_MAP)] } {
        techmap -map $::env(CARRY_SELECT_ADDER_MAP)
    }
}

if { $::env(SYNTH_NO_FLAT) } {
    synth -top $vtop
} else {
    synth -top $vtop -flatten
}

if { [info exists ::env(SYNTH_EXTRA_MAPPING_FILE)] } {
    if { [file exists $::env(SYNTH_EXTRA_MAPPING_FILE)] } {
        log "\[INFO\] applying mappings in $::env(SYNTH_EXTRA_MAPPING_FILE)"
        techmap -map $::env(SYNTH_EXTRA_MAPPING_FILE)
    } else {
        log -stderr "\[ERROR] file not found $::env(SYNTH_EXTRA_MAPPING_FILE)."
    }
}

show -format dot -prefix $::env(STEP_DIR)/post_techmap

if { $::env(SYNTH_SHARE_RESOURCES) } {
    share -aggressive
}

set fa_map false
if { $adder_type == "FA" } {
    if { [info exists ::env(FULL_ADDER_MAP)] && [file exists $::env(FULL_ADDER_MAP)] } {
        extract_fa -fa -v
        extract_fa -ha -v
        set fa_map true
    }
}

opt
opt_clean -purge

set report_dir $::env(STEP_DIR)/reports
file mkdir $report_dir

tee -o "$report_dir/pre_techmap.json" stat -json

# Map tri-state buffers
if { $tbuf_map } {
    log {mapping tbuf}
    techmap -map $::env(TRISTATE_BUFFER_MAP)
    simplemap
}

# Map full adders
if { $fa_map } {
    techmap -map $::env(FULL_ADDER_MAP)
}

# Handle technology mapping of latches
if { [info exists ::env(SYNTH_LATCH_MAP)] && [file exists $::env(SYNTH_LATCH_MAP)] } {
    techmap -map $::env(SYNTH_LATCH_MAP)
    simplemap
}

dfflibmap -liberty $dfflib
tee -o "$report_dir/post_dff.json" stat -json

proc run_strategy {output script strategy_name {postfix_with_strategy 0}} {
    upvar clock_period clock_period
    upvar sdc_file sdc
    upvar sclib lib
    upvar report_dir report_dir

    log "\[INFO\] USING STRATEGY $strategy_name"

    set strategy_escaped [string map {" " _} $strategy_name]

    design -load checkpoint

    abc -D "$clock_period" \
        -constr "$sdc" \
        -liberty "$lib" \
        -script "$script" \
        -showtmp

    setundef -zero

    hilomap -hicell $::env(SYNTH_TIEHI_CELL) -locell $::env(SYNTH_TIELO_CELL)

    splitnets
    opt_clean -purge
    insbuf -buf {*}[split $::env(SYNTH_BUFFER_CELL) "/"]

    tee -o "$report_dir/chk.rpt" check
    tee -o "$report_dir/stat.json" stat -top $::env(DESIGN_NAME) -liberty [lindex $::env(LIB_SYNTH) 0] -json

    if { [info exists ::env(SYNTH_AUTONAME)] && $::env(SYNTH_AUTONAME) } {
        # Generate public names for the various nets, resulting in very long names that include
        # the full heirarchy, which is preferable to the internal names that are simply
        # sequential numbers such as `_000019_`. Renamed net names can be very long, such as:
        #     manual_reset_gf180mcu_fd_sc_mcu7t5v0__dffq_1_Q_D_gf180mcu_ \
        #     fd_sc_mcu7t5v0__nor3_1_ZN_A1_gf180mcu_fd_sc_mcu7t5v0__aoi21_ \
        #     1_A2_A1_gf180mcu_fd_sc_mcu7t5v0__nand3_1_ZN_A3_gf180mcu_fd_ \
        #     sc_mcu7t5v0__and3_1_A3_Z_gf180mcu_fd_sc_mcu7t5v0__buf_1_I_Z
        autoname
    }
    write_verilog -noattr -noexpr -nohex -nodec -defparam $output
    if { $::env(QUIT_ON_SYNTH_CHECKS) == 1 } {
        read_liberty -ignore_miss_func $::env(LIB_SYNTH)
        check -assert $::env(DESIGN_NAME)
    }
    design -reset
}
design -save checkpoint

run_strategy\
    "$::env(SAVE_NETLIST)"\
    "$strategy_script"\
    "$strategy_name"

if { $::env(SYNTH_NO_FLAT) } {
    design -reset

    if { [info exists ::env(SYNTH_DEFINES) ] } {
        foreach define $::env(SYNTH_DEFINES) {
            log "Defining $define"
            verilog_defines -D$define
        }
    }

    foreach lib $::env(LIB_SYNTH_COMPLETE_NO_PG) {
        read_liberty -lib -ignore_miss_dir -setattr blackbox $lib
    }

    if { [info exists ::env(EXTRA_LIBS) ] } {
        foreach lib $::env(EXTRA_LIBS) {
            read_liberty -lib -ignore_miss_dir -setattr blackbox $lib
        }
    }

    if { [info exists ::env(EXTRA_VERILOG_MODELS)] } {
        foreach verilog_file $::env(EXTRA_VERILOG_MODELS) {
            read_verilog -sv -lib {*}$vIdirsArgs $verilog_file
        }
    }

    file copy -force $::env(SAVE_NETLIST) $::env(synthesis_results)/$::env(DESIGN_NAME).hierarchy.nl.v
    read_verilog -sv $::env(SAVE_NETLIST)
    synth -top $vtop -flatten

    design -save checkpoint
    run_strategy\
        "$::env(SAVE_NETLIST)"\
        "$strategy_script"\
        "$strategy_name"
}

