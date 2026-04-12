import os
import difflib
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Code comparison — CG_assignment1", layout="wide")

st.title("Code comparison — CG_assignment1")

# --- changed: scan the entire new_app/project folder for files and present them in dropdowns ---
BASE = "/Users/darisdzakwanhoesien/Documents/project_documentation/codebase/education/oulu_courses/new_app/project"

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
# -------------------------------------------------------------------------------

if not FILE_OPTIONS:
    st.error(f"No files found under: {BASE}")
    st.stop()

left_label_default = list(FILE_OPTIONS.keys())[0]
right_label_default = list(FILE_OPTIONS.keys())[1] if len(FILE_OPTIONS) > 1 else left_label_default

left_label = st.sidebar.selectbox("Left file", list(FILE_OPTIONS.keys()), index=0)
right_label = st.sidebar.selectbox("Right file", list(FILE_OPTIONS.keys()), index=1 if len(FILE_OPTIONS) > 1 else 0)

left_path = FILE_OPTIONS[left_label]
right_path = FILE_OPTIONS[right_label]

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

view = st.sidebar.radio("View mode", ["Side-by-side HTML", "Unified diff (text)", "Raw left", "Raw right"])

st.markdown(f"**Left:** `{left_label}` — `{left_path}`  ")
st.markdown(f"**Right:** `{right_label}` — `{right_path}`  ")

if view == "Side-by-side HTML":
    # Generate an HTML side-by-side diff using difflib.HtmlDiff and embed it
    differ = difflib.HtmlDiff(tabsize=4, wrapcolumn=140)
    html = differ.make_file(left_lines, right_lines, fromdesc=left_label, todesc=right_label)
    # Reduce height if very large; allow scrolling
    components.html(html, height=800, scrolling=True)

elif view == "Unified diff (text)":
    ud = difflib.unified_diff(left_lines, right_lines, fromfile=left_label, tofile=right_label, lineterm="")
    diff_text = "\n".join(list(ud))
    if not diff_text:
        st.success("No differences found.")
    else:
        st.code(diff_text, language="diff")

elif view == "Raw left":
    st.subheader(left_label)
    st.code("\n".join(left_lines), language="python")

elif view == "Raw right":
    st.subheader(right_label)
    st.code("\n".join(right_lines), language="python")

st.sidebar.markdown("---")
st.sidebar.markdown("Actions")
if st.sidebar.button("Open both files in editor (path)"):
    st.sidebar.code(left_path)
    st.sidebar.code(right_path)

st.markdown("Tip: Use the side-by-side HTML view for a quick visual diff and the unified view for a concise patch you can apply.")