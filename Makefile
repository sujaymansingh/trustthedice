

.PHONY: dependencies
dependencies:
	@pip install --editable .


.PHONY: test
test:
	@pytest --doctest-modules trustthedice tests
