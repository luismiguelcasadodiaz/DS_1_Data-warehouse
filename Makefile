# Set the default goal so running `make` with no arguments prints the help menu

.DEFAULT_GOAL := help
environment := piscine
DEF_TAB_DS0_EX02 ?=DS_0_Creation_DB/data/customer/data_2022_oct.csv 

.PHONY: help
help: ## Show this help menu
	@awk 'BEGIN {FS = ":.*?## "} /^[0-9a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
# ###############################################################33
.PHONY: DS1_ex00
DS1_ex00: ## import items
	psql -U luicasad -d piscineds -h localhost -c "SELECT * FROM data_2022_oct WHERE event_type = 'cart' AND event_time >= '2022-10-01 00:00:00' LIMIT 6;"

.PHONY: DS1_ex01
DS1_ex01: ## concatenates all data_202*_***.csv into customers
	@python ex01/customer_table.py

.PHONY: DS1_ex02
DS1_ex02: ## remove duplicates in customer table
	@echo "This is a heavy operation. best if logged via ssh"
	@python ex02/remove_duplicates.py 

.PHONY: DS1_ex03
DS1_ex03: ## combine the "customers" tables with "items" in the "customers" table
	python ex03/fusion.py 
# ###############################################################33


.PHONY: set
set: ## Set a python environment for this project
	bash -c "python3 -m venv $(environment) && source $(environment)/bin/activate && pip install --upgrade pip &&pip install -r requirements.txt"

.PHONY: activate
activate: ## Activate the python environment for this project
	@echo "Run: source $(environment)/bin/activate"

.PHONY: unset
unset: ## removes the python 
	rm -rf $(environment)

.PHONY: upgrade
upgrade: ## Upgrades pip
	pip install --upgrade pip

.PHONY: norminette
norminette: ## Run norminette on all .py files
	flake8  */*.py		
