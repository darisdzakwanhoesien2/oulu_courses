# oulu_courses

Personal course/project archive with a small Streamlit demo app.

## What's In Here

- `app.py`: Streamlit "Machine Vision Interactive Lab" demo.
- `core/`: small image-processing modules used by `app.py`.
- `registry.json` + course folders: notes/data for courses.
- `_docs/`: generated documentation dumps (if you use the helper scripts).

## Quick Start (Streamlit demo)

1) Install dependencies (example)

```bash
pip install streamlit opencv-python numpy pillow
```

2) Run

```bash
streamlit run app.py
```

## Repo Helpers

- `structure_code.py`: generates a collapsible directory tree into `project_directory.md`.
- `dump_codebase_to_markdown.py`: dumps text files (and notebook cells) into `_docs/<project>/code_dump.md`.

## Notes

The previous long-form planning notes were moved to `notes.md`.

