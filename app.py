import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Tesla Quantum Nexus", layout="wide")

# ESTILO TESLA (PRETO E DOURADO)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #d4af37; }
    .stButton>button { background-color: #d4af37; color: black; border-radius: 10px; width: 100%; }
    h1, h2, h3 { color: #d4af37; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ TESLA QUANTUM NEXUS")
st.write("<p style='text-align: center;'>Operador: Cristiano Daniel de Noronha</p>", unsafe_allow_html=True)

# FUNÇÃO MATEMÁTICA DE TESLA
def reduzir_tesla(n):
    n_limpo = ''.join(filter(str.isdigit, str(n)))
    if not n_limpo: return 0
    soma = int(n_limpo)
    while soma > 9:
        soma = sum(int(d) for d in str(soma))
    return soma

# ABAS DO SISTEMA
tab1, tab2, tab3, tab4 = st.tabs(["🎰 Loteria", "📜 Bíblia", "₿ Cripto", "📊 Mercado Pet"])

with tab1:
    st.header("Frequência de Sorte (Vórtice)")
    if st.button("GERAR NÚMEROS 3-6-9"):
        nums = [n for n in range(1, 61) if reduzir_tesla(n) in [3, 6, 9]]
        sorteio = random.sample(nums, 6)
        st.success(f"Números Identificados: {sorted(sorteio)}")

with tab2:
    st.header("Decifrador de Frequência Bíblica")
    texto = st.text_input("Digite o nome ou versículo:")
    if texto:
        res = reduzir_tesla(sum(ord(c) for c in texto))
        st.metric("Vibração Numérica", res)
        if res == 9: st.warning("ALERTA: Confluência Ponto Zero Detectada!")

with tab3:
    st.header("Monitoramento Cripto em Tempo Real")
    moeda = st.selectbox("Escolha a Moeda:", ["BTC-USD", "ETH-USD", "SOL-USD"])
    
    # Gráfico em Tempo Real
    data = yf.download(moeda, period="7d", interval="1h")
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
                    increasing_line_color='#d4af37', decreasing_line_color='#444')])
    fig.update_layout(template='plotly_dark', paper_bgcolor='black', plot_bgcolor='black')
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.header("E-commerce & Renda Extra (Pet)")
    st.write("Análise de Nicho: Acessórios Inteligentes para Pets")
    st.info("Estratégia: Focar em produtos com valor final que reduza a 3, 6 ou 9 para aumentar conversão psíquica.")
