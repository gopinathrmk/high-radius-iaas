SHELL := /bin/bash

ifeq ($(OS),Windows_NT)
	VENV_PATH = venv/Scripts
	JQ_BIN = admin_tools/jq/jq-windows-amd64.exe
else
	UNAME_S := $(shell uname -s)
	UNAME_M := $(shell uname -m)
	ifeq ($(UNAME_S),Linux)
		VENV_PATH = venv/bin
		ifeq ($(UNAME_M),arm64)
			JQ_BIN = ./admin_tools/jq/jq-linux-arm64
		else
			JQ_BIN = ./admin_tools/jq/jq-linux-amd64
		endif
	endif
	ifeq ($(UNAME_S),Darwin)
		VENV_PATH = venv/bin
		ifeq ($(UNAME_M),arm64)
			JQ_BIN = ./admin_tools/jq/jq-macos-arm64
		else
			JQ_BIN = ./admin_tools/jq/jq-macos-amd64
		endif
	endif
endif

#### CALM_ENVIRONMENT default is "bwe". To override, pass CALM_ENVIRONMENT for the make call, e.g., make init-dsl-config CALM_ENVIRONMENT=nyc
CALM_ENVIRONMENT ?= bwe

ifneq ($(wildcard ./.local),)
	CALM_DSL_VERSION := $(shell cat .local/calm_dsl_version)
ifneq ($(wildcard ./.local/${CALM_ENVIRONMENT}/${CALM_ENVIRONMENT}-config.json),)
	CALM_PROJECT := $(shell $(JQ_BIN) -r '.calm_config.calm_project_name' ./.local/${CALM_ENVIRONMENT}/${CALM_ENVIRONMENT}-config.json)
	CALM_IP_ADDRESS := $(shell $(JQ_BIN) -r '.calm_config.calm_ip_address' ./.local/${CALM_ENVIRONMENT}/${CALM_ENVIRONMENT}-config.json)
	CALM_USER := $(shell $(JQ_BIN) -r '.calm_config.calm_user' ./.local/${CALM_ENVIRONMENT}/${CALM_ENVIRONMENT}-config.json)
	CALM_PASS := $(shell $(JQ_BIN) -r '.calm_config.calm_password' ./.local/${CALM_ENVIRONMENT}/${CALM_ENVIRONMENT}-config.json)
endif
else
	CALM_DSL_VERSION :=
	CALM_PROJECT :=
	CALM_IP_ADDRESS :=
	CALM_USER :=
	CALM_PASS :=
endif

CALM_PORT := 9440
DSL_INIT_PARAMS := --ip ${CALM_IP_ADDRESS} --port ${CALM_PORT} --username ${CALM_USER} --password ${CALM_PASS}
CALM_DSL_LOCAL_DIR_LOCATION = $(CURDIR)/.local/${CALM_ENVIRONMENT}/
PROJECT_ROOT := $(CURDIR)

#### Color variables used throughout the Makefile.
GREEN =\033[1;32m
YELLOW =\033[1;33m
PURPLE =\033[1;35m
BLUE=\033[1;34m
NOCOLOR =\033[0m

#### Determine if Calm DSL has been installed local cloned repo and VENV is used.
ifneq ($(wildcard ./calm-dsl/.),)
	DSL_VENV = @source calm-dsl/${VENV_PATH}/activate &&
	DSL_VENV_SHELL = source calm-dsl/${VENV_PATH}/activate &&
else
	DSL_VENV =
	DSL_VENV_SHELL =
endif

#### EXPORTING ALL MAKE VARIABLES
export

#### CALM DSL PREREQUISITE TASKS
#### INITIAL DEVELOPER ENVIRONMENT REPO CREATION TASKS
.PHONY: init-calm-config
init-calm-config:  ## Create local configs and secret files to be used in the Calm Environment, e.g. prism central ip, user, pass, etc...
	@echo $$'${GREEN}Asking for information about the Calm-DSL installation, Calm instance to utilize and other blueprint specific items${NOCOLOR}'
	@if [ ! -d calm-dsl ] || [ ! -f .local/calm_dsl_version ]; \
	then ${CALM_DSL_VERSION_SELECTION}; \
	else echo $$'${YELLOW}Calm-DSL seems to be present in the local repo - Installing Calm-DSL as a submodule will not occur.${NOCOLOR}'; \
	echo $$'${YELLOW}Moving on to configure the repository schema.${NOCOLOR}'; \
	fi
	@if [ ! -d .local/$$CALM_ENVIRONMENT ]; \
	then mkdir -p .local/$$CALM_ENVIRONMENT; \
	elif [ -d .local/$$CALM_ENVIRONMENT ]; \
	then rm -rf .local/$$CALM_ENVIRONMENT && mkdir -p .local/$$CALM_ENVIRONMENT; \
	fi
	@make schema-input
	@make init-dsl-config

.PHONY: schema-input
schema-input:
	@make -C config schema-input

.PHONY: install-dsl
install-dsl: ## Install Calm-DSL into the cloned local repo.
	@echo $$'${GREEN}Installing Calm-DSL${NOCOLOR}'
ifneq ($(wildcard ./calm-dsl/.),)
	@echo $$'${YELLOW}The Calm DSL repository seems to be present - Adding the DSL repo as a submodule will not occur${NOCOLOR}'
else
	@echo $$'${GREEN}Cloning the Calm DSL Git repository${NOCOLOR}'
	@echo $$'$(GREEN)'"Calm DSL version selected is $(CALM_DSL_VERSION)" $$'$(NOCOLOR)'
	@git clone --depth 1 --single-branch --branch ${CALM_DSL_VERSION} https://github.com/nutanix/calm-dsl calm-dsl
endif
	if [[ $$(grep -L "cerberus>=1.3.4" calm-dsl/requirements.txt) ]]; \
	then echo "$$DSL_ADDITIONAL_TOOLS" >> calm-dsl/requirements.txt; \
	else echo $$'${GREEN}DSL additional tools are present in the pip requirements file${NOCOLOR}'; \
	fi
ifeq ($(OS),Windows_NT)
	if [[ $$(grep -L "windev:" calm-dsl/Makefile) ]]; \
	then echo "$$DSL_WINDEV" >> calm-dsl/Makefile && echo $$'${GREEN}Configuring Calm DSL${NOCOLOR}' && make -C calm-dsl windev; \
	else echo $$'${GREEN}Configuring Calm DSL${NOCOLOR}' && make -C calm-dsl windev; \
	source calm-dsl/${VENV_PATH}/activate && pip3 install --upgrade requests; \
	fi
endif
ifeq ($(shell uname),$(filter $(shell uname),Darwin Linux))
	echo $$'${GREEN}Configuring the Calm DSL Python Virtual Environment${NOCOLOR}' && make -C calm-dsl dev; \
	source calm-dsl/${VENV_PATH}/activate && pip3 install --upgrade requests
endif

.PHONY: print-make-envs
print-make-envs:  ## Print Make environment variables.
	@echo $$'\n${BLUE}BELOW ARE CURRENT VALUES FOR VARIABLES USED WITHIN THE MAKEFILE ENVIRONMENT.${NOCOLOR}'
	@echo $$'\n${BLUE}PROJECT_ROOT = ${GREEN}$(PROJECT_ROOT)${NOCOLOR}'
	@echo $$'${BLUE}CALM_ENVIRONMENT = ${GREEN}$(CALM_ENVIRONMENT)${NOCOLOR}'
	@echo $$'${BLUE}CALM_USER = ${GREEN}$(CALM_USER)${NOCOLOR}'
	@echo $$'${BLUE}CALM_ADDRESS = ${GREEN}$(CALM_IP_ADDRESS)${NOCOLOR}'
	@echo $$'${BLUE}CALM_PROJECT = ${GREEN}$(CALM_PROJECT)${NOCOLOR}'
	@echo $$'${BLUE}CALM_DSL_VERSION = ${GREEN}$(shell ${DSL_VENV_SHELL} calm --version)${NOCOLOR}'
	@echo $$'${BLUE}MAKE_VERSION = ${GREEN}$(shell make --version | head -n1)${NOCOLOR}'
	@echo $$'${BLUE}PYTHON_VERSION = ${GREEN}$(shell python --version | head -n1)${NOCOLOR}'
	@echo $$'${BLUE}CURRENT_GIT_BRANCH = ${GREEN}$(shell git rev-parse --abbrev-ref HEAD)${NOCOLOR}'
	@echo $$'${BLUE}CURRENT_GIT_COMMIT = ${GREEN}$(shell git rev-parse --short HEAD)${NOCOLOR}'
	@echo $$'${BLUE}CURRENT_GIT_TAG = ${GREEN}$(shell git rev-list --tags --max-count=1 | xargs -I {} git describe --tags {} | tr -d '.' | cut -d- -f1)${NOCOLOR}\n'

.PHONY: init-dsl-config
init-dsl-config: print-make-envs ## Initialize CALM-DSL to the Calm instance and Calm Project.
	@echo $$'${GREEN}Initializing Calm DSL with the Calm instance${NOCOLOR}'
	${DSL_VENV} calm init dsl ${DSL_INIT_PARAMS} --project ${CALM_PROJECT}; \
	calm set config -rt 120; \
	calm get projects -n ${CALM_PROJECT}

#### CREATE BLUEPRINT TASKS
# CALM_ENVIRONMENT default is "bwe".  To override, pass CALM_ENVIRONMENT for the make call, e.g., make create-windows-bp CALM_ENVIRONMENT=nyc
create-all-bps create-windows-bp create-linux-bp create-ndb-bp: init-dsl-config
create-all-bps: create-windows-bp create-linux-bp ## Compile and Create both Windows and Linux blueprints.
create-windows-bp: ## Compile and create the Windows blueprint.
	${DSL_VENV} make -C blueprints/windows create-bp
create-linux-bp: ## Compile and create the Linux blueprint.
	${DSL_VENV}  make -C blueprints/linux create-bp
create-ndb-bp: ## Compile and create the NDB blueprint.
	${DSL_VENV}  make -C blueprints/NDBMySQL create-ndb-bp
create-ndb-restored-bp: ## Compile and create the NDB blueprint.
	${DSL_VENV}  make -C blueprints/NDBMySQL create-ndb-restored-bp
create-ndb-cloned-bp: ## Compile and create the NDB blueprint.
	${DSL_VENV}  make -C blueprints/NDBMySQL create-ndb-cloned-bp

#### COMPILE BLUEPRINT TASKS
compile-windows-bp: ## Compile the Windows Blueprint.
	${DSL_VENV} make -C blueprints/windows compile-bp
compile-linux-bp: ## Compile the Linux Blueprint.
	${DSL_VENV} make -C blueprints/linux compile-bp
compile-ndb-bp: ## Compile the NDB Blueprint.
	${DSL_VENV} make -C blueprints/NDBMySQL compile-bp

compile-ndb-restored-bp: ## Compile the NDB Blueprint.
	${DSL_VENV} make -C blueprints/NDBMySQL-restore compile-bp


test-linux-bp:
	make -C blueprints/linux test-bp

#### LAUNCH BLUEPRINT TASKS
launch-windows-bp:
	${DSL_VENV} make -C blueprints/windows launch-ahv-test-bp
launch-linux-bp:
	${DSL_VENV} make -C blueprints/linux launch-ahv-test-bp

#########################################
#### RELEASE MANAGEMENT
### PROD MASTER BRANCH RELEASE: Create Converged master Branch Blueprints with Git-Tag/SHA-CODE and Publish to Marketplace on each site.
## The following should be run from the master branch along with git tag v1.0.x-$(git rev-parse --short HEAD), git push origin --tags
# If needing to publish from a previous commit/tag than current master HEAD, from master, run git reset --hard tagname to set local working copy to that point in time.
# Run git reset --hard origin/master to return your local working copy back to latest master HEAD.
publish-all-masterbranch-bps: ## Publish all master branch blueprints to marketplace item in bwe.
	make create-all-bps publish-all-current-tag-bps CALM_ENVIRONMENT=${CALM_ENVIRONMENT}
	${DSL_VENV} make -C blueprints/windows unpublish-mp-previous-tag
	${DSL_VENV} make -C blueprints/linux unpublish-mp-previous-tag
publish-windows-masterbranch-bps: ## Publish Windows master branch blueprints to marketplace item in bwe.
	make create-windows-bp publish-windows-current-tag-bp CALM_ENVIRONMENT=${CALM_ENVIRONMENT}
	${DSL_VENV} make -C blueprints/windows unpublish-mp-previous-tag
publish-linux-masterbranch-bps: ## Publish Linux master branch blueprints to marketplace item in bwe.
	make create-linux-bp publish-linux-current-tag-bp CALM_ENVIRONMENT=${CALM_ENVIRONMENT}
	${DSL_VENV} make -C blueprints/linux unpublish-mp-previous-tag

### TEST FEATURE BRANCH RELEASE: Create Converged Feature Branch Blueprints with no Git-Tag and Publish to Marketplace on each site.
publish-all-featurebranch-bps: ## Publish all feature branch blueprints to marketplace item in bwe.
	make create-all-bps publish-all-featurebranch-bps CALM_ENVIRONMENT=${CALM_ENVIRONMENT}
publish-windows-featurebranch-bps: ## Publish Windows feature branch blueprints to marketplace item in bwe.
	make create-windows-bp publish-windows-featurebranch-bp CALM_ENVIRONMENT=${CALM_ENVIRONMENT}
publish-linux-featurebranch-bps: ## Publish Linux feature branch blueprints to marketplace item in bwe.
	make create-linux-bp publish-linux-featurebranch-bp CALM_ENVIRONMENT=${CALM_ENVIRONMENT}

#### PUBLISH BLUEPRINT TASKS
## PUBLISH FEATUREBRANCH BPS
# CALM_ENVIRONMENT default is "bwe".  To override, pass CALM_ENVIRONMENT for the make call, e.g., make publish-windows-featurebranch-bp CALM_ENVIRONMENT=nyc
publish-all-featurebranch-bps publish-windows-featurebranch-bp publish-linux-featurebranch-bp: CALM_TEST_PROJECT_LIST_COMMA = $(shell ${DSL_VENV_SHELL} calm get projects -l 250 -q | grep -E "^$(CALM_PROJECT)" | tr '\n' ',' | sed 's/,$$//')
publish-all-featurebranch-bps: publish-windows-featurebranch-bp publish-linux-featurebranch-bp
publish-windows-featurebranch-bp:
	# publish new version of existing windows test blueprints
	${DSL_VENV} make -C blueprints/windows publish-featurebranch-bp # MARKETPLACE_PRJ_LIST=${CALM_TEST_PROJECT_LIST_COMMA}
publish-linux-featurebranch-bp:
	# publish new version of existing linux test blueprints
	${DSL_VENV} make -C blueprints/linux publish-featurebranch-bp # MARKETPLACE_PRJ_LIST=${CALM_TEST_PROJECT_LIST_COMMA}

## PUBLISH TAGGED MASTER BRANCH BPS
# These targets all require CALM_PROD_PROJECT_LIST_COMMA which is relatively expensive for prod, so it only evals for these targets.
# CALM_ENVIRONMENT default is "bwe".  To override, pass CALM_ENVIRONMENT for the make call, e.g., make publish-windows-current-tag-bp CALM_ENVIRONMENT=nyc
publish-all-current-tag-bps publish-windows-current-tag-bp publish-linux-current-tag-bp: CALM_PROD_PROJECT_LIST_COMMA = $(shell ${DSL_VENV_SHELL} calm get projects -l 250 -q | grep -E "^$(CALM_PROJECT)" | tr '\n' ',' | sed 's/,$$//')
publish-all-current-tag-bps: publish-windows-current-tag-bp publish-linux-current-tag-bp
publish-windows-current-tag-bp:
	# publish new version of existing windows blueprints
	${DSL_VENV} make -C blueprints/windows publish-current-tag-bp # MARKETPLACE_PRJ_LIST=${CALM_PROD_PROJECT_LIST_COMMA}
publish-linux-current-tag-bp:
	# publish new version of existing linux blueprints
	${DSL_VENV} make -C blueprints/linux publish-current-tag-bp # MARKETPLACE_PRJ_LIST=${CALM_PROD_PROJECT_LIST_COMMA}

#### UNPUBLISH BLUEPRINT TASKS
## UNPUBLISH FEATUREBRANCH BPS
unpublish-all-current-featurebranch-bps: unpublish-windows-current-featurebranch-bps unpublish-linux-current-featurebranch-bps
unpublish-windows-current-featurebranch-bps:
	${DSL_VENV} make -C blueprints/windows unpublish-mp-current-commitid delete-mp-current-commitid
unpublish-linux-current-featurebranch-bps:
	${DSL_VENV} make -C blueprints/linux unpublish-mp-current-commitid delete-mp-current-commitid

## UNPUBLISH TAGGED MASTER BRANCH BPS
unpublish-all-current-tag-bps: unpublish-windows-current-tag-bps unpublish-linux-current-tag-bps
unpublish-windows-current-tag-bps:
	${DSL_VENV} make -C blueprints/windows unpublish-mp-current-tag delete-mp-current-tag
unpublish-linux-current-tag-bps:
	${DSL_VENV} make -C blueprints/linux unpublish-mp-current-tag delete-mp-current-tag

#### ENDPOINT TASKS
create-all-endpoints create-windows-ep create-linux-ep: init-dsl-config
create-all-endpoints: create-windows-ep create-linux-ep
create-windows-ep: ## Create a Windows Endpoint.
	# create windows endpoint (stored creds)
	${DSL_VENV} make -C endpoints/windows create-endpoint

create-linux-ep: ## Create a Linux Endpoint.
	# create linux endpoint (stored creds)
	${DSL_VENV} make -C endpoints/linux create-endpoint

delete-all-endpoints delete-windows-ep delete-linux-ep: init-dsl-config
delete-all-endpoints: delete-windows-ep delete-linux-ep

delete-windows-ep: ## Delete a Windows Endpoint.
	# delete windows endpoint
	${DSL_VENV} make -C endpoints/windows delete-endpoint

delete-linux-ep: ## Delete a Linux Endpoint.
	# delete linux endpoint
	${DSL_VENV} make -C endpoints/linux delete-endpoint

#### PRUNING Maintenance Tasks, please use with EXTREME caution!!!!!
## These blocks will query blueprints and delete them based on search criteria.
prune-all-bps-working-commit-test: init-dsl-config
	${DSL_VENV} calm get bps -q --limit 10 -n $(shell git rev-parse --short HEAD)
prune-all-bps-working-commit: init-dsl-config ## This will delete all blueprints (up to 10 at a time) that are associated to the current working COMMMIT_ID of the current COMMIT_BRANCH, regardless of application count.
	${DSL_VENV} calm get bps -q --limit 10 -n $(shell git rev-parse --short HEAD) | xargs -I {} calm delete bp {}
prune-all-bps-working-branch-test: init-dsl-config
	${DSL_VENV} calm get bps -q --limit 10 -n $(shell git rev-parse --abbrev-ref HEAD | head -c15)
prune-all-bps-working-branch: init-dsl-config ## This will delete all blueprints (up to 10 at a time) that are associated to current working COMMIT_BRANCH (not just commit id), regardless of application count.
	${DSL_VENV} calm get bps -q --limit 10 -n $(shell git rev-parse --abbrev-ref HEAD | head -c15) | xargs -I {} calm delete bp {}
prune-all-bps-not-working-commit: init-dsl-config ## BE CAREFUL HERE - This will delete all blueprints (up to 10 at a time) that are NOT associated to current working COMMMIT_ID and COMMIT_BRANCH, regardless of application count.
	${DSL_VENV} calm get bps -q | grep -m 10 $(shell git rev-parse --abbrev-ref HEAD | head -c15) | grep -v $(shell git rev-parse --short HEAD) | cut -d: -f2- | awk '{print $1}' | xargs -I {} calm delete bp {}
prune-all-bps-current-tag-test: init-dsl-config  ## This is a test target for the below target.  It will NOT delete anything.
	${DSL_VENV} calm get bps -q --limit 10 -n $(shell git rev-list --tags --max-count=1 | xargs -I {} git describe --tags {} | tr -d '.' | cut -d- -f1)
prune-all-bps-current-tag: init-dsl-config  ## This will delete all blueprints (up to 10 at a time) that are associated to the current working tag of the current COMMIT_BRANCH, regardless of application count.
	${DSL_VENV} calm get bps -q --limit 10 -n $(shell git rev-list --tags --max-count=1 | xargs -I {} git describe --tags {} | tr -d '.' | cut -d- -f1) | xargs -I {} calm delete bp {}
prune-all-bps-previous-tag-test: init-dsl-config  ## This is a test target for the below target.  It will NOT delete anything.
	${DSL_VENV} calm get bps -q --limit 10 -n $(shell tags=$$(git rev-list --tags --max-count=2 | awk -F'[ ]' '{print $$1}{print $$2}') && tag=$$(echo $$tags | awk -F'[ ]' '{print$$2}' | xargs -I {} git describe --tags {} | awk -F'[-]' '{print$$1}{print$$2}' | tr ' ' '-') && echo $$tag | tr ' ' '-' | tr -d 'v' | tr -d '.' | cut -d- -f1)
prune-all-bps-previous-tag: init-dsl-config  ## This will delete all blueprints (up to 10 at a time) that are associated to the previous working tag of the current COMMIT_BRANCH, regardless of application count.
	${DSL_VENV} calm get bps -q --limit 10 -n $(shell tags=$$(git rev-list --tags --max-count=2 | awk -F'[ ]' '{print $$1}{print $$2}') && tag=$$(echo $$tags | awk -F'[ ]' '{print$$2}' | xargs -I {} git describe --tags {} | awk -F'[-]' '{print$$1}{print$$2}' | tr ' ' '-') && echo $$tag | tr ' ' '-' | tr -d 'v' | tr -d '.' | cut -d- -f1) | xargs -I {} calm delete bp {}

## MAKE HELP TASKS
.PHONY: help
help:
	@grep -hE '^[A-Za-z0-9_ \-]*?:.*##.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

define DSL_WINDEV
windev:
	[ -f venv/Scripts/python3 ] || python -m venv venv
	venv/Scripts/python -m pip install --upgrade pip
	venv/Scripts/pip install setuptools --upgrade --ignore-installed
	venv/Scripts/pip install --no-cache -r requirements.txt -r dev-requirements.txt
	venv/Scripts/python setup.py develop
endef

define DSL_ADDITIONAL_TOOLS
cerberus>=1.3.4
endef

define CALM_DSL_VERSION_SELECTION
	echo $$'${YELLOW}Calm-DSL does not seem to be present in the local repo - Installing Calm-DSL as a submodule will occur now!${NOCOLOR}'; \
	export PS3=$$'\033[1;35mEnter the number for the desired version of Calm DSL: \033[0m'; \
	tags=($$(git ls-remote --tags https://github.com/nutanix/calm-dsl.git | awk -F/ '{ print $$3 }')); \
	echo $$'\033[1;32m'"Choose the Calm DSL version you wish to use from the list below: " $$'\033[0m'; \
	select tag in "$${tags[@]}"; \
	do \
		echo $$'\033[1;35m'"You selected choice ($$REPLY) which is tag $$tag" $$'\033[0m'; \
		if [ "$$tag" == "" ]; then \
			echo 'Invalid selection, please choose from one of the listed numbers, for example 1 or 2' >&2; \
		else \
			if [ ! -f .local/calm_dsl_version ]; then \
			mkdir -p .local; \
			fi; \
			echo $$tag >| .local/calm_dsl_version; \
		break; \
		fi; \
	done; \
	make install-dsl
endef