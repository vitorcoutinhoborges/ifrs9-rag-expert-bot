# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 15:14:14 2026

@author: vitor.borges
"""

import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# --- Configurações da Página ---
st.set_page_config(page_title="Expert IFRS 9", page_icon="⚖️", layout="centered")

st.title("⚖️ IFRS 9 Specialist Bot")
st.markdown("Assistente inteligente para consulta da norma técnica IFRS 9.")

api_key = st.secrets.get("GOOGLE_API_KEY") 

if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key

# --- Lógica de Carregamento (Cache para performance) ---
@st.cache_resource
def init_rag():
    # Tradutor local (Grátis e sem limites)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    # Carrega a base que veio do Databricks
    vector_db = FAISS.load_local("ifrs9_index_local", embeddings, allow_dangerous_deserialization=True)
    return vector_db.as_retriever(search_kwargs={"k": 3})

# --- Execução do Chat ---
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    retriever = init_rag()
    
    # Prompt de Especialista
    template = """Você é um Consultor Especialista em IFRS 9. Use o contexto para responder Seja breve em sua resposta e traga sempre a fonte.
    Contexto: {context}
    Pergunta: {question}
    Resposta Técnica (em Português):"""
    
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.1)
    
    # Chain LCEL
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Interface de Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_input := st.chat_input("Ex: Como funciona a perda esperada?"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Consultando a norma..."):
                response = rag_chain.invoke(user_input)
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
else:

    st.warning("⚠️ Adicione sua Google API Key na barra lateral para começar.")

