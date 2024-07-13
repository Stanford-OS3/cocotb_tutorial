# Makefile

# defaults
SIM ?= verilator
TOPLEVEL_LANG ?= verilog
#EXTRA_ARGS += --trace --trace-structs
#export COCOTB_LOG_LEVEL = DEBUG
WAVES = 1
PLUSARGS = --trace 

VERILOG_SOURCES += $(PWD)/ks_add.sv
VERILOG_SOURCES += $(PWD)/pg_0.sv
VERILOG_SOURCES += $(PWD)/pg_1plus.sv


# use VHDL_SOURCES for VHDL files

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = ks_add

# MODULE is the basename of the Python test file
MODULE = ks_add_test

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

# add waveform generation
