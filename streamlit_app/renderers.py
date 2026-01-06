import streamlit as st
import nbformat
from nbconvert import HTMLExporter

def render_notebook(path):
    with open(path, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    html_exporter = HTMLExporter()
    body, _ = html_exporter.from_notebook_node(nb)
    st.components.v1.html(body, height=800, scrolling=True)


def render_metadata(entry):
    st.markdown(f"### {entry['title']}")
    st.caption(entry["description"])

    st.markdown("**Tags:** " + ", ".join(entry.get("tags", [])))
    st.markdown(f"**Course:** {entry['course']}")