import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go
import time
import pandas as pd
from datetime import datetime, timedelta

# =================================================================
# 1. CONFIGURAÇÃO DE ALTA PERFORMANCE E CABEÇALHO DO SISTEMA
# =================================================================
st.set_page_config(
    page_title="Quantum Nexus Elite - Terminal de Estado", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# =================================================================
# 2. ESTILIZAÇÃO VISUAL CUSTOMIZADA (CSS DE ELITE)
# =================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 2px solid #d4af37; box-shadow: 10px 0px 40px rgba(212, 175, 55, 0.15); }
    h1, h2, h3 { color: #d4af37; font-family: 'JetBrains Mono', monospace; letter-spacing: 4px; text-transform: uppercase; font-weight: 700; }
    
    .stButton>button { 
        border-radius: 15px; border: 1px solid #d4af37; background: linear-gradient(135deg, #1a1a1a 0%, #000 100%); 
        color: #d4af37 !important; font-weight: 800; text-transform: uppercase; letter-spacing: 2px;
        width: 100%; height: 65px; transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover { 
        transform: translateY(-5px); background: linear-gradient(135deg, #d4af37 0%, #f9e295 100%); color: #000 !important;
    }
    
    .card-quantum { border-radius: 30px; background: linear-gradient(145deg, #0f0f0f, #050505); padding: 40px; border: 1px solid #222; margin-bottom: 30px; }
    [data-testid="stMetricValue"] { color: #d4af37 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 2.8rem !important; }
    .state-message { border-left: 10px solid #d4af37; padding: 40px; background: rgba(10, 10, 10, 0.8); line-height: 2.4; font-size: 1.25rem; border-radius: 0 40px 40px 0; margin: 20px 0; }
    
    #MainMenu, footer, header {visibility: hidden;}
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #d4af37; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 3. MOTORES ANALÍTICOS (NÚCLEO DE DADOS)
# =================================================================

def render_corretora_chart(ticker, nome):
    try:
        data = yf.download(ticker, period="90d", interval="1d", progress=False, auto_adjust=True)
        if data.empty:
            st.error(f"⚠️ FALHA NA SINCRONIZAÇÃO: {nome} está fora de alcance.")
            return

        fig = go.Figure(data=[go.Candlestick(
            x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
            increasing_line_color='#d4af37', decreasing_line_color='#ff4b4b',
            increasing_fillcolor='#d4af37', decreasing_fillcolor='#ff4b4b', name="Preço"
        )])
        fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=580, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        atual = data['Close'].iloc[-1]
        anterior = data['Close'].iloc[-2]
        delta_perc = ((atual - anterior) / anterior) * 100
        
        m1, m2, m3 = st.columns(3)
        m1.metric("PREÇO ATUAL", f"{atual:.2f}")
        m2.metric("VARIAÇÃO DIA", f"{delta_perc:.2f}%")
        m3.metric("MÁXIMA 90D", f"{data['High'].max():.2f}")
    except:
        st.warning("🔄 Reconectando ao servidor de dados...")

def logic_astrolabio_tesla(max_n, qtd, modalidade):
    with st.status("🌀 SINCRO-VÓRTICE ATIVO...", expanded=True) as status:
        time.sleep(1)
        random.seed(int(time.time() * 1000))
        populacao_total = list(range(1, max_n + 1))
        vortex_base = [n for n in populacao_total if (n % 3 == 0 or n % 6 == 0 or n % 9 == 0)]
        
        if qtd > len(vortex_base):
            vortex_base = vortex_base + random.sample(list(set(populacao_total) - set(vortex_base)), qtd - len(vortex_base))
        
        selecionados = sorted(random.sample(vortex_base, qtd))
        trevos = sorted(random.sample(range(1, 7), 2)) if modalidade == "Milionária" else None
        status.update(label="CONFLUÊNCIA ESTABELECIDA!", state="complete")
        return selecionados, trevos

# =================================================================
# 4. SIDEBAR - PAINEL DE COMANDO
# =================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>⚡ NEXUS ELITE</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("COMANDOS DISPONÍVEIS:", ["💎 IA Quântico Tesla", "💹 Trade & Commodities", "👗 Fashion High-Ticket", "🌍 Soberania & Reservas", "🙏 Devocional de Poder", "🤝 Conselho de Elite"])
    st.write("---")
    st.caption(f"Execução: {datetime.now().strftime('%H:%M:%S')}")

# =================================================================
# 5. EXECUÇÃO DOS MÓDULOS
# =================================================================

if menu == "💎 IA Quântico Tesla":
    st.title("💎 IA Quântico Tesla")
    jogo = st.selectbox("Modalidade:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    esfera = st.select_slider("Frequência (Hz):", options=[369, 432, 528, 963])

    if st.button("EXECUTAR CONFLUÊNCIA DE VÓRTICE"):
        configs = {"Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5), "Lotomania": (100, 50), "Milionária": (50, 6)}
        n_max, n_qtd = configs[jogo]
        nums, trevos = logic_astrolabio_tesla(n_max, n_qtd, jogo)
        
        st.markdown(f"<div class='card-quantum' style='text-align: center; border: 2px solid #d4af37;'><h1>{', '.join(map(str, nums))}</h1></div>", unsafe_allow_html=True)
        if jogo == "Milionária":
            st.success(f"☘️ TREVOS: {trevos[0]} e {trevos[1]}")

elif menu == "💹 Trade & Commodities":
    st.title("💹 Trade & Commodities")
    t_ativo = st.selectbox("Ativo:", ["BTC-USD", "ETH-USD", "USDBRL=X", "GC=F"])
    render_corretora_chart(t_ativo, t_ativo)

elif menu == "👗 Fashion High-Ticket":
    st.title("👗 Fashion High-Ticket")
    f_marca = st.selectbox("Marca:", ["MC.PA (LVMH)", "RMS.PA (Hermès)", "ARZZ3.SA (Arezzo)"])
    render_corretora_chart(f_marca.split(" (")[1].replace(")", ""), f_marca)

elif menu == "🌍 Soberania & Reservas":
    st.title("🌍 Soberania & Reservas")
    reserva_sel = st.selectbox("Ativo Estratégico:", ["GC=F (Ouro)", "VALE3.SA (Vale/Nióbio)", "PETR4.SA (Petrobras)"])
    render_corretora_chart(reserva_sel.split(" (")[1].replace(")", ""), reserva_sel)
    
    st.markdown("<div class='state-message'><b>ANÁLISE:</b> O controle do Nióbio e Ouro é a base da soberania nacional.</div>", unsafe_allow_html=True)

elif menu == "🙏 Devocional de Poder":
    st.title("🙏 Devocional de Poder")
    st.markdown("<div class='state-message'><h3>O PRINCÍPIO DA DEPENDÊNCIA</h3><p>Toda riqueza vem da Fonte Primária. Deus é o dono do ouro e da prata. Administre com sabedoria.</p><h1>Ω</h1><p>SOLI DEO GLORIA</p></div>", unsafe_allow_html=True)

elif menu == "🤝 Conselho de Elite":
    st.title("🤝 Conselho de Elite")
    st.checkbox("Mente em estado de governo?")
    st.checkbox("Gestão de risco calculada?")
    st.markdown("<div class='card-quantum'>Foque no High-Ticket. O lucro é feito na compra.</div>", unsafe_allow_html=True)
