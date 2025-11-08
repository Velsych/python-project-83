install:
	uv sync

build:
	uv build

package-install:
	uv tool install dist/*.whl


package-reinstall: build
	uv tool install --force dist/*.whl


lint:
	uv run ruff check page_analyzer


fix:
	uv run ruff check page_analyzer --fix

coverage:
	uv run pytest --cov --cov-report xml

test:
	uv run pytest tests

dev:
	uv run flask --debug --app page_analyzer:app run --port 8000

PORT ?= 8000
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
build:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app