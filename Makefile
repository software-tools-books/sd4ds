.DEFAULT: commands

ABBREV=sd4ds
HTML=info/head.html info/foot.html
INFO=info/bibliography.bib info/glossary.yml info/links.yml
IVY=$(wildcard lib/mccole/*/*.*)
TEX=info/head.tex info/foot.tex
SRC=$(wildcard *.md) $(wildcard src/*.md) $(wildcard src/*/index.md)

PORT=4000

## commands: show available commands
commands:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## build: rebuild site without running server
build: docs/index.html
docs/index.html: ${SRC} ${INFO} ${IVY} config.py
	ivy build && touch $@

## serve: build site and run server
.PHONY: serve
serve:
	ivy watch --port ${PORT}

## single: create single-page HTML
single: docs/all.html
docs/all.html: docs/index.html ${HTML} bin/single.py
	python bin/single.py --head info/head.html --foot info/foot.html --root docs > docs/all.html

## latex: create LaTeX document
latex: docs/${ABBREV}.tex
docs/${ABBREV}.tex: docs/all.html ${TEX} bin/html2tex.py
	python bin/html2tex.py --head info/head.tex --foot info/foot.tex < docs/all.html > docs/${ABBREV}.tex

## pdf: create PDF document
pdf: docs/${ABBREV}.tex
	cp info/bibliography.bib docs
	cd docs && pdflatex ${ABBREV}
	cd docs && biber ${ABBREV}
	cd docs && makeindex ${ABBREV}
	cd docs && pdflatex ${ABBREV}
	cd docs && pdflatex ${ABBREV}

## clean: clean up stray files
clean:
	@find . -name '*~' -exec rm {} \;
	@find . -type d -name __pycache__ | xargs rm -r

## lint: check code and structure
.PHONY: lint
lint:
	-flake8
	-isort --check .
	-black --check .
	python bin/lint.py --src src

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
	@echo HTML ${HTML}
	@echo INFO ${INFO}
	@echo IVY ${IVY}
	@echo SRC ${SRC}
	@echo TEX ${TEX}

# Local commands if available.
-include local.mk
