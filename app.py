import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go
import time

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Tesla Quantum Nexus", layout="wide")

# ESTILO TESLA - INTERFACE DE COMANDO
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #050505; border-right: 2px solid #d4af37; }
    .stApp { background-color: #050505; color: #d4af37; }
    h1, h2, h3 { color: #d4af37; text-shadow: 2px 2px #000; }
    .stButton>button { border: 1px solid #d4af37; background-color: transparent; color: #d4af37; transition: 0.3s; }
    .stButton>button:hover { background-color: #d4af37; color: black; }
    </style>
    """, unsafe_allow_html=True)

# FUNÇÃO MATEMÁTICA DE TESLA
def reduzir_tesla(n):
    n_limpo = ''.join(filter(str.isdigit, str(n)))
    if not n_limpo: return 0
    soma = int(n_limpo)
    while soma > 9:
        soma = sum(int(d) for d in str(soma))
    return soma

# BARRA LATERAL (MENU VERTICAL)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2874/2874810.png", width=100) # Ícone de Energia
    st.title("NEXUS COMMAND")
    st.write("---")
    menu = st.radio("SELECIONE O MÓDULO:", 
                    ["🎰 Mapa de Loterias", "📖 Sabedoria Quântica", "₿ Terminal Cripto", "🌍 Radar Global"])
    st.write("---")
    st.write("**Operador:** Cristiano Noronha")

# MÓDULO 1: MAPA DE LOTERIAS (IA + ASTROLÁBIO)
if menu == "🎰 Mapa de Loterias":
    st.header("🎰 Algoritmo de Sugestão Quântica")
    st.subheader("Integração: Tesla 3-6-9 + Astrolábio de Precisão")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        tipo = st.selectbox("Selecione o Jogo:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
        processar = st.button("EXECUTAR CÁLCULO IA")

    with col2:
        if processar:
            with st.spinner('Sincronizando Astrolábio e Frequências...'):
                time.sleep(1.5)
                config = {
                    "Mega-Sena": (60, 6), "Lotofácil": (25, 15), 
                    "Quina": (80, 5), "Lotomania": (100, 20), "Milionária": (50, 6)
                }
                max_n, qtd = config[tipo]
                
                # Algoritmo: Filtra Tesla e completa com IA Quântica (Simulada por pesos)
                base_tesla = [n for n in range(1, max_n + 1) if reduzir_tesla(n) in [3, 6, 9]]
                sugestao = random.sample(base_tesla, min(len(base_tesla), qtd))
                
                st.code(f"CONFLUÊNCIA DETECTADA PARA {tipo.upper()}", language="markdown")
                st.write(f"### Números Sugeridos: {sorted(sugestao)}")
                st.caption("Cálculo baseado na posição vetorial 3-6-9 e entropia quântica.")

# MÓDULO 2: SABEDORIA
elif menu == "📖 Sabedoria Quântica":
    st.header("📖 Versículo e Decifrador")
    st.info("**Provérbios 16:3**: 'Consagre ao Senhor tudo o que você faz, e os seus planos serão bem-sucedidos.'")
    st.write("A inteligência financeira começa com a clareza espiritual e o alinhamento de metas.")

# MÓDULO 3: CRIPTO
elif menu == "₿ Terminal Cripto":
    st.header("₿ Monitoramento Bitcoin")
    data_btc = yf.download("BTC-USD", period="60d", interval="1d")
    fig = go.Figure(data=[go.Candlestick(x=data_btc.index, open=data_btc['Open'], high=data_btc['High'], low=data_btc['Low'], close=data_btc['Close'],
                    increasing_line_color='#d4af37', decreasing_line_color='#444')])
    fig.update_layout(template='plotly_dark', paper_bgcolor='black', plot_bgcolor='black')
    st.plotly_chart(fig, use_container_width=True)

# MÓDULO 4: GLOBAL
elif menu == "🌍 Radar Global":
    st.header("🌍 Ativos de Alto Valor")
    ativo = st.selectbox("Ativo:", ["GC=F", "SI=F", "HG=F", "PJP"], 
                        format_func=lambda x: {"GC=F":"Ouro", "SI=F":"Prata", "HG=F":"Cobre", "PJP":"Pharma"}[x])
    data_g = yf.download(ativo, period="30d", interval="1d")
    st.line_chart(data_g['Close'])
