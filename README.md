# Вступ до Webots

Self-study course (in Ukrainian), built with [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

- Pages: `docs/` (home page is `docs/index.md`)
- Navigation: `docs/SUMMARY.md`
- Screenshots: `docs/images/`
- Config: `mkdocs.yml`
- Starter projects: `projects/urok-NN/` (state at the start of lesson NN); `tools/mkdocs_hooks.py` zips them into `docs/downloads/urok-NN.zip` on every build (generated, not committed)
- Screenshot tooling: `tools/screenshots/` (`ui.py` drives the live Webots window on Hyprland, `annotate.py` + `specs.py` turn raw captures into `docs/images/`)

## Build

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve          # live preview at http://127.0.0.1:8000
.venv/bin/mkdocs build --strict # static site in site/
```

## Markdown conventions

```markdown
!!! warning "Увага"

    Callout text, indented 4 spaces (types: info, warning, danger, success).

??? success "Відповідь"

    Collapsible answer to a self-check question.
```

Continuation lines inside numbered lists (images, tips) are indented 4 spaces.
