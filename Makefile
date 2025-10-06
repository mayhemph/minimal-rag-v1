.PHONY: venv install run clean
venv:
	python -m venv .venv
install: venv
	. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt
run:
	. .venv/bin/activate && cp -n .env.example .env || true && python src/rag_cli.py
clean:
	rm -rf .venv .chroma_db