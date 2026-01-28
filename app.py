import streamlit as st
from openai import OpenAI

from database import get_sql_data
from embeddings import create_faiss_index, retrieve_docs

st.set_page_config(page_title="SQL RAG Chatbot", layout="wide")

st.markdown("""
<style>
.chatbox {
    background: #15192e;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 0 25px #7f8cff;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 SQL RAG Chatbot")

client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "http://localhost:8501",
        "X-Title": "SQL RAG Chatbot"
    }
)

@st.cache_resource
def load_data():
    texts = get_sql_data()
    index = create_faiss_index(texts)
    return texts, index

texts, index = load_data()

query = st.text_input("Ask a question from your SQL data:")

if query:
    docs = retrieve_docs(query, texts, index)

    prompt = f"""
You are a RAG assistant.
Answer ONLY using the context below.

Context:
{docs}

Question:
{query}
"""

    response = client.chat.completions.create(
    model="nvidia/nemotron-nano-12b-v2-vl:free",
    messages=[
        {
            "role": "system",
            "content": "You are a precise RAG assistant. Answer strictly from the provided context."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2,
    max_tokens=500
)

    st.markdown("<div class='chatbox'>", unsafe_allow_html=True)
    st.write(response.choices[0].message.content)
    st.markdown("</div>", unsafe_allow_html=True)
