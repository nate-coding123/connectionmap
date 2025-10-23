import streamlit as st
from pyvis.network import Network
import random

st.set_page_config(page_title="Relationship Map", layout="wide")
st.title("🕸️ Relationship Map Builder")

# Initialize data structures
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
    st.session_state.relationships.append((name1, name2, relation))
    st.success(f"Added: {name1} — {relation} — {name2}")

# Create network
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
        title=rel,            # show label on hover
        color=style["color"],
        dashes=(style["style"] != "solid"),  # dotted/dashed lines
        width=2
    )

# Enable node interaction (click to focus)
net.set_options("""
var options = {
  edges: {
    smooth: false,
    arrows: { to: { enabled: false } },
    color: { inherit: false }
  },
  nodes: {
    shape: "dot",
    size: 15,
    font: { size: 14 }
  },
  interaction: {
    hover: true,
    tooltipDelay: 200,
    hideEdgesOnDrag: false,
    selectConnectedEdges: true
  },
  physics: {
    stabilization: true
  }
}
""")

# Render network
net.save_graph("relationship_map.html")
st.components.v1.html(open("relationship_map.html", "r", encoding="utf-8").read(), height=800)
