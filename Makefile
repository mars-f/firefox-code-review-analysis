SHELL=/bin/bash
export PYTHONPATH=src

all: data/processed/transactions.parq data/processed/users.parq

data/raw/revisions.jsonl: scripts/get-revisions.py
	$^ $@

data/raw/transactions.jsonl: scripts/get-transactions.py data/raw/revisions.jsonl
	$^ $@

data/raw/users.jsonl: scripts/get-users.py
	$^ $@

data/processed/transactions.parq: scripts/process-transactions.py data/raw/transactions.jsonl
	$^ $@

data/processed/users.parq: scripts/process-users.py data/raw/users.jsonl
	$^ $@
