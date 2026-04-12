import streamlit as st
import nbformat
from nbconvert import HTMLExporter
from pathlib import Path


# -----------------------------
# Metadata renderer
# -----------------------------
def render_metadata(entry):
    st.markdown(f"## {entry['title']}")
    if entry.get("description"):
        st.write(entry["description"])

    if entry.get("tags"):
        st.markdown("**Tags:** " + ", ".join(entry["tags"]))

    st.markdown(f"**Course:** {entry['course']}")
    st.divider()


# -----------------------------
# Notebook renderer
# -----------------------------
def render_notebook(path: Path):
    with path.open("r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    html_exporter = HTMLExporter()
    html_exporter.template_name = "classic"

    body, _ = html_exporter.from_notebook_node(nb)
    st.components.v1.html(body, height=900, scrolling=True)


# -----------------------------
# Course overview renderer
# -----------------------------
def render_course(entry, all_projects):
    st.subheader("📚 Assignments in this course")

    children = entry.get("children", [])
    lookup = {p["id"]: p for p in all_projects}

    cols = st.columns(2)

    for i, cid in enumerate(children):
        child = lookup.get(cid)
        if not child:
            continue

        with cols[i % 2]:
            st.markdown(f"### {child['title']}")
            st.caption(child.get("description", ""))

            if st.button("Open", key=f"open_{cid}"):
                st.session_state["selected_override"] = child
                st.rerun()


# import streamlit as st
# import nbformat
# from nbconvert import HTMLExporter

# def render_notebook(path):
#     with open(path, encoding="utf-8") as f:
#         nb = nbformat.read(f, as_version=4)

#     html_exporter = HTMLExporter()
#     body, _ = html_exporter.from_notebook_node(nb)
#     st.components.v1.html(body, height=800, scrolling=True)


# def render_metadata(entry):
#     st.markdown(f"### {entry['title']}")
#     st.caption(entry["description"])

#     st.markdown("**Tags:** " + ", ".join(entry.get("tags", [])))
#     st.markdown(f"**Course:** {entry['course']}")