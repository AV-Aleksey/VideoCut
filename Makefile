run:
	.venv/bin/python -m uvicorn internal.main:app --reload

lint:
	.venv/bin/python -m ruff .