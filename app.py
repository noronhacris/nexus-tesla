import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go
import time
from datetime import datetime

# CONFIGURAÇÃO DE INTERFACE PROFISSIONAL
st.set_page_config(page_title="Tesla Quantum Nexus", layout="wide", initial_sidebar_state="expanded")

# CSS ESTILO MODERN UI (INSTAGRAM DARK MODE)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #E1E1E1; }
    [data-testid="stSidebar"] { background-image: linear-gradient(#050505, #121212); border-right: 1px solid #333; }
    .stButton>button { border-radius: 20px; border: 1px solid #d4af37; background: transparent; color: #d4af37; font-weight: bold; width: 100%; }
    .stButton>button:hover { background: #d4af37; color: black; box-shadow: 0px 0px 15px #d4af37; }
    .css-1r6slb0 { border-radius: 15px; border: 1px solid #222; background-color: #111; padding: 20px; }
    h1, h2 { font-family: 'Helvetica Neue', sans-serif; letter-spacing: -1px; }
    </style>
    """, unsafe_allow_html=True)

# LÓGICA TESLA + NOSTRADAMUS
def algoritmo_nostradamus(max_n, qtd):
    seed = int(time.time()) # Semente baseada no tempo real (Astrolábio)
    random.seed(seed)
    # Filtro Tesla 3-6-9
    base_vortex = [n for n in range(1, max_n + 1) if (n % 9 in [3, 6, 0])]
    # Mistura IA Quântica
    pool = base_vortex + random.sample(range(1, max_n + 1), qtd)
    return sorted(random.sample(list(set(pool)), qtd))

# BARRA LATERAL ESTILO APP
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>NEXUS</h2>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("NAVEGAÇÃO", ["🎰 Loterias", "💹 Trade Center", "🌍 Mercado Global", "📖 Sabedoria"])
    st.write("---")
    st.caption("v2.0 Beta - Operador Cristiano")

# MÓDULO 1: LOTERIAS (CONFLUÊNCIA TOTAL)
if menu == "🎰 Loterias":
    st.title("🎰 Algoritmo Nostradamus 3-6-9")
    jogo = st.selectbox("Selecione a Modalidade:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    
    if st.button("CALCULAR CONFLUÊNCIA"):
        with st.status("Sincronizando Astrolábio...", expanded=True) as status:
            time.sleep(1)
            st.write("Analisando Entropia Quântica...")
            time.sleep(1)
            
            config = {
                "Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5),
                "Lotomania": (100, 50), "Milionária": (50, 6)
            }
            max_n, qtd = config[jogo]
            resultado = algoritmo_nostradamus(max_n, qtd)
            
            st.write("### Sugestão Gerada:")
            st.info(f"**Números:** {resultado}")
            if jogo == "Milionária":
                st.warning(f"**Trevos sugeridos:** {random.sample(range(1, 7), 2)}")
            status.update(label="Cálculo Finalizado!", state="complete")

# MÓDULO 2: TRADE CENTER (BTC + AÇÕES)
elif menu == "💹 Trade Center":
    st.title("₿ Terminal de Investimentos")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        ativo = st.selectbox("Ativo para Análise:", ["BTC-USD", "AAPL", "GOOGL", "AMZN", "VALE3.SA"])
        data = yf.download(ativo, period="60d", interval="1d")
        fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
                        increasing_line_color='#00ff00', decreasing_line_color='#ff0000')])
        fig.update_layout(template='plotly_dark', paper_bgcolor='black', plot_bgcolor='black')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sugestão IA")
        preco_atual = data['Close'][-1]
        st.metric("Preço Atual", f"${preco_atual:.2f}")
        if preco_atual < data['Close'].mean():
            st.success("SINAL: COMPRA (Abaixo da média)")
        else:
            st.error("SINAL: AGUARDAR")

# MÓDULO 3: MERCADO GLOBAL
elif menu == "🌍 Mercado Global":
    st.title("🌍 Radar Global de Commodities e Moedas")
    ativos_globais = {
        "Dólar (BRL)": "USDBRL=X", "Euro (USD)": "EURUSD=X", "Ouro": "GC=F",
        "Prata": "SI=F", "Cobre": "HG=F", "Nióbio (Proxy Vale)": "VALE"
    }
    escolha = st.multiselect("Selecione os itens para comparar:", list(ativos_globais.keys()), default=["Dólar (BRL)", "Ouro"])
    
    for item in escolha:
        ticker = ativos_globais[item]
        d_global = yf.download(ticker, period="30d")
        st.write(f"**{item}**")
        st.line_chart(d_global['Close'])

# MÓDULO 4: SABEDORIA
else:
    st.title("📖 Sabedoria e Propósito")
    st.subheader("Versículo do Dia")
    st.info("**Mateus 7:7** - 'Peçam, e lhes será dado; busquem, e encontrarão; batam, e a porta será aberta para vocês.'")
    st.write("A busca pela riqueza global exige persistência e o uso das ferramentas certas. O Nexus é o seu cajado tecnológico.")
