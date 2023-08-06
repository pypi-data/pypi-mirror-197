#!/usr/bin/make -f

# SPDX-FileCopyrightText: 2023, Metify, Inc. <metify@metify.io>
# SPDX-License-Identifier: BSD-3-Clause

PYTHON_VERSION ?= 3.9
PYTHON := python$(PYTHON_VERSION)

VIRTUAL_ENV_PATH ?= $(PWD)/.venv
VIRTUAL_ENV_EXPORTS ?= VIRTUAL_ENV=$(VIRTUAL_ENV_PATH) PATH=$(VIRTUAL_ENV_PATH)/bin:$(PATH)

VIRTUAL_ENV_PYTHON := $(VIRTUAL_ENV_EXPORTS) $(PYTHON)
VIRTUAL_ENV_PYTHON_M_PIP := $(VIRTUAL_ENV_EXPORTS) $(PYTHON) -m pip
VIRTUAL_ENV_PYTHON_M_PIP_TOOLS := $(VIRTUAL_ENV_EXPORTS) $(PYTHON) -m piptools
VIRTUAL_ENV_PYTHON_M_PRE_COMMIT := $(VIRTUAL_ENV_EXPORTS) $(PYTHON) -m pre_commit
VIRTUAL_ENV_PYTHON_M_TOX := $(VIRTUAL_ENV_EXPORTS) $(PYTHON) -m tox
VIRTUAL_ENV_TOML_SORT := $(VIRTUAL_ENV_EXPORTS) toml-sort

all:

noop:

virtual-env: $(VIRTUAL_ENV_PATH)/bin/activate

$(VIRTUAL_ENV_PATH)/bin/activate:
		test -d $(VIRTUAL_ENV_PATH) || $(PYTHON) -m venv $(VIRTUAL_ENV_PATH) --prompt $(notdir $(PWD))

development-upgrade-virtual-env: virtual-env
		$(VIRTUAL_ENV_PYTHON_M_PIP) install --upgrade \
			packaging \
			pip \
			setuptools \
			wheel
		$(VIRTUAL_ENV_PYTHON_M_PIP) install --upgrade \
			pip-tools \
			pre-commit \
			toml-sort

development-install-editable-package: virtual-env
		$(VIRTUAL_ENV_PYTHON_M_PIP) install --upgrade -e ./[dev]

development-install-pre-commit: virtual-env
		$(VIRTUAL_ENV_PYTHON_M_PRE_COMMIT) install

development-upgrade-pre-commit: virtual-env
		$(VIRTUAL_ENV_PYTHON_M_PRE_COMMIT) autoupdate

development: \
	development-upgrade-virtual-env \
	development-install-editable-package \
	development-install-pre-commit \
	development-upgrade-pre-commit \
	noop

pyproject: pyproject.toml

pyproject.toml:
	$(VIRTUAL_ENV_TOML_SORT) \
		--in-place \
		--sort-inline-arrays \
		--sort-inline-tables \
		--sort-table-keys \
		--spaces-indent-inline-array 4 \
		--trailing-comma-inline-array \
		$@

test: development
	$(VIRTUAL_ENV_PYTHON_M_TOX)

.PHONY: \
	development-install-editable-package \
	development-install-pre-commit \
	development-upgrade-pre-commit \
	development-upgrade-virtual-env \
	metify.code-workspace \
	pyproject.toml \
	test \
	noop
