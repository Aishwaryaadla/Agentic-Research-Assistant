import streamlit as st
import arxiv
import re
import networkx as nx
import matplotlib.pyplot as plt
from transformers import pipeline
from pyvis.network import Network

# -----------------------
# Load Summarizer
# -----------------------
@st.cache_resource
def load_summarizer():
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn",
        device=-1   # Force CPU (avoids GPU/meta issues)
    )

summarizer = load_summarizer()


# -----------------------
# Helpers
# -----------------------
def clean_text(text: str) -> str:
    """Clean up whitespace and formatting."""
    return re.sub(r"\s+", " ", text).strip()

def structured_summary(text: str) -> dict:
    """
    Extract Problem, Method, Results, Limitations
    using summarizer prompts.
    """
    text = clean_text(text)

    prompts = {
        "Problem": f"Summarize the main problem this paper addresses: {text}",
        "Method": f"Summarize the method or approach used in this paper: {text}",
        "Results": f"Summarize the results or findings of this paper: {text}",
        "Limitations": f"Summarize the limitations of this paper: {text}",
    }

    fields = {}
    for key, q in prompts.items():
        try:
            ans = summarizer(q, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
            fields[key] = ans.strip()
        except Exception:
            fields[key] = "⚠️ Could not generate summary."
    return fields

def build_knowledge_graph(papers: list) -> nx.Graph:
    """Create a knowledge graph of papers and their extracted fields."""
    G = nx.Graph()

    for i, paper in enumerate(papers, start=1):
        paper_node = f"📄 {paper['title']}"
        G.add_node(paper_node, type="paper")

        for key, val in paper["summary"].items():
            concept_node = f"{key}: {val}"
            G.add_node(concept_node, type="concept")
            G.add_edge(paper_node, concept_node)

    return G

def draw_graph(G: nx.Graph):
    """Visualize the knowledge graph with matplotlib."""
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)

    node_colors = [
        "lightblue" if G.nodes[n]["type"] == "paper" else "lightgreen"
        for n in G.nodes
    ]

    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2500,
        font_size=9,
        font_weight="bold",
        edge_color="gray"
    )
    st.pyplot(plt)

def draw_graph_interactive(G, max_len=80):
    # Create a PyVis network
    net = Network(height="600px", width="100%", bgcolor="white", font_color="black")

    for node, data in G.nodes(data=True):
        color = "lightblue" if data["type"] == "paper" else "lightgreen"

        # Shorten label for readability
        short_label = node if len(node) <= max_len else node[:max_len] + "..."

        # Tooltip will show full text on hover
        net.add_node(node, label=short_label, title=node, color=color)

    for u, v in G.edges():
        net.add_edge(u, v)

    # Save and render
    net.save_graph("graph.html")
    with open("graph.html", "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=600, scrolling=True)


# -----------------------
# Streamlit UI
# -----------------------
st.title("📚 Agentic Research Assistant")
st.write("Search arXiv, extract structured summaries, and build a knowledge graph.")

query = st.text_input(
    "🔎 Enter a search query (e.g., 'graph neural networks healthcare')",
    ""
)

if st.button("Search") and query.strip():
    st.info(f"Searching arXiv for: **{query}**")

    search = arxiv.Search(
        query=query,
        max_results=3,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers = []

    for i, result in enumerate(search.results(), start=1):
        st.subheader(f"📄 Paper {i}: {result.title}")
        st.markdown(f"🔗 [Link to paper]({result.entry_id})")

        structured = structured_summary(result.summary)

        with st.expander("📌 Extracted Insights", expanded=True):
            st.write("**Problem:**", structured["Problem"])
            st.write("**Method:**", structured["Method"])
            st.write("**Results:**", structured["Results"])
            st.write("**Limitations:**", structured["Limitations"])

        papers.append({"title": result.title, "summary": structured})

    # Build and show knowledge graph
    if papers:
        st.subheader("🕸 Knowledge Graph of Extracted Concepts")
        G = build_knowledge_graph(papers)
        # draw_graph(G)
        draw_graph_interactive(G)
