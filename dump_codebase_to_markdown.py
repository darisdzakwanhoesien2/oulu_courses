#!/usr/bin/env python3

import sys
import json
from pathlib import Path
from typing import List

# ==================================================
# CONFIG
# ==================================================

ROOT = Path.cwd()                      # Run from anywhere
DOCS_ROOT = ROOT / "_docs"             # Output folder

EXCLUDE_DIRS = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
    "node_modules",
    "extracted",
    "docs",
    "data",
    "previous_data",
    "outputs",
    "logs",
}

EXCLUDE_FILES = {
    ".DS_Store",
}

TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".txt",
    ".csv",
    ".toml",
    ".ini",
    ".env",
    ".ipynb",   # ✅ notebooks supported
}

# ==================================================
# HELPERS
# ==================================================

def is_text_file(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS


def should_skip(path: Path) -> bool:
    if path.name in EXCLUDE_FILES:
        return True
    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True
    return False


def fence_for_extension(ext: str) -> str:
    return {
        ".py": "python",
        ".json": "json",
        ".md": "markdown",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".csv": "csv",
        ".toml": "toml",
        ".ini": "ini",
        ".ipynb": "python",   # rendered as extracted code blocks
        ".txt": "",
    }.get(ext.lower(), "")


# ==================================================
# NOTEBOOK PARSER
# ==================================================

def extract_notebook_cells(nb_path: Path) -> List[str]:
    """
    Extract markdown + code cells from a Jupyter notebook.
    Skips outputs and base64 blobs.
    """
    blocks = []

    try:
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"⚠️ Failed to parse notebook: {e}"]

    cells = nb.get("cells", [])

    for i, cell in enumerate(cells, start=1):
        cell_type = cell.get("cell_type", "")
        source = "".join(cell.get("source", [])).rstrip()

        if not source.strip():
            continue

        if cell_type == "markdown":
            blocks.append(f"\n### 📝 Markdown Cell {i}\n")
            blocks.append(source)

        elif cell_type == "code":
            blocks.append(f"\n### 💻 Code Cell {i}\n")
            blocks.append("```python")
            blocks.append(source)
            blocks.append("```")

    if not blocks:
        blocks.append("_No extractable cells found._")

    return blocks


# ==================================================
# MAIN LOGIC
# ==================================================

def dump_codebase(codebase_path: Path):

    if not codebase_path.exists():
        raise FileNotFoundError(f"❌ Path not found: {codebase_path}")

    codebase_path = codebase_path.resolve()

    project_name = codebase_path.name
    out_dir = DOCS_ROOT / project_name
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file = out_dir / "code_dump.md"

    lines = []
    lines.append(f"# 📦 Full Code Dump — `{project_name}`\n")
    lines.append(f"> Source path: `{codebase_path}`\n")
    lines.append("> Auto-generated snapshot of the entire codebase\n")
    lines.append("---\n")

    file_count = 0

    for path in sorted(codebase_path.rglob("*")):
        if path.is_dir():
            continue
        if should_skip(path):
            continue
        if not is_text_file(path):
            continue

        rel_path = path.relative_to(codebase_path)
        ext = path.suffix.lower()

        lines.append(f"## 📁 `{rel_path}`\n")

        # --------------------------------------------------
        # Jupyter Notebook
        # --------------------------------------------------
        if ext == ".ipynb":
            blocks = extract_notebook_cells(path)
            lines.extend(blocks)
            lines.append("\n")
            file_count += 1
            continue

        # --------------------------------------------------
        # Normal text files
        # --------------------------------------------------
        fence = fence_for_extension(ext)

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(errors="ignore")

        lines.append(f"```{fence}")
        lines.append(content.rstrip())
        lines.append("```")
        lines.append("")

        file_count += 1

    if file_count == 0:
        lines.append("⚠️ No eligible files were found. Check extension filters.\n")

    out_file.write_text("\n".join(lines), encoding="utf-8")

    print(f"✅ {file_count} files dumped")
    print(f"📄 Output: {out_file}")


# ==================================================
# CLI
# ==================================================

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python dump_codebase_to_markdown.py <path>")
        print("Example:")
        print("  python dump_codebase_to_markdown.py .")
        sys.exit(1)

    target_path = Path(sys.argv[1]).expanduser()
    dump_codebase(target_path)
