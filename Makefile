PYTHON ?= python

# make store name=switchbot version=latest method=all index-name=latest
# make store name=switchbot version=latest method=separate
store:
	$(PYTHON) -m rag.store.main --service $(name) --version $(version) --method $(method) $(if $(index-name),--index-name $(index-name))

# make repair name=switchbot types="commits pull-requests" config=9_DsLs out=./output
repair:
	$(PYTHON) -m rag.repair.main --service $(name) --source-types $(types) --configuration $(config) $(if $(out),--output-dir $(out))

# Consistency tests. They need neither API keys nor the packages in requirements.txt.
test:
	$(PYTHON) -m unittest discover -s tests -t .

.PHONY: store repair test
