SHELL=/bin/bash
export PYTHONPATH=src

all: data/processed/transactions.parq

data/raw/revisions.jsonl: scripts/get-revisions.py
	$^ $@

data/raw/transactions.jsonl: scripts/get-transactions.py data/raw/revisions.jsonl
	$^ $@

data/processed/transactions.parq: scripts/process-transactions.py data/raw/transactions.jsonl
	$^ $@

printvars:
	@$(foreach V,$(sort $(.VARIABLES)), \
	$(if $(filter-out environ% default automatic, \
	$(origin $V)),$(info $V=$($V) ($(value $V)))))

.PHONY: printvars
