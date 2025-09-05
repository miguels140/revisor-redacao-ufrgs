import streamlit as st
from textblob import TextBlob

st.title("Corretor de Redações UFRGS (Versão Gratuita)")

# Entrada do usuário
tema = st.text_input("Informe o tema da redação:")
texto = st.text_area("Cole sua redação aqui:")

# Funções auxiliares
def contar_linhas(texto):
    linhas = [l for l in texto.strip().split("\n") if l.strip() != ""]
    return len(linhas)

def extrair_palavras_chave(texto):
    blob = TextBlob(texto)
    keywords = [word.lower() for (word, tag) in blob.tags if tag.startswith('NN')]
    return list(set(keywords))

def avaliar_redacao(texto, tema):
    feedback = {}
    
    # Linhas
    linhas = contar_linhas(texto)
    if linhas < 25:
        estrutura = 5
        feedback['Estrutura'] = f"Redação muito curta ({linhas} linhas)."
    elif linhas > 30:
        estrutura = 6
        feedback['Estrutura'] = f"Redação muito longa ({linhas} linhas)."
    else:
        estrutura = 8
        feedback['Estrutura'] = f"Redação dentro do tamanho adequado ({linhas} linhas)."
    
    # Tema
    if tema.lower() in texto.lower():
        conteudo = 8
        tema_cumprido = "Sim"
        feedback['Conteúdo'] = "Texto adequado ao tema."
    else:
        conteudo = 4
        tema_cumprido = "Não"
        feedback['Conteúdo'] = "O texto não está totalmente relacionado ao tema."
    
    # Linguagem
    blob = TextBlob(texto)
    erros_ort = len(blob.correct().split()) - len(texto.split())
    if erros_ort <= 2:
        linguagem = 7
        feedback['Linguagem'] = "Poucos erros gramaticais."
    elif erros_ort <= 5:
        linguagem = 5
        feedback['Linguagem'] = f"Alguns erros gramaticais ({erros_ort} erros)."
    else:
        linguagem = 3
        feedback['Linguagem'] = f"Muitos erros gramaticais ({erros_ort} erros)."
    
    # Argumentação/Coesão
    sentencas = blob.sentences
    media_palavras = sum(len(s.words) for s in sentencas)/len(sentencas) if len(sentencas)>0 else 0
    if media_palavras > 10:
        argumentacao = 7
        feedback['Argumentação'] = "Boa argumentação e coesão."
    else:
        argumentacao = 4
        feedback['Argumentação'] = "Fraca argumentação; frases muito curtas."
    
    # Nota final
    nota_final = conteudo + estrutura + linguagem + argumentacao
    palavras_chave = extrair_palavras_chave(texto)
    
    return {
        "nota": round(nota_final,1),
        "feedback": feedback,
        "palavras_chave": palavras_chave,
        "linhas": linhas,
        "tema_cumprido": tema_cumprido
    }

# Botão de correção
if st.button("Corrigir Redação"):
    if not texto.strip() or not tema.strip():
        st.warning("Preencha o tema e a redação.")
    else:
        resultado = avaliar_redacao(texto, tema)
        st.subheader(f"Nota final: {resultado['nota']}/30")
        st.subheader("Feedback detalhado:")
        for crit, msg in resultado['feedback'].items():
            st.write(f"**{crit}**: {msg}")
        st.subheader("Palavras-chave detectadas:")
        st.write(", ".join(resultado['palavras_chave']))
        st.write(f"Número de linhas: {resultado['linhas']}")
        st.write(f"Tema cumprido: {resultado['tema_cumprido']}")
