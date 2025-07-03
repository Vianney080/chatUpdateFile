import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# ---------- Prompt ----------
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

model  = OllamaLLM(model="mistral")
prompt = ChatPromptTemplate.from_template(template)
chain  = prompt | model

# ---------- Streamlit ----------
st.set_page_config("Alexandra prof de Teccart", ":microscope:", layout="centered")
st.title("👩‍🏫 Alexandra, prof de Teccart")

# État de session
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("doc_text", "")

# -- Chargement de document --------------------------------------------------
with st.sidebar:
    st.header("Charger un document")
    uploaded = st.file_uploader("Télécharger .txt / .pdf / .docx", type=["txt", "pdf", "docx"])
    if uploaded:
        ext = uploaded.name.lower().split(".")[-1]

        if ext == "pdf":
            from pypdf import PdfReader
            reader = PdfReader(uploaded)
            text = "\n".join(p.extract_text() or "" for p in reader.pages)

        elif ext == "docx":
            import docx
            doc  = docx.Document(uploaded)
            text = "\n".join(p.text for p in doc.paragraphs)

        else:  # .txt
            text = uploaded.read().decode("utf-8")

        st.session_state.doc_text = text.strip()[:20_000]
        st.success("Document chargé ! Posez maintenant vos questions ↓")

# -- Affichage de l’historique ----------------------------------------------
for speaker, msg in st.session_state.chat_history:
    avatar = "🧑" if speaker == "Vous" else "👩‍🏫"
    st.markdown(f"**{avatar} {speaker}** : {msg}")

# -- Entrée utilisateur et génération ---------------------------------------
user_input = st.chat_input("Posez votre question…")

if user_input:
    with st.spinner("Alexandra réfléchit…"):
        result = chain.invoke(
            {
                "doc_context": st.session_state.doc_text or "Aucun document fourni.",
                "chat_context": "\n".join(f"{s}: {m}" for s, m in st.session_state.chat_history),
                "question": user_input          # ✅ fourni !
            }
        )

    # Mettre à jour l’historique
    st.session_state.chat_history.extend([("Vous", user_input),
                                          ("Alexandra", result)])

    st.success(result)
