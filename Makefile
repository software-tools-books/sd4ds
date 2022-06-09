.DEFAULT: commands

INFO=info/bibliography.bib info/glossary.yml info/links.yml
SRC=$(wildcard *.md) src/index.md $(wildcard src/*/index.md)

PORT=4000

## commands: show available commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## build: rebuild site without running server
build: docs/index.html
docs/index.html: ${SRC} ${INFO}
	ivy build

## serve: build site and run server
.PHONY: serve
serve:
	ivy watch --port ${PORT}

## single: create single-page HTML
single: docs/all.html
docs/all.html: bin/single.py info/head.html info/foot.html docs/index.html
	python bin/single.py --head info/head.html --foot info/foot.html --root docs > docs/all.html

## latex: create LaTeX document
latex: docs/sd4ds.tex
docs/sd4ds.tex: docs/all.html bin/tex.py info/head.tex info/foot.tex
	@make single
	python bin/tex.py --head info/head.tex --foot info/foot.tex < docs/all.html > docs/sd4ds.tex

## pdf: create PDF document
pdf: docs/sd4ds.tex
	cp info/bibliography.bib info/krantz.cls docs
	cd docs && pdflatex sd4ds
	cd docs && biber sd4ds
	cd docs && makeindex sd4ds
	cd docs && pdflatex sd4ds
	cd docs && pdflatex sd4ds

## clean: clean up stray files
clean:
	@find . -name '*~' -exec rm {} \;

## lint: check code
.PHONY: lint
lint:
	-flake8
	-isort --check .
	-black --check .

## valid: run html5validator on generated files
.PHONY: valid
valid: docs/all.html
	@html5validator --root docs \
	--ignore \
	'Attribute "g" not allowed on element "span"' \
	'Attribute "i" not allowed on element "span"'

## vars: show variables
.PHONY: vars
vars:
	@echo SRC ${SRC}

# Local commands if available.
-include local.mk
