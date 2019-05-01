

.PHONY: dependencies
dependencies:
	@pip install --editable .


.PHONY: format
format:
	@black trustthedice tests


.PHONY: test
test:
	@pytest --doctest-modules trustthedice tests
