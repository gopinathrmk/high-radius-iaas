SHELL := /bin/bash

.PHONY: init-ssh-keys
init-ssh-keys:
	@if [ ${SSH_KEY_TYPE} == "private" ]; then \
		read -d "~" -e -p $$'\033[1;35mPaste in the private ssh key for the Linux user ${USER} credential (type \"~\" when done pasting) \033[0m: ' privatecredkey ; \
        echo "$$privatecredkey" >> .local/${CALM_ENVIRONMENT}/CRED-credkey; \
        break; \
    elif [ ${SSH_KEY_TYPE} == "public" ]; then \
        read -d "~" -e -p $$'\033[1;35mPaste in the public ssh key for the Linux user ${USER} credential (type \"~\" when done pasting) \033[0m: ' publiccredkey ; \
        echo "$$publiccredkey" >> .local/${CALM_ENVIRONMENT}/CRED-credkey; \
        break; \
    fi; \

schema-input:
	@python user_input_schema.py