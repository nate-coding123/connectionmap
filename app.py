import streamlit as st
from pyvis.network import Network
import random

# Streamlit page setup
st.set_page_config(page_title="Relationship Map", layout="wide")
st.title("🕸️ Interactive Relationship Map")

# Initialize persistent session data
if "relationships" not in st.session_state:
    st.session_state.relationships = []
if "styles" not in st.session_state:
    st.session_state.styles = {}

# Random color generator
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Random edge style generator
def random_style():
    styles = ["solid", "dash", "dot", "dash-dot"]
    return random.choice(styles)

# Input form
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
    st.session_state.relationships.append((name1.strip(), name2.strip(), relation.strip()))
    st.success(f"Added: {name1} — {relation} — {name2}")

# Create the PyVis network
net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="black")
net.toggle_physics(True)

# Assign colors/styles for each relationship type
for _, _, rel in st.session_state.relationships:
    if rel not in st.session_state.styles:
        st.session_state.styles[rel] = {
            "color": random_color(),
            "style": random_style()
        }

# Build the graph
for n1, n2, rel in st.session_state.relationships:
    style = st.session_state.styles[rel]
    net.add_node(n1, label=n1)
    net.add_node(n2, label=n2)
    net.add_edge(
        n1,
        n2,
        title=rel,                # shows label only on hover
        color=style["color"],
        dashes=(style["style"] != "solid"),  # dotted/dashed line if not solid
        width=2
    )

# Proper JSON options for PyVis (no 'var options'!)
net.set_options("""
{
  "edges": {
    "smooth": false,
    "arrows": { "to": { "enabled": false } },
    "color": { "inherit": false }
  },
  "nodes": {
    "shape": "dot",
    "size": 15,
    "font": { "size": 14 }
  },
  "interaction": {
    "hover": true,
    "tooltipDelay": 200,
    "hideEdgesOnDrag": false,
    "selectConnectedEdges": true,
    "zoomView": true,
    "dragView": true
  },
  "physics": {
    "stabilization": true
  }
}
""")

# Generate and display the network graph
net.save_graph("relationship_map.html")
html_file = open("relationship_map.html", "r", encoding="utf-8")
st.components.v1.html(html_file.read(), height=800)
html_file.close()

# Show color legend under the graph
if st.session_state.styles:
    st.subheader("Legend")
    for rel, style in st.session_state.styles.items():
        st.markdown(f"- <span style='color:{style['color']}'><b>{rel}</b></span> ({style['style']})", unsafe_allow_html=True)
