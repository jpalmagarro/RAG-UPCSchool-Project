import streamlit as st
import os
import torch
from transformers import AutoTokenizer, AutoModel
import chromadb
from rank_bm25 import BM25Okapi
import numpy as np
from openai import OpenAI
import json
import logging

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="COSORA RAG Demo", page_icon="🏗️", layout="centered")

# --- SISTEMA DE LOGIN (Contraseña) ---
def check_password():
    """Devuelve True si el usuario ingresó la contraseña correcta."""
    def password_entered():
        # Leer la contraseña de las variables de entorno (o secrets de Streamlit)
        correct_password = os.getenv("APP_PASSWORD") or st.secrets.get("APP_PASSWORD")
        
        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # No guardar contraseña en plano
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.title("🔒 Acceso Restringido")
    st.text_input(
        "Introduce la contraseña para acceder a la demo:",
        type="password",
        on_change=password_entered,
        key="password"
    )
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Contraseña incorrecta")
    return False

if not check_password():
    st.stop()  # Detener ejecución si no está logueado

# --- PARÁMETROS GLOBALES ---
EMBED_MODEL_NAME = "intfloat/multilingual-e5-base"
CHROMA_PATH = os.getenv("CHROMA_PATH", "./data/chroma_db")
TOP_N = 5
RRF_K = 60
RRF_MIN_SCORE = 0.01

# --- CACHÉ DE RECURSOS (Para no recargar cada vez que el usuario pregunta) ---
@st.cache_resource
def load_resources():
    # 1. ChromaDB
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(name="cosora_actas_e5")
    
    # Extraer todos los documentos para BM25
    all_data = collection.get(include=["documents", "metadatas"])
    all_docs = all_data["documents"]
    all_metas = all_data["metadatas"]
    
    # 2. BM25
    tokenized_corpus = [doc.lower().split() for doc in all_docs]
    bm25 = BM25Okapi(tokenized_corpus)
    
    # 3. Embedding Model (E5) cargado de forma ESTRICTAMENTE local
    model_path = "./hf_model"
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModel.from_pretrained(model_path, local_files_only=True)
    
    # 4. OpenAI Client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("Falta la variable de entorno OPENAI_API_KEY.")
        st.stop()
    openai_client = OpenAI(api_key=api_key)
    
    return collection, all_docs, all_metas, bm25, tokenizer, model, openai_client

with st.spinner("Cargando la base de datos de actas y modelos..."):
    collection, all_docs, all_metas, bm25, tokenizer, model, openai_client = load_resources()

# --- LÓGICA DE RAG (De tu notebook) ---
def embed_query(text):
    text = f"query: {text}" # Prefijo necesario para E5
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :]
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
    return embeddings[0].numpy().tolist()

def retrieve_hybrid(query, top_n=TOP_N):
    # 1. Búsqueda Densa
    q_emb = embed_query(query)
    dense_results = collection.query(query_embeddings=[q_emb], n_results=top_n)
    dense_ids = dense_results["ids"][0]
    
    # 2. Búsqueda BM25
    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)
    top_bm25_indices = np.argsort(bm25_scores)[::-1][:top_n]
    
    # 3. RRF (Fusión)
    rrf_scores = {}
    
    # Procesar Dense
    for rank, doc_id in enumerate(dense_ids):
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + (1.0 / (RRF_K + rank + 1))
        
    # Procesar BM25
    for rank, idx in enumerate(top_bm25_indices):
        doc_id = all_metas[idx]["chunk_id"]
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0) + (1.0 / (RRF_K + rank + 1))
        
    # Ordenar y recuperar
    sorted_rrf = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    
    final_hits = []
    for doc_id, score in sorted_rrf:
        try:
            idx = next(i for i, meta in enumerate(all_metas) if meta["chunk_id"] == doc_id)
            final_hits.append({
                "score": score,
                "text": all_docs[idx],
                "meta": all_metas[idx]
            })
        except StopIteration:
            continue
            
    return final_hits

def ask_cosora(query):
    # Retrieve
    hits = retrieve_hybrid(query, top_n=TOP_N)
    
    # Filter
    if not hits or hits[0]["score"] < RRF_MIN_SCORE:
        return "No he encontrado información relevante en las actas para responder a tu pregunta.", []
        
    # Prompt
    context_blocks = []
    for i, chunk in enumerate(hits, 1):
        doc_id = chunk["meta"]["doc_id"]
        text = chunk["text"]
        context_blocks.append(f"--- Documento {i} (Origen: {doc_id}) ---\n{text}")
    context_str = "\n\n".join(context_blocks)
    
    system_prompt = (
        "Eres COSORA, un asistente experto en ingeniería civil especializado en actas de obra del Proyecto UPCSchool.\n"
        "Básate ÚNICAMENTE en el siguiente contexto extraído de actas oficiales para responder.\n"
        "Si la información no está en el contexto, di claramente 'No dispongo de esa información en las actas actuales'."
    )
    
    # Generate
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"CONTEXTO DE ACTAS:\n{context_str}\n\nPREGUNTA DEL USUARIO:\n{query}"}
        ],
        temperature=0.0
    )
    
    return response.choices[0].message.content, hits

# --- INTERFAZ DE USUARIO ---
st.title("🏗️ COSORA: Asistente de Actas de Obra")
st.markdown("Hazme cualquier pregunta sobre las actas de la obra Variante de Vallirana (Drenajes, Estructuras, Expropiaciones, etc.)")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("Ver fuentes documentales"):
                for source in message["sources"]:
                    st.caption(f"**Origen:** `{source['meta']['doc_id']}` (Score RRF: {source['score']:.4f})")
                    st.text(source['text'])

# Input del usuario
if prompt := st.chat_input("Ej: ¿Qué decisiones se tomaron sobre el talud?"):
    # Guardar y mostrar input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta
    with st.chat_message("assistant"):
        with st.spinner("Buscando en las actas..."):
            answer, sources = ask_cosora(prompt)
            st.markdown(answer)
            
            if sources:
                with st.expander("Ver fuentes documentales"):
                    for source in sources:
                        st.caption(f"**Origen:** `{source['meta']['doc_id']}` (Score RRF: {source['score']:.4f})")
                        st.text(source['text'])
                        
    # Guardar respuesta
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
