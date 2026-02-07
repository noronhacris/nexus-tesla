import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go

# CONFIGURAÇÃO DA PÁGINA (Layout Wide para ser Horizontal)
st.set_page_config(page_title="Tesla Quantum Nexus", layout="wide")

# ESTILO TESLA PERSONALIZADO
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #d4af37; }
    h1, h2, h3 { color: #d4af37; text-align: center; }
    .stTabs [data-baseweb="tab-list"] { display: flex; justify-content: center; }
    .css-1r6slb0 { border: 1px solid #d4af37; border-radius: 10px; padding: 10px; }
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

# ABAS HORIZONTAIS
tab1, tab2, tab3, tab4 = st.tabs(["💰 Loterias", "📖 Sabedoria", "💹 Cripto/BTC", "🌍 Radar Global"])

with tab1:
    st.header("🎰 Gerador de Frequências Lotéricas")
    col1, col2 = st.columns(2)
    with col1:
        tipo_loto = st.selectbox("Escolha a Loteria:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    
    config = {
        "Mega-Sena": (60, 6), "Lotofácil": (25, 15), 
        "Quina": (80, 5), "Lotomania": (100, 20), "Milionária": (50, 6)
    }
    
    with col2:
        if st.button("GERAR SEQUÊNCIA 3-6-9"):
            max_n, qtd = config[tipo_loto]
            nums = [n for n in range(1, max_n + 1) if reduzir_tesla(n) in [3, 6, 9]]
            sorteio = random.sample(nums, min(len(nums), qtd))
            st.success(f"Números Identificados para {tipo_loto}: {sorted(sorteio)}")

with tab2:
    st.header("📖 Versículo e Sabedoria do Dia")
    col_v1, col_v2 = st.columns([1, 2])
    with col_v1:
        st.info("**Provérbios 16:3**")
    with col_v2:
        st.write("*'Consagre ao Senhor tudo o que você faz, e os seus planos serão bem-sucedidos.'*")
        st.write("**Explicação:** Este versículo ensina que a prosperidade começa com a intenção e a organização. No Nexus, alinhar seus planos à frequência divina é o primeiro passo para o retorno financeiro.")

with tab3:
    st.header("₿ Gráfico Diário Bitcoin (BTC)")
    data_btc = yf.download("BTC-USD", period="60d", interval="1d")
    fig_btc = go.Figure(data=[go.Candlestick(x=data_btc.index, open=data_btc['Open'], high=data_btc['High'], low=data_btc['Low'], close=data_btc['Close'],
                    increasing_line_color='#d4af37', decreasing_line_color='#444')])
    fig_btc.update_layout(template='plotly_dark', paper_bgcolor='black', plot_bgcolor='black', height=400)
    st.plotly_chart(fig_btc, use_container_width=True)

with tab4:
    st.header("🌍 Radar de Ativos Estratégicos")
    col_a, col_b = st.columns(2)
    with col_a:
        ativo_nome = st.selectbox("Escolha o Ativo:", ["Ouro (GC=F)", "Prata (SI=F)", "Cobre (HG=F)", "S&P 500 (^GSPC)", "Farmacêutico (PJP)"])
    
    ticker = ativo_nome.split('(')[1].replace(')', '')
    data_g = yf.download(ticker, period="30d", interval="1d")
    st.area_chart(data_g['Close'])
    st.write(f"Monitorando: **{ticker}**")
