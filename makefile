.PHONY: help
help:
		@echo "---------------HELP-----------------"
		@echo "- make install --> Install the dependencies"
		@echo "- make up-local --> Setup Environment"
		@echo "- make start --> Run local app"
		@echo "- make test --> Run all tests"
		@echo "- make seeds --> Run seeder"
		@echo "- make test-coverage --> Run tests coverage"
		@echo "------------------------------------"

.PHONY: install
install:
		@echo "=========================================Installing dependencies Performance========================================="
		pip install --upgrade pip
		pip install -r requirements.txt
		@echo "Completed! "

.PHONY: up-local
up-local: export FLASK_ENV=development
up-local:
		@echo "=========================================Set up Pizza Planet app Environment========================================="
		python3 manage.py db init
		python3 manage.py db migrate
		python3 manage.py db upgrade

.PHONY: seeds
seeds:
		@echo "=====================================================Run Seeder================================================="
		python ./manage.py seed run --root app/seeds

.PHONY: start
start:
		@echo "=====================================================Run App Locally================================================="
		python3 manage.py run

.PHONY: test
test:
		@echo "=====================================================Run Tests================================================="
		python3 manage.py test

test-coverage:
		@echo "=====================================================Run Tests Coverage================================================="
		coverage run -m pytest -v && coverage report -m
