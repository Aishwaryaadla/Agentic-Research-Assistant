# AgenticAI – Research Exploration Agent

Research Exploration Agent is an **AI-powered research exploration tool** that helps you **search, analyze, and visualize research papers** in an interactive way.  
It uses **Streamlit** for the UI, **transformers (Hugging Face)** for summarization, and **NetworkX / Matplotlib** for building research knowledge graphs.  

---

## 🚀 Features
-  Search research topics and fetch related papers from **arXiv**  
-  Automatically generate structured summaries (**Problem, Method, Results, Limitations**)  
-  Build a **knowledge graph** of extracted research concepts  
-  Visualize research connections interactively  
-  Simple, minimal **Streamlit web app**  

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/your-username/agenticai.git
cd agenticai

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# 3. Install dependencies
pip install -r requirements.txt


```
---

## ▶️ Usage
```bash 
# Run the Streamlit app
streamlit run app.py

```

Open the provided localhost URL in your browser.

---

## Project Structure

```bash

agenticai/
│── app.py                 # Main Streamlit application
│── requirements.txt       # Project dependencies
│── utils/
│   ├── arxiv_fetcher.py   # Fetch research papers from arXiv
│   ├── summarizer.py      # Hugging Face summarization pipeline
│   ├── graph_builder.py   # Knowledge graph creation (NetworkX)
│── static/
│   └── styles.css         # Optional custom styles
│── README.md              # Project documentation

```
---

## ⚙️ Dependencies
- **Python 3.8+**
- [Streamlit](https://streamlit.io/)
- [Transformers (Hugging Face)](https://huggingface.co/transformers/)
- [NetworkX](https://networkx.org/)
- [Matplotlib](https://matplotlib.org/)
- [arxiv](https://pypi.org/project/arxiv/)

```bash

pip install -r requirements.txt

```
---

## Example Workflow

1. Enter a research topic (e.g., Graph Neural Networks)

2. AgenticAI fetches the top relevant papers from arXiv

3. Each paper is automatically summarized into Problem, Method, Results, Limitations

4. A knowledge graph is generated showing relationships between concepts

5. Explore and visualize connections interactively

---


## 📜 License

This project is licensed under the MIT License – see the <a href = "https://github.com/Aishwaryaadla/Agentic-Research-Assistant/blob/main/LICENSE">LICENSE </a>file for details.
