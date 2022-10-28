# Project utilities
env_create:
	conda create -n dev_kpi_calculation_platform python=3.10 -y

env_configure: env_install_dependencies env_install_jupyter_extensions env_install_precommit_hooks
	echo "Environment is configured"

env_install_precommit_hooks:
	pre-commit install && pre-commit install --hook-type commit-msg

env_install_dependencies:
	pip3 install --upgrade pip \
	&& pip3 install wheel poetry \
	&& poetry install

env_install_jupyter_extensions:
	jupyter contrib nbextension install --sys-prefix \
	&& jupyter nbextension enable --py widgetsnbextension \
	&& jupyter nbextension enable codefolding/main \
	&& jupyter nbextension enable spellchecker/main \
	&& jupyter nbextension enable toggle_all_line_numbers/main \
	&& jupyter nbextension enable hinterland/hinterland \
	&& jt -t grade3

env_delete:
	conda remove --name dev_kpi_calculation_platform --all -y

run_test:
	pytest

run_precommit:
	pre-commit run --all-files

run_build:
	docker build -f ./docker/Dockerfile -t dev_kpi_calculation_platform:latest .

run_lambda:
	docker run \
	-p 9000:8080 \
	-e AWS_REGION=${AWS_REGION} \
	-e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
	-e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
	-e APP_ENV=${APP_ENV} \
	dev_kpi_calculation_platform:latest

run_test:
	pytest
