COMMON_CONFIG_FILE := ${PROJECT_ROOT}/common/common_config.json
USECASE_CONFIG_FILE := ./usecase_config.json
export

BASE64_FLAG :=
ifeq ($(OS),Windows_NT)
	BASE64_FLAG = -d
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Linux)
		BASE64_FLAG = -d
	endif
	ifeq ($(UNAME_S),Darwin)
		BASE64_FLAG = -D
	endif
endif

GIT_BRANCH_NAME := $(shell git rev-parse --abbrev-ref HEAD | head -c15)
GIT_COMMIT_ID := $(shell git rev-parse --short HEAD)
GIT_COMMIT_ID_PREVIOUS := $(shell git rev-list --parents -n 1 $$(git rev-parse --short HEAD) | awk -F'[ ]' '{print $$2}' | cut -c -7)

test-commit-id:
	@echo ${GIT_COMMIT_ID_PREVIOUS}

# Blueprint Git Tag remove dot notation because dots are not allowed in Blueprint naming.
BP_GIT_TAG := $(shell git rev-list --tags --max-count=1 | xargs -I {} git describe --tags {} | tr -d '.')

# Marketplace Git Tag leaves dot notation and remove 'v' character to stay in line with existing semantic versioning guidelines.
MP_GIT_TAG := $(shell git rev-list --tags --max-count=1 | xargs -I {} git describe --tags {} | tr -d 'v')
MP_GIT_TAG_PREVIOUS := $(shell tags=$$(git rev-list --tags --max-count=2 | awk -F'[ ]' '{print $$1}{print $$2}') && tag=$$(echo $$tags | awk -F'[ ]' '{print$$2}' | xargs -I {} git describe --tags {} | awk -F'[-]' '{print$$1}{print$$2}' | tr ' ' '-') && echo $$tag | tr ' ' '-' | tr -d 'v')

test-mp-tag:
	@echo ${MP_GIT_TAG_PREVIOUS}

test-bp:
	python blueprint-lin.py

BLUEPRINT_SUFFIX_NAME :=
ifeq ($(GIT_BRANCH_NAME),main)
	ifeq ($(strip $(BP_GIT_TAG)),)
		BLUEPRINT_SUFFIX_NAME = ${CALM_ENVIRONMENT}-${GIT_BRANCH_NAME}-${GIT_COMMIT_ID}
	endif
	ifneq ($(strip $(BP_GIT_TAG)),)
		BLUEPRINT_SUFFIX_NAME = $(BP_GIT_TAG)
	endif
else
	BLUEPRINT_SUFFIX_NAME := ${CALM_ENVIRONMENT}-${GIT_BRANCH_NAME}-${GIT_COMMIT_ID}
endif

DATE := $(shell date '+%M%S')

DSL_FILENAME := "blueprint.py"
BLUEPRINT_NAME := "NDB-MySQL-Provision"
MARKETPLACE_ITEM_NAME := "ECHo-Linux-Server"
MARKETPLACE_ITEM_NAME_TEST := "ECHo-Linux-Server-Test"
MARKETPLACE_CATEGORY := "DevOps"
MARKETPLACE_PRJ_LIST ?= default
GLOBAL_MARKETPLACE_ICON_NAME := "RedHatEnterpriseLogo"
CALM_AHV_PROFILE_NAME := AHV_Default
CALM_AHV_PROFILE_NAME_ABBR := $(shell echo ${CALM_AHV_PROFILE_NAME} | head -c3 | tr '[:upper:]' '[:lower:]')
AHV_TEST_PARAMSFILE := "tests/ahv_test_params.py"
AHV_APP_TEST_NAME := $(shell echo ${CALM_AHV_PROFILE_NAME_ABBR}-${DATE} | tr '[:upper:]' '[:lower:]')

ifeq ($(CALM_ENVIRONMENT),bwe)
	CALM_ENV_AHV_NAME = default
endif
ifeq ($(CALM_ENVIRONMENT),ams)
	CALM_ENV_AHV_NAME = default
endif

print-make-envs:
	@echo $(OS)
	@echo BASE64_FLAG=$(BASE64_FLAG)
	@echo CALM_ENVIRONMENT=$(CALM_ENVIRONMENT)

compile-bp:
	calm compile bp -f ${DSL_FILENAME}

compile-bp-json:
	calm compile bp -f ${DSL_FILENAME} -o json > bp.json

create-bp:
	calm compile bp -f ${DSL_FILENAME}
	calm create bp -f ${DSL_FILENAME} --name ${BLUEPRINT_NAME} --force

launch-ahv-test-bp:
	@echo CALM_ENV_AHV_NAME=${CALM_ENV_AHV_NAME}
	calm launch bp ${BLUEPRINT_NAME} --app_name ${AHV_APP_TEST_NAME} -ws --environment ${CALM_ENV_AHV_NAME} --profile_name ${CALM_AHV_PROFILE_NAME} \
	--launch_params ${AHV_TEST_PARAMSFILE}
	calm get apps --name ${AHV_APP_TEST_NAME}

launch-ahv-test-mp:
	calm launch marketplace item --app-name ${AHV_APP_TEST_NAME} --environment ${CALM_ENV_AHV_NAME} --profile-name ${CALM_AHV_PROFILE_NAME} \
	--launch_params ${AHV_TEST_PARAMSFILE} ${MARKETPLACE_ITEM_NAME_TEST}
	calm get apps --name ${AHV_APP_TEST_NAME}

### PUBLISHING NOTE ###
## The Python script used below sanitizes bp platform data during publishing.  Needed in cases where the bp was first created -
## on a project that has the same account that will be used when launched from the marketplace, e.g., bp created on project X, account X with project environment Y and will be
## launched from mp on project X, account X with project environment Z, the bp values, with project environment Y values baked-in, will overrride project environment Z values.
## In summary, without using the script for publishing, Calm Project Environment values will not be used if this is the case and values in the bp will -
## override the environment selected at mp launch.
publish-current-tag-bp:
    # Publish a new version of an existing blueprint to marketplace manager. This should only be executed from main stable branch.
    # calm publish bp -v ${MP_GIT_TAG} --existing_markeplace_bp --with_secrets -n ${MARKETPLACE_ITEM_NAME} -i ${GLOBAL_MARKETPLACE_ICON_NAME} -d "$$(cat mp_meta/bp-description.md | sed /References:/Q)" --project ${MARKETPLACE_PRJ_LIST} --publish_to_marketplace ${BLUEPRINT_NAME}
    # sanitize blueprint platform data prior to publishing so that environment configs can be populated at launch time.
	python ../../admin_tools/publish_bp_to_mp.py ${DSL_INIT_PARAMS} -v ${MP_GIT_TAG} --existing_markeplace_bp --with_secrets -n ${MARKETPLACE_ITEM_NAME} -i ${GLOBAL_MARKETPLACE_ICON_NAME} -d "$$(cat mp_meta/bp-description.md | sed /References:/Q)" --project ${MARKETPLACE_PRJ_LIST} --publish_to_marketplace --blueprint_name ${BLUEPRINT_NAME} --os LINUX --cat ${MARKETPLACE_CATEGORY}
	calm get marketplace bps -n ${MARKETPLACE_ITEM_NAME} -a PUBLISHED
publish-featurebranch-bp:
    # Publish a new version of an existing test blueprint to marketplace manager. This should only be executed from development branches for testing.
    # calm publish bp -v ${MP_GIT_TAG} --existing_markeplace_bp --with_secrets -n ${MARKETPLACE_ITEM_NAME_TEST} -i ${GLOBAL_MARKETPLACE_ICON_NAME} -d "$$(cat mp_meta/bp-description.md | sed /References:/Q)" --project ${MARKETPLACE_PRJ_LIST} --publish_to_marketplace ${BLUEPRINT_NAME}
    # sanitize blueprint platform data prior to publishing so that environment configs can be populated at launch time.
	python ../../admin_tools/publish_bp_to_mp.py ${DSL_INIT_PARAMS} -v ${GIT_COMMIT_ID} --existing_markeplace_bp --with_secrets -n ${MARKETPLACE_ITEM_NAME_TEST} -i ${GLOBAL_MARKETPLACE_ICON_NAME} -d "$$(cat mp_meta/bp-description.md | sed /References:/Q)" --project ${MARKETPLACE_PRJ_LIST} --publish_to_marketplace --blueprint_name ${BLUEPRINT_NAME} --os LINUX --cat ${MARKETPLACE_CATEGORY}
	calm get marketplace bps -n ${MARKETPLACE_ITEM_NAME_TEST} -a PUBLISHED

unpublish-mp-current-tag:
	# Unpublish blueprints from marketplace store
	calm unpublish marketplace bp -v ${MP_GIT_TAG} -s LOCAL ${MARKETPLACE_ITEM_NAME}

delete-mp-current-tag:
	# Delete approved marketplace item from store
	calm delete marketplace bp -v ${MP_GIT_TAG} -s LOCAL ${MARKETPLACE_ITEM_NAME}

unpublish-mp-previous-tag:
	# Unpublish blueprints from marketplace store
	calm unpublish marketplace bp -v ${MP_GIT_TAG_PREVIOUS} -s LOCAL ${MARKETPLACE_ITEM_NAME}

delete-mp-previous-tag:
	# Delete approved marketplace item from store
	calm delete marketplace bp -v ${MP_GIT_TAG_PREVIOUS} -s LOCAL ${MARKETPLACE_ITEM_NAME}

unpublish-mp-current-commitid:
	# Unpublish blueprints from marketplace store
	calm unpublish marketplace bp -v ${GIT_COMMIT_ID} -s LOCAL ${MARKETPLACE_ITEM_NAME_TEST}

delete-mp-current-commitid:
	# Delete approved marketplace item from store
	calm delete marketplace bp -v ${GIT_COMMIT_ID} -s LOCAL ${MARKETPLACE_ITEM_NAME_TEST}

unpublish-mp-previous-commitid:
	# Unpublish blueprints from marketplace store
	calm unpublish marketplace bp -v ${GIT_COMMIT_ID_PREVIOUS} -s LOCAL ${MARKETPLACE_ITEM_NAME_TEST}

delete-mp-previous-commitid:
	# Delete approved marketplace item from store
	calm delete marketplace bp -v ${GIT_COMMIT_ID_PREVIOUS} -s LOCAL ${MARKETPLACE_ITEM_NAME_TEST}