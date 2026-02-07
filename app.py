import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go
import time
from datetime import datetime

# =================================================================
# 1. CONFIGURAÇÃO DE INTERFACE E DESIGN DE ALTA FIDELIDADE
# =================================================================
st.set_page_config(
    page_title="Quantum Nexus Elite - Terminal de Estado", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Estilização CSS Expandida para Terminal de Elite (Design Viciante)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Profissional com Gradiente de Borda Áurea */
    [data-testid="stSidebar"] { 
        background-color: #050505; 
        border-right: 2px solid #d4af37; 
        box-shadow: 10px 0px 30px rgba(212, 175, 55, 0.1);
    }
    
    /* Botão de Execução Tesla com Efeito de Brilho e Pulso */
    .stButton>button { 
        border-radius: 12px; border: none; 
        background: linear-gradient(135deg, #d4af37 0%, #f9e295 100%); 
        color: #000 !important; font-weight: 800; text-transform: uppercase;
        width: 100%; height: 55px; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.3);
        margin-top: 15px;
    }
    .stButton>button:hover { 
        transform: scale(1.02); 
        box-shadow: 0px 8px 40px rgba(212, 175, 55, 0.6);
        background: linear-gradient(135deg, #f9e295 0%, #d4af37 100%);
    }
    
    /* Containers de Módulos (Cards Dinâmicos) */
    .card-quantum { 
        border-radius: 25px; background: linear-gradient(145deg, #111, #050505); 
        padding: 35px; border: 1px solid #222; margin-bottom: 30px;
        box-shadow: 15px 15px 40px rgba(0,0,0,0.7);
    }
    
    /* Tipografia de Autoridade */
    h1, h2, h3 { 
        color: #d4af37; 
        font-family: 'JetBrains Mono', monospace; 
        letter-spacing: 3px; 
        font-weight: 700; 
        text-transform: uppercase;
    }
    
    /* Estilização de Mensagens Neutras */
    .neutro-msg { 
        border-left: 8px solid #d4af37; padding: 35px; 
        background: linear-gradient(to right, #0a0a0a, #000); 
        line-height: 2.0; font-size: 1.15rem;
        border-radius: 0 25px 25px 0;
        box-shadow: 5px 5px 20px rgba(0,0,0,0.3);
    }

    /* Estilização de Métricas de Alta Performance */
    [data-testid="stMetricValue"] { 
        color: #d4af37 !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 2.3rem !important; 
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] { font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 2. MOTORES GRÁFICOS E ALGORITMOS (NÚCLEO DE INTELIGÊNCIA)
# =================================================================

def render_corretora_chart(ticker, nome):
    try:
        data = yf.download(ticker, period="90d", interval="1d", progress=False, auto_adjust=True)
        if data.empty:
            st.error(f"⚠️ Erro de Sincronização: O sinal de {nome} não foi detectado.")
            return

        fig = go.Figure(data=[go.Candlestick(
            x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
            increasing_line_color='#d4af37', decreasing_line_color='#ff4b4b',
            increasing_fillcolor='#d4af37', decreasing_fillcolor='#ff4b4b'
        )])
        
        fig.update_layout(
            template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', height=550,
            xaxis_rangeslider_visible=False,
            margin=dict(l=10, r=10, t=50, b=10),
            title=dict(text=f"TERMINAL ANALÍTICO: {nome.upper()}", font=dict(color='#d4af37', size=20))
        )
        st.plotly_chart(fig, use_container_width=True)
        
        m1, m2, m3, m4 = st.columns(4)
        atual = data['Close'].iloc[-1]
        anterior = data['Close'].iloc[-2]
        delta_p = ((atual - anterior) / anterior) * 100
        
        m1.metric("PREÇO ATUAL", f"{atual:.2f}")
        m2.metric("VARIAÇÃO 24H", f"{delta_p:.2f}%", delta=f"{delta_p:.2f}%")
        m3.metric("MÁXIMA (90D)", f"{data['High'].max():.2f}")
        m4.metric("MÍNIMA (90D)", f"{data['Low'].min():.2f}")
    except Exception as e:
        st.warning(f"Sinal de {nome} oscilando. Tentando reconexão...")

def logic_astrolabio_tesla(max_n, qtd, modalidade):
    with st.status("🌀 Sincronizando Astrolábio Quântico...", expanded=True) as status:
        time.sleep(2.5)
        random.seed(int(time.time() * 1000))
        vortex = [n for n in range(1, max_n + 1) if (n % 3 == 0 or n % 6 == 0 or n % 9 == 0)]
        pool = list(set(vortex + random.sample(range(1, max_n + 1), int(max_n * 0.45))))
        principais = sorted(random.sample(pool, qtd))
        
        if modalidade == "Milionária":
            trevos = sorted(random.sample(range(1, 7), 2))
            status.update(label="Vórtice Estabilizado: Trevos Identificados!", state="complete")
            return principais, trevos
        
        status.update(label="Frequência Harmônica Estabelecida!", state="complete")
        return principais, None

# =================================================================
# 3. SIDEBAR - COMANDO CENTRAL DO OPERADOR
# =================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>⚡ NEXUS ELITE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d4af37;'>SISTEMA DE ESTADO v4.1</p>", unsafe_allow_html=True)
    st.write("---")
    
    menu = st.radio(
        "COMANDOS DISPONÍVEIS:", 
        ["💎 IA Quântico Tesla", "🐾 Pet Global Intelligence", "💹 Trade & Commodities", 
         "👗 Fashion High-Ticket", "🌍 Soberania & Reservas", "🙏 Devocional de Poder", "🤝 Conselho de Elite"]
    )
    
    st.write("---")
    st.markdown("**Status do Sistema:** Operacional")
    st.markdown("**Nível de Acesso:** Senior Administrator")
    st.caption(f"Pulso Temporal: {datetime.now().strftime('%H:%M:%S')}")

# =================================================================
# 4. EXECUÇÃO DOS MÓDULOS
# =================================================================

if menu == "💎 IA Quântico Tesla":
    st.title("💎 IA Quântico Tesla & Astrolábio")
    st.markdown("<div class='card-quantum'>Algoritmo de análise universal baseado na Matemática de Vórtice (3-6-9) para decifrar padrões de confluência.</div>", unsafe_allow_html=True)
    col_j1, col_j2 = st.columns([2, 1])
    with col_j1:
        jogo = st.selectbox("Selecione a Modalidade Operacional:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    with col_j2:
        esfera = st.select_slider("Frequência (Hz):", options=[369, 432, 528, 963])

    if st.button("EXECUTAR CONFLUÊNCIA DE VÓRTICE"):
        configs = {"Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5), "Lotomania": (100, 50), "Milionária": (50, 6)}
        n_max, n_qtd = configs[jogo]
        nums, trevos = logic_astrolabio_tesla(n_max, n_qtd, jogo)
        st.markdown(f"<div class='card-quantum' style='text-align: center; border: 2px solid #d4af37;'><h3>NÚMEROS IDENTIFICADOS</h3><h1 style='font-size: 3.8rem; color: #FFF;'>{', '.join(map(str, nums))}</h1></div>", unsafe_allow_html=True)
        if trevos:
            st.markdown(f"<div style='text-align: center;'><h2>☘️ TREVOS DA SORTE: {trevos[0]} e {trevos[1]}</h2></div>", unsafe_allow_html=True)

elif menu == "🐾 Pet Global Intelligence":
    st.title("🐾 Pet Global Intelligence")
    pet_t = st.selectbox("Analise o Ativo Pet:", ["PETZ3.SA (Petz BR)", "ZTS (Zoetis)", "CHWY (Chewy)", "IDXX (IDEXX Labs)"])
    render_corretora_chart(pet_t.split(" (")[1].replace(")", ""), pet_t)
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        fig_p1 = go.Figure(data=[go.Pie(labels=['Mars', 'Purina', 'Zoetis', 'Hills', 'Outros'], values=[32, 28, 14, 11, 15], hole=.5)])
        st.plotly_chart(fig_p1)
    with col_p2:
        fig_p2 = go.Figure(data=[go.Pie(labels=['Petz', 'Cobasi', 'Petlove', 'Outros'], values=[38, 27, 15, 20], hole=.5)])
        st.plotly_chart(fig_p2)

elif menu == "💹 Trade & Commodities":
    st.title("💹 Terminal de Trading Profissional")
    t_ativo = st.selectbox("Escolha o Ativo:", ["BTC-USD (Bitcoin)", "ETH-USD (Ethereum)", "USDBRL=X (Dólar)", "EURBRL=X (Euro)"])
    render_corretora_chart(t_ativo.split(" (")[1].replace(")", ""), t_ativo)

elif menu == "👗 Fashion High-Ticket":
    st.title("👗 Radar Fashion Luxo & Market Share")
    f_marca = st.selectbox("Analise a Gigante do Luxo:", ["MC.PA (LVMH)", "RMS.PA (Hermès)", "NKE (Nike)", "ARZZ3.SA (Arezzo)"])
    render_corretora_chart(f_marca.split(" (")[1].replace(")", ""), f_marca)

elif menu == "🌍 Soberania & Reservas":
    st.title("🌍 Soberania Nacional e Reservas Mundiais")
    reserva = st.selectbox("Commodity Estratégica:", ["GC=F (Ouro)", "SI=F (Prata)", "BZ=F (Petróleo Brent)", "VALE (Nióbio/Mineradora)"])
    render_corretora_chart(reserva.split(" (")[1].replace(")", ""), reserva)

elif menu == "🙏 Devocional de Poder":
    st.title("🙏 Sabedoria, Propósito e Legado")
    st.markdown("<div class='neutro-msg'><h2 style='text-align: center;'>O FUNDAMENTO DA VERDADEIRA RIQUEZA</h2><p align='center'><i>'Minha é a prata, e meu é o ouro, diz o Senhor dos Exércitos...'</i></p><p>A compreensão de que os recursos globais possuem um dono soberano redefine a forma como operamos. Gestão e domínio são as chaves.</p></div>", unsafe_allow_html=True)

elif menu == "🤝 Conselho de Elite":
    st.title("🤝 Conselho de Elite: Alianças e Blindagem")
    st.markdown("<div class='card-quantum'>Foco na expansão estratégica e na preservação de ativos.</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.checkbox("Consolidação de Reservas", value=True)
        st.checkbox("Otimização E-commerce Pet")
    with c2:
        st.info("A paciência é o ativo mais escasso do mercado.")
