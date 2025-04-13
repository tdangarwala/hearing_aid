# Project Name
TARGET = hearing_aid

# Sources
CPP_SOURCES = hearing_aid.cpp

# CMSIS DSP sources
CMSIS_DSP_SRC_DIR = $(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source
C_SOURCES += $(CMSIS_DSP_SRC_DIR)/FilteringFunctions/arm_fir_init_f32.c
C_SOURCES += $(CMSIS_DSP_SRC_DIR)/FilteringFunctions/arm_fir_f32.c

# Library Locations
LIBDAISY_DIR = ../../libDaisy
DAISYSP_DIR = ../../DaisySP

# Core location, and generic Makefile.
SYSTEM_FILES_DIR = $(LIBDAISY_DIR)/core
include $(SYSTEM_FILES_DIR)/Makefile