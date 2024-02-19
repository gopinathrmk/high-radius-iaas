CALM_ENVIRONMENT ?=
export CALM_ENVIRONMENT

BASE64_FLAG:=
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

EP_DSL_FILENAME := "linux_endpoint.py"
EP_NAME := "LIN_ENDPOINT"

validate:
	@echo CALM_ENVIRONMENT=${CALM_ENVIRONMENT}
	@echo "---LOCAL GIT ONLY - Specific Variables---"
	@echo GIT_BRANCH_NAME=${GIT_BRANCH_NAME}
	@echo GIT_COMMIT_ID=${GIT_COMMIT_ID}
	@echo MP_GIT_TAG=${MP_GIT_TAG}
	@echo "---ENDPOINT ONLY - Specific Variables---"
	@echo WIN_EP_DSL_FILENAME=${EP_DSL_FILENAME}
	@echo WIN_EP_NAME=${EP_NAME}
	@echo $(shell calm --version)
	@echo $(shell make --version | head -n1)
	@echo $(shell python --version | head -n1)
	@echo $(shell pip --version | awk '{print $1 " " $2}')

create-endpoint: validate
	calm create endpoint --name ${EP_NAME} --file ${EP_DSL_FILENAME} --force

delete-endpoint: validate
	calm delete endpoint ${EP_NAME}