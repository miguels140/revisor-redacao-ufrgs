# app.py
import streamlit as st
from textblob import TextBlob
import spacy
import os

st.set_page_config(page_title="Corretor de Redações UFRGS", layout="wide")

# Tenta carregar modelo português do spaCy, se não existir, baixa
try:
    nlp = spacy.load("pt_core_news_sm")
except OSError:
    os.system("python -m spacy download pt_core_news_sm")
    nlp = spacy.load("pt_core_news_sm")

# ---------------- Funções ----------------

def verificar_linhas(texto, min_linhas=20, max_linhas=30):
    linhas = texto.strip().split('\n')
    num_linhas = len([l for l in linhas if l.strip() != ''])
    dentro_limite = min_linhas <= num_linhas <= max_linhas
    return num_linhas, dentro_limite

def contar_palavras_chave(texto, palavras_chave):
    texto_lower = texto.lower()
    presentes = [p for p in palavras_chave if p.lower() in texto_lower]
    return presentes, len(presentes)

def analisar_gramatica(texto):
    blob = TextBlob(texto)
    erros = len(blob.correct().split()) - len(blob.words)
    return max(erros, 0)

def analisar_coesao(texto):
    conectivos = ["portanto", "entretanto", "além disso", "por outro lado", "assim"]
    presentes = [c for c in conectivos if c in texto.lower()]
    indice = len(presentes) / len(conectivos)
    return round(indice * 100, 1)  # %

def pontuar_redacao(texto):
    # Critérios simulados UFRGS: Conteúdo, Coesão, Linguagem, Estrutura
    conteudo = min(len(texto) / 500, 1) * 10
    coesao = analisar_coesao(texto) / 10
    gramatica = max(10 - analisar_gramatica(texto)/2, 0)
    estrutura = 10 if len(texto.split()) > 100 else 7
    
    nota_total = round((conteudo + coesao + gramatica + estrutura) / 4, 1)
    
    feedback = {
        "Conteúdo": round(conteudo, 1),
        "Coesão": round(coesao, 1),
        "Gramática": round(gramatica, 1),
        "Estrutura": estrutura,
        "Nota final estimada": nota_total
    }
    return feedback

# ---------------- Interface Streamlit ----------------

st.title("Corretor de Redações - UFRGS (Simulado)")

texto = st.text_area("Cole sua redação aqui:", height=300)
palavras_chave_input = st.text_input("Palavras-chave (separadas por vírgula):")
palavras_chave = [p.strip() for p in palavras_chave_input.split(',') if p.strip()]

min_linhas = st.number_input("Mínimo de linhas:", value=20)
max_linhas = st.number_input("Máximo de linhas:", value=30)

if st.button("Corrigir Redação"):
    if texto.strip() == "":
        st.warning("Digite sua redação para análise.")
    else:
        num_linhas, dentro_limite = verificar_linhas(texto, min_linhas, max_linhas)
        st.write(f"Número de linhas: {num_linhas} - Dentro do limite? {dentro_limite}")
        
        feedback = pontuar_redacao(texto)
        st.subheader("Notas por critério:")
        for k, v in feedback.items():
            st.write(f"{k}: {v}")
        
        if palavras_chave:
            presentes, total = contar_palavras_chave(texto, palavras_chave)
            st.subheader("Palavras-chave encontradas:")
            st.write(f"{presentes} ({total}/{len(palavras_chave)})")
        
        st.success("Análise concluída!")
