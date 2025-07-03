import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# Prompt Template
template = """
Tu es un professeur de sciences au lycée. Sois clair, concis et pédagogue.
Explique les réponses en utilisant des exemples simples et un langage adapté aux élèves de 16 ans.

Voici des informations tirées d'un document fourni par l'utilisateur :
{doc_context}

Voici l'historique de la conversation :
{chat_context}

Question : {question}

Réponse :
"""
model = OllamaLLM(model = "mistral")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


# Streamlit App
st.set_page_config(page_title="Alexandra prof de Teccart", page_icon=":microscope:", layout="centered")
st.title(" 👩‍🏫 Alexandra, prof de Teccart")
