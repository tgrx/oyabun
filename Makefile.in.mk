# -----------------------------------------------
# OS-depend actions

ifeq ($(OS), Windows_NT)

define log
	@echo ">>>>>>>>>>>>>>>>    $(1)"
endef

else

define log
	@tput bold 2>/dev/null || exit 0
	@tput setab 0  2>/dev/null || exit 0
	@tput setaf 4  2>/dev/null || exit 0
	@printf %s "#    $(1)    #"
	@tput sgr0  2>/dev/null || exit 0
	@echo ""
endef

endif


# -----------------------------------------------
# independent variables

DIR_REPO := $(realpath ./)
DIR_VENV := $(shell poetry env info --path 2>/dev/null)

# -----------------------------------------------
# OS-depend variables

ifeq ($(OS), Windows_NT)

else

endif


# -----------------------------------------------
# Paths

DIR_ARTIFACTS := $(abspath $(DIR_REPO)/.artifacts)
DIR_OYABUN := $(abspath $(DIR_REPO)/oyabun)
DIR_SAMURAI := $(abspath $(DIR_REPO)/samurai)
DIR_TESTS := $(abspath $(DIR_REPO)/tests)


# -----------------------------------------------
# calculated variables

PYTHON := python
