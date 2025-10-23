import streamlit as st
from pyvis.network import Network

st.set_page_config(page_title="Relationship Map", layout="wide")
st.title("🕸️ Relationship Map Builder")

# Create PyVis network
net = Network(height="700px", width="100%", bgcolor="#ffffff", font_color="black", directed=False)
net.toggle_physics(True)  # enable zoom and movement

# Persist data in session
if "relationships" not in st.session_state:
    st.session_state.relationships = []

with st.form("add_relationship"):
    col1, col2, col3 = st.columns(3)
    with col1:
        name1 = st.text_input("First name")
    with col2:
        name2 = st.text_input("Second name")
    with col3:
        relation = st.text_input("Relationship (e.g. friends, dating)")
    submitted = st.form_submit_button("Add Relationship")

if submitted and name1 and name2 and relation:
    st.session_state.relationships.append((name1, name2, relation))
    st.success(f"Added: {name1} — {relation} — {name2}")

# Build graph
for n1, n2, rel in st.session_state.relationships:
    net.add_node(n1, label=n1)
    net.add_node(n2, label=n2)
    net.add_edge(n1, n2, title=rel, label=rel)

# Display network
net.save_graph("relationship_map.html")
st.components.v1.html(open("relationship_map.html", "r", encoding="utf-8").read(), height=750)
