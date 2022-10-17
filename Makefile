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

run_uvicorn:
	uvicorn src.endpoints.main:app \
		--host 0.0.0.0 \
		--port 8000 \
		--reload \
		--log-config log.ini

run_gunicorn:
	gunicorn \
		--bind 0.0.0.0:8000 \
		src.endpoints.main:app \
		--workers 2 \
		-k uvicorn.workers.UvicornWorker \
		--timeout 5 \
		--log-config log.ini

run_build:
	docker build -f ./docker/Dockerfile -t dev_kpi_calculation_platform:latest .

run_docker_api:
	docker run --platform linux/amd64 -p 80:8000 --env-file .env --mount type=bind,source="$(pwd)/"logs,target=/dev_veolia_uk_backend/logs -d dev_veolia_uk_backend:latest gunicorn --bind 0.0.0.0:8000 --workers 8 -k uvicorn.workers.UvicornWorker --timeout 5 --log-config log.ini src.endpoints.main:app

run_docker_tests:
	docker run -it --platform linux/amd64 --env-file .env dev_kpi_calculation_platform:latest pytest
