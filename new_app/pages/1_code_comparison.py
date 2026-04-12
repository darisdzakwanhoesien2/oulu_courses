import os
import json
import difflib
from pathlib import Path
import re

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Code comparison — CG_assignment1", layout="wide")

st.title("Code comparison — CG_assignment1")

# --- changed: scan the entire new_app/project folder for files and present them in dropdowns ---
BASE = str(Path(__file__).parent.parent / "project")
DATA_JSON = Path(__file__).parent.parent / "data.json"

def collect_files(base_dir: str):
    p = Path(base_dir)
    if not p.exists():
        return {}
    files = [f for f in p.rglob("*") if f.is_file()]
    files.sort()
    # Use relative paths as labels so dropdown is compact
    labels = [str(f.relative_to(p)) for f in files]
    return {label: str(p.joinpath(label)) for label in labels}

FILE_OPTIONS = collect_files(BASE)

# --- presets handling (JSON) ---
def load_presets(json_path: Path):
    if not json_path.exists():
        return []
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
        return data.get("presets", [])
    except Exception:
        return []

def save_preset(json_path: Path, preset: dict):
    data = {"presets": []}
    if json_path.exists():
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
        except Exception:
            data = {"presets": []}
    data.setdefault("presets", [])
    # avoid duplicates by label
    existing = [p for p in data["presets"] if p.get("label") == preset.get("label")]
    if existing:
        # replace
        data["presets"] = [p for p in data["presets"] if p.get("label") != preset.get("label")]
    data["presets"].append(preset)
    json_path.write_text(json.dumps(data, indent=2), encoding="utf-8")

PRESETS = load_presets(DATA_JSON)
# PRESET structure example:
# {"label":"assignment1-cg", "left":"Computer_Graphics_2026/Assignment1/CG_assignment1.py", "right":"Computer_Graphics_2026/Assignment1_Daris.../CG_assignment1.py"}

# -------------------------------------------------------------------------------

if not FILE_OPTIONS:
    st.error(f"No files found under: {BASE}")
    st.stop()

# Reverse map for quick lookup
PATH_TO_LABEL = {p: lbl for (lbl, p) in FILE_OPTIONS.items()}

# Selection source: manual browse or presets
selection_mode = st.sidebar.radio("Selection source", ["Manual (browse files)", "Presets (JSON)"])

left_path = right_path = None
left_label = right_label = None

if selection_mode == "Presets (JSON)":
    if not PRESETS:
        st.sidebar.warning(f"No presets found in {DATA_JSON}. Use Manual mode or add presets.")
        selection_mode = "Manual (browse files)"
    else:
        preset_labels = [p.get("label", f"preset-{i}") for i, p in enumerate(PRESETS)]
        chosen = st.sidebar.selectbox("Choose preset", preset_labels, index=0)
        preset = PRESETS[preset_labels.index(chosen)]
        # Resolve preset paths relative to new_app/project if they are relative
        def resolve_path(pth):
            p = Path(pth)
            if not p.is_absolute():
                candidate = Path(BASE) / p
                if candidate.exists():
                    return str(candidate)
                # allow direct join to project root if user provided leading folder name
                candidate2 = Path(__file__).parent.parent / p
                if candidate2.exists():
                    return str(candidate2)
            return str(pth)
        left_path = resolve_path(preset.get("left", ""))
        right_path = resolve_path(preset.get("right", ""))

# Manual browse fallback / default
if selection_mode == "Manual (browse files)":
    left_label_default = list(FILE_OPTIONS.keys())[0]
    right_label_default = list(FILE_OPTIONS.keys())[1] if len(FILE_OPTIONS) > 1 else left_label_default

    left_label = st.sidebar.selectbox("Left file", list(FILE_OPTIONS.keys()), index=0)
    right_label = st.sidebar.selectbox("Right file", list(FILE_OPTIONS.keys()), index=1 if len(FILE_OPTIONS) > 1 else 0)

    left_path = FILE_OPTIONS[left_label]
    right_path = FILE_OPTIONS[right_label]

# --- show selected pair and a compact mapped list of all available files ---
st.sidebar.markdown("### Selected pair")
st.sidebar.code(f"left:  {left_path}\nright: {right_path}")

st.markdown("## File mapping")
st.markdown("List of all files under new_app/project with the currently selected pair annotated:")
for label, path in FILE_OPTIONS.items():
    tag = ""
    if path == left_path:
        tag = " (left)"
    elif path == right_path:
        tag = " (right)"
    st.markdown(f"- `{path}`{tag}")
# --- end new code ---

# Basic existence checks
missing = []
for p in (left_path, right_path):
    if not Path(p).exists():
        missing.append(p)
if missing:
    st.error(f"The following file(s) were not found in the workspace:\n\n" + "\n".join(missing))
    st.stop()

def read_lines(p):
    # Attempt to read as text; fall back to a placeholder on failure (binary files)
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read().splitlines(keepends=False)
    except Exception:
        return [f"<unable to read file as text: {p}>"]

left_lines = read_lines(left_path)
right_lines = read_lines(right_path)

# --- new: generate a short human-readable change report from the unified diff ---
def make_unified_diff(left_lines, right_lines, fromfile, tofile):
    return list(difflib.unified_diff(left_lines, right_lines, fromfile=fromfile, tofile=tofile, lineterm=""))

def summarize_diff(ud_lines):
    added = sum(1 for l in ud_lines if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in ud_lines if l.startswith("-") and not l.startswith("---"))
    hunks = []
    current = None
    for l in ud_lines:
        if l.startswith("@@"):
            if current:
                hunks.append(current)
            current = {"header": l, "lines": []}
        elif current is not None:
            current["lines"].append(l)
    if current:
        hunks.append(current)
    # find added/removed defs or classes
    pattern = re.compile(r'^[\+\-]\s*(def|class)\s+([A-Za-z_][A-Za-z0-9_]*)')
    added_defs = []
    removed_defs = []
    for l in ud_lines:
        m = pattern.match(l)
        if m:
            if l.startswith("+"):
                added_defs.append(f"{m.group(1)} {m.group(2)}")
            elif l.startswith("-"):
                removed_defs.append(f"{m.group(1)} {m.group(2)}")
    return {"added_lines": added, "removed_lines": removed, "num_hunks": len(hunks), "hunks": hunks, "added_defs": added_defs, "removed_defs": removed_defs}

unified = make_unified_diff(left_lines, right_lines, left_path, right_path)
report = summarize_diff(unified)
# --- end new code ---

# --- new: LaTeX report generator ---
def generate_latex_report(left_path: str, right_path: str, report: dict, unified_lines: list) -> str:
    def latex_itemize(items):
        if not items:
            return "None\n"
        lines = []
        for s in items:
            escaped = s.replace("_", "\\_")
            lines.append("\\item " + escaped)
        return "\n".join(lines) + "\n"

    # Precompute escaped strings to avoid backslashes inside f-string expressions
    left_escaped = left_path.replace("_", "\\_")
    right_escaped = right_path.replace("_", "\\_")
    unified_text = "\n".join(unified_lines)

    top_hunks = ""
    for h in report["hunks"][:6]:
        block = "\n".join(h["lines"][:30])
        top_hunks += "\\begin{verbatim}\n" + h["header"] + "\n" + block + "\n\\end{verbatim}\n\n"

    latex = f"""\\documentclass[11pt]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{geometry}}
\\geometry{{margin=1in}}
\\title{{Code comparison report}}
\\author{{Auto-generated}}
\\date{{\\today}}

\\begin{{document}}
\\maketitle

\\section*{{Files compared}}
\\begin{{itemize}}
\\item Left: \\texttt{{{left_escaped}}}
\\item Right: \\texttt{{{right_escaped}}}
\\end{{itemize}}

\\section*{{Summary}}
\\begin{{itemize}}
\\item Lines added: {report['added_lines']}
\\item Lines removed: {report['removed_lines']}
\\item Changed hunks: {report['num_hunks']}
\\end{{itemize}}

\\section*{{Added / removed definitions}}
\\subsection*{{Added}}
\\begin{{itemize}}
{latex_itemize(report['added_defs'])}
\\end{{itemize}}

\\subsection*{{Removed}}
\\begin{{itemize}}
{latex_itemize(report['removed_defs'])}
\\end{{itemize}}

\\section*{{Top changed hunks (preview)}}
{top_hunks}

\\section*{{Full unified diff (optional)}}
\\begin{{verbatim}}
{unified_text}
\\end{{verbatim}}

\\end{{document}}
"""
    return latex
# --- end LaTeX generator ---

# add LaTeX option to view selection
view = st.sidebar.radio("View mode", ["Side-by-side HTML", "Unified diff (text)", "Raw left", "Raw right", "Change report", "LaTeX report"])

st.markdown(f"**Left:** `{left_path}`  ")
st.markdown(f"**Right:** `{right_path}`  ")

if view == "Side-by-side HTML":
    # Generate an HTML side-by-side diff using difflib.HtmlDiff and embed it
    differ = difflib.HtmlDiff(tabsize=4, wrapcolumn=140)
    html = differ.make_file(left_lines, right_lines, fromdesc=left_path, todesc=right_path)
    components.html(html, height=800, scrolling=True)

elif view == "Unified diff (text)":
    ud = unified
    diff_text = "\n".join(ud)
    if not diff_text:
        st.success("No differences found.")
    else:
        st.code(diff_text, language="diff")

elif view == "Raw left":
    st.subheader(Path(left_path).name)
    st.code("\n".join(left_lines), language="python")

elif view == "Raw right":
    st.subheader(Path(right_path).name)
    st.code("\n".join(right_lines), language="python")

elif view == "Change report":
    st.header("Change report (auto-generated)")
    st.markdown("A concise summary of the differences between the selected files.")
    cols = st.columns(3)
    cols[0].metric("Lines added", report["added_lines"])
    cols[1].metric("Lines removed", report["removed_lines"])
    cols[2].metric("Changed hunks", report["num_hunks"])

    with st.expander("Added / removed functions and classes", expanded=True):
        if report["added_defs"]:
            st.subheader("Added")
            for d in report["added_defs"]:
                st.write(f"- {d}")
        else:
            st.write("No added function/class definitions detected.")
        if report["removed_defs"]:
            st.subheader("Removed")
            for d in report["removed_defs"]:
                st.write(f"- {d}")
        else:
            st.write("No removed function/class definitions detected.")

    with st.expander("Top changed hunks (preview)", expanded=True):
        if report["hunks"]:
            for h in report["hunks"][:6]:
                sample = h["header"] + "\n" + "\n".join(h["lines"][:30])
                st.code(sample, language="diff")
        else:
            st.write("No hunks to show (files identical).")

elif view == "LaTeX report":
    st.header("LaTeX report (generated)")
    latex = generate_latex_report(left_path, right_path, report, unified)
    st.markdown("Copy the generated LaTeX below or download as a .tex file.")
    st.code(latex, language="latex")
    st.download_button("Download .tex", data=latex.encode("utf-8"), file_name="code_comparison_report.tex", mime="text/x-tex")

st.sidebar.markdown("---")
st.sidebar.markdown("Actions")
col1, col2 = st.sidebar.columns(2)
if col1.button("Open both files in editor (path)"):
    st.sidebar.code(left_path)
    st.sidebar.code(right_path)

# Save current manual pair as preset
if selection_mode == "Manual (browse files)":
    preset_label = st.sidebar.text_input("Preset label (save current pair as)", value=f"{Path(left_path).name} vs {Path(right_path).name}")
    if col2.button("Save preset to JSON"):
        preset = {"label": preset_label, "left": str(Path(left_path).relative_to(Path(BASE)) if Path(left_path).is_relative_to(Path(BASE)) else left_path), "right": str(Path(right_path).relative_to(Path(BASE)) if Path(right_path).is_relative_to(Path(BASE)) else right_path)}
        try:
            save_preset(DATA_JSON, preset)
            st.sidebar.success(f"Preset saved to {DATA_JSON}")
        except Exception as e:
            st.sidebar.error(f"Failed to save preset: {e}")

st.markdown("Tip: Use the side-by-side HTML view for a quick visual diff and the unified view for a concise patch you can apply.")