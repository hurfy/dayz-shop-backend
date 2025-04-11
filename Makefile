# Default mode
.DEFAULT_GOAL := run

dzshop:
	poetry remove dzshop
	poetry add packages/dzshop
	poetry lock
	poetry sync

.PHONY: dzshop
