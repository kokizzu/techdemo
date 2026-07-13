PYTHON ?= python3
CMD ?=

.PHONY: test run

test:
	$(PYTHON) scripts/test_cdk_python_lambda.py

run:
	@test -n "$(CMD)" || (echo "usage: make run CMD='python3 scripts/test_cdk_python_lambda.py'" >&2; exit 2)
	$(CMD)
