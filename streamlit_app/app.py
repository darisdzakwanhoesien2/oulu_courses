import streamlit as st
from pathlib import Path

from loaders import load_registry
from utils import resolve_path
from renderers import render_notebook, render_metadata

ROOT = Path(__file__).parents[1]
REGISTRY_PATH = ROOT / "registry.json"

st.set_page_config(
    page_title="📚 Course Documentation Hub",
    layout="wide"
)

st.title("📘 University Coursework Documentation")
st.caption("Indexed notebooks, experiments, and datasets")

projects = load_registry(REGISTRY_PATH)

# Sidebar filters
courses = sorted(set(p["course"] for p in projects))
selected_course = st.sidebar.selectbox("Course", ["All"] + courses)

filtered = [
    p for p in projects
    if selected_course == "All" or p["course"] == selected_course
]

selected = st.sidebar.selectbox(
    "Select Document",
    filtered,
    format_func=lambda x: x["title"]
)

render_metadata(selected)

content_path = resolve_path(ROOT, selected["path"])

if selected["type"] == "notebook":
    render_notebook(content_path)
else:
    st.info("Unsupported document type")