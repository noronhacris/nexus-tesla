import streamlit as st
import random

# IDENTIDADE DO OPERADOR
OPERADOR = "Cristiano Daniel de Noronha"

st.set_page_config(page_title="Tesla Quantum Nexus", page_icon="⚡")

st.markdown(f"""
    <style>
    .stApp {{ background-color: #050505; color: #00e5ff; }}
    .stButton>button {{ background-color: #d4af37; color: black; font-weight: bold; border-radius: 20px; width: 100%; }}
    h1, h2, h3 {{ color: #d4af37; text-align: center; }}
    </style>
    <h1 style='text-align: center;'>⚡ TESLA QUANTUM NEXUS</h1>
    <p style='text-align: center;'>Operador: {OPERADOR}</p>
    """, unsafe_allow_html=True)

def reduzir_tesla(n):
    # Remove qualquer caractere que não seja número (pontos, vírgulas, etc)
    n_limpo = ''.join(filter(str.isdigit, str(n)))
    if not n_limpo: return 0
    soma = sum(int(d) for d in n_limpo)
    while soma > 9:
        soma = sum(int(d) for d in str(soma))
    return soma

tabs = st.tabs(["🎰 Loteria", "📜 Bíblia", "₿ Cripto", "📊 Mercado"])

with tabs[0]:
    st.subheader("Frequência de Sorte (Vórtice)")
    if st.button("GERAR NÚMEROS 3-6-9"):
        # Filtra apenas números cuja redução de Tesla seja 3, 6 ou 9
        numeros_vortex = [n for n in range(1, 61) if reduzir_tesla(n) in [3,6,9]]
        escolhidos = sorted(random.sample(numeros_vortex, 6))
        st.success(f"Sequência Harmônica: {escolhidos}")

with tabs[1]:
    st.subheader("Decifrador Bíblico")
    texto = st.text_input("Digite o versículo ou palavra sagrada:")
    if texto:
        # Soma o valor ASCII de cada letra e reduz
        valor_total = sum(ord(c) for c in texto)
        res = reduzir_tesla(valor_total)
        st.info(f"Vibração Numérica: {res}")
        if res == 9: 
            st.warning("⚠️ CONFLUÊNCIA DIVINA DETECTADA (9)")

with tabs[2]:
    st.subheader("Análise de Cripto")
    p = st.number_input("Insira o Preço Atual da Moeda:", value=0.0, format="%.2f")
    if p > 0:
        res = reduzir_tesla(p)
        st.write(f"Raiz de Tesla do Preço: **{res}**")
        if res == 9: 
            st.balloons()
            st.success("💎 PONTO ZERO (9): Oportunidade de Confluência Quântica!")

with tabs[3]:
    st.subheader("Mercado Futuro Global")
    st.write("Monitorando ciclos de 3, 6 e 9 horas...")
    st.write(f"Status: Ativo para Operador {OPERADOR}")
