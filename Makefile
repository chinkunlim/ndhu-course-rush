.PHONY: help install sync test audit run dev clean

help:
	@echo "Available make commands:"
	@echo "  make sync     - Sync project dependencies using uv"
	@echo "  make install  - Install Playwright browser dependencies"
	@echo "  make run      - Run the NDHU course selector script"
	@echo "  make test     - Run pytest test suite"
	@echo "  make audit    - Run Antigravity project compliance auditor"
	@echo "  make clean    - Remove build artifacts, pycache and test caches"

sync:
	uv sync

install:
	uv run playwright install chromium

run:
	uv run python auto_login.py

test:
	uv run pytest -v

audit:
	python3 audit_project.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info

