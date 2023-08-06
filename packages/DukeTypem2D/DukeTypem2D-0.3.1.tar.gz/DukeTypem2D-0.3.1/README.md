# Duke Typem 2D

Improves readability, spelling and expression of your text documents. The main focus will be scientific documents.

**WARNING**: as of now this is a non-working skeleton / prototype.

### Planned features:

- read in your documents (tex, markdown, reStructuredText, word, pdf, ...)
- check spelling
- hint at common mistakes
- evaluate choice of words
- improve readability and overall quality
- analyze phrasing and expression

### How can it be used?

- python package
- continuous integration via pre-commit
- web-API
- maybe a language

## Installation

### Extension-Options

- `web`: include web-api
- `dev`: packages used for development-work around the package
- `test`v: all dependencies for the unittests

### Locally

This example installs `DukeTypem` with `web` and `dev` extension.

```
git clone https://github.com/orgua/DukeTypem2D
cd DukeTypem2D
pip install ./[web, test]
```

### Via pip from Pypi

This example installs `DukeTypem` with no extension.

```
pip install DukeTypem2d
```



## Technical Requirements

### Basics

- Python with latest

### Config

- language: en, de, ..
- feature-choice
- file-ignore
- fix-mode that changes file on-demand (double-spaces)

### Input Files

- txt - plain text
- tex - LaTeX
- md - Markdown
- html - HTML
- rst - reStructuredText

## Program Structure

### Preparation

- file parsing
- cleanup
- remove code
  - [HTML](https://pypi.org/project/html2text/)
- break text up into file, line, sentence, word
- link line numbers to text-fragments

### Rule-Set

- per dataset (all files), file, line, sentence, word
- reimplement [TNT](https://github.com/entorb/typonuketool)
- add in [hpmor checks](https://github.com/entorb/hpmor-de/tree/main/scripts)
- Fix basic Syntax of document-format? like [markdown](https://www.markdownguide.org/basic-syntax)

### Output

- plain pipeline log (for console)
- HTML, similar to TNT
- Language Server Protocol (LSP) for IDEs
- readability score via [Textstat](https://pypi.org/project/textstat/)
  - [Flesch-Reading-Ease](https://de.wikipedia.org/wiki/Lesbarkeitsindex#Flesch-Reading-Ease)

## Inspiration

A modern take on the original [Typo Nuke Tool](https://entorb.net/TypoNukeTool/) ([git](https://github.com/entorb/typonuketool)).


## nearToDo

- allow pre-commit hooking
- add github-actions for testing
- add project-infos
- documentation skeleton
- begin inner workings
- add to pypi

## Latest Changes

- project bootstrap based on ['23 ruleset](https://blog.pronus.io/en/posts/python/how-to-set-up-a-perfect-python-project/)
- add configs for tools in toml
