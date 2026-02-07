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
            increasing_fillcolor='#d4af37', decreasing_fillcolor='#ff4b4b', name="Preço de Mercado"
        )])
        fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=580, xaxis_rangeslider_visible=False, title=dict(text=f"TERMINAL ANALÍTICO: {nome.upper()}", font=dict(color='#d4af37', size=22)))
        st.plotly_chart(fig, use_container_width=True)
        
        atual = data['Close'].iloc[-1]
        anterior = data['Close'].iloc[-2]
        delta_perc = ((atual - anterior) / anterior) * 100
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("PREÇO ATUAL", f"{atual:.2f}")
        m2.metric("VARIAÇÃO DIA", f"{delta_perc:.2f}%", delta=f"{(atual-anterior):.2f}")
        m3.metric("MÁXIMA 90D", f"{data['High'].max():.2f}")
        m4.metric("MÍNIMA 90D", f"{data['Low'].min():.2f}")
    except Exception as e:
        st.warning("🔄 Conexão instável com o servidor de dados.")

def logic_astrolabio_tesla(max_n, qtd, modalidade):
    with st.status("🌀 SINCRO-VÓRTICE ATIVO: ANALISANDO FREQUÊNCIAS...", expanded=True) as status:
        time.sleep(1.5)
        random.seed(int(time.time() * 1000))
        populacao_total = list(range(1, max_n + 1))
        vortex_base = [n for n in populacao_total if (n % 3 == 0 or n % 6 == 0 or n % 9 == 0)]
        
        # Correção do erro de amostragem
        if qtd > len(vortex_base):
            restante = list(set(populacao_total) - set(vortex_base))
            full_pool = vortex_base + random.sample(restante, qtd - len(vortex_base))
        else:
            full_pool = vortex_base
        
        selecionados = sorted(random.sample(full_pool, qtd))
        trevos = sorted(random.sample(range(1, 7), 2)) if modalidade == "Milionária" else None
        status.update(label="CONFLUÊNCIA ESTABELECIDA!", state="complete")
        return selecionados, trevos

# =================================================================
# 4. SIDEBAR - PAINEL DE COMANDO CENTRAL
# =================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>⚡ NEXUS ELITE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d4af37;'>SISTEMA DE ESTADO v4.1</p>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("COMANDOS DISPONÍVEIS:", ["💎 IA Quântico Tesla", "🐾 Pet Global Intelligence", "💹 Trade & Commodities", "👗 Fashion High-Ticket", "🌍 Soberania & Reservas", "🙏 Devocional de Poder", "🤝 Conselho de Elite"])
    st.write("---")
    st.markdown("**Status:** Operacional")
    st.markdown("**Nível:** Administrator")
    st.caption(f"Tempo de Execução: {datetime.now().strftime('%H:%M:%S')}")

# =================================================================
# 5. EXECUÇÃO DOS MÓDULOS
# =================================================================

if menu == "💎 IA Quântico Tesla":
    st.title("💎 IA Quântico Tesla & Astrolábio")
    st.markdown("<div class='card-quantum'>Este módulo utiliza a Matemática de Vórtice para identificar padrões de confluência em jogos de alta volatilidade.</div>", unsafe_allow_html=True)
    col_j1, col_j2 = st.columns([2, 1])
    with col_j1:
        jogo = st.selectbox("Modalidade Operacional:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    with col_j2:
        esfera = st.select_slider("Frequência (Hz):", options=[369, 432, 528, 963])

    if st.button("EXECUTAR CONFLUÊNCIA DE VÓRTICE"):
        configs = {"Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5), "Lotomania": (100, 50), "Milionária": (50, 6)}
        n_max, n_qtd = configs[jogo]
        nums, trevos = logic_astrolabio_tesla(n_max, n_qtd, jogo)
        st.markdown(f"<div class='card-quantum' style='text-align: center; border: 2px solid #d4af37;'><h1 style='font-size: 3.8rem;'>{', '.join(map(str, nums))}</h1></div>", unsafe_allow_html=True)
        if jogo == "Milionária" and trevos:
            st.markdown(f"<h2 style='text-align: center; color: #d4af37;'>☘️ TREVOS: {trevos[0]} e {trevos[1]}</h2>", unsafe_allow_html=True)

elif menu == "🐾 Pet Global Intelligence":
    st.title("🐾 Pet Global Intelligence")
    st.markdown("<div class='card-quantum'>Análise de mercado especializado em Pet Shops e E-commerce de nicho.</div>", unsafe_allow_html=True)
    pet_ativo = st.selectbox("Selecione Ativo Pet:", ["PETZ3.SA (Petz Brasil)", "CHWY (Chewy Inc USA)", "PAWZ (ETF Pet Care)"])
    render_corretora_chart(pet_ativo.split(" (")[1].replace(")", ""), pet_ativo)

elif menu == "💹 Trade & Commodities":
    st.title("💹 Terminal de Trading Profissional")
    t_ativo = st.selectbox("Selecione o Ativo:", ["BTC-USD (Bitcoin)", "ETH-USD (Ethereum)", "USDBRL=X (Dólar)", "GC=F (Ouro Futuros)"])
    render_corretora_chart(t_ativo.split(" (")[1].replace(")", ""), t_ativo)
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("<div style='background: #0a0a0a; padding: 25px; border-radius: 20px; border: 1px solid #d4af37;'><h4>🧠 INSIGHT IA</h4><p>Forte acumulação em zonas de suporte institucional.</p></div>", unsafe_allow_html=True)
    with col_t2:
        fig_vol = go.Figure(data=[go.Bar(x=['Bitcoin', 'Ethereum', 'Dólar', 'Ouro'], y=[65, 78, 12, 8], marker_color='#d4af37')])
        fig_vol.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', height=250)
        st.plotly_chart(fig_vol, use_container_width=True)

elif menu == "👗 Fashion High-Ticket":
    st.title("👗 Radar Fashion Luxo & Market Share")
    f_marca = st.selectbox("Ativo Luxo:", ["MC.PA (LVMH)", "RMS.PA (Hermès)", "KER.PA (Kering)", "ARZZ3.SA (Arezzo)", "SOMA3.SA (Soma)"])
    render_corretora_chart(f_marca.split(" (")[1].replace(")", ""), f_marca)
    st.subheader("🏛️ TOP 10 CONGLOMERADOS DE LUXO MUNDIAIS")
    col_fi1, col_fi2 = st.columns([3, 2])
    marcas_int = ['LVMH', 'Hermès', 'Dior', 'Chanel', 'Richemont', 'Kering', 'Estée Lauder', 'Rolex', 'Prada', 'Burberry']
    val_int = [420, 210, 150, 110, 85, 70, 65, 50, 45, 30]
    with col_fi1:
        fig_bar_fi = go.Figure(data=[go.Bar(x=marcas_int, y=val_int, marker_color='#d4af37')])
        fig_bar_fi.update_layout(title="Valuation (Bilhões USD)", template='plotly_dark')
        st.plotly_chart(fig_bar_fi, use_container_width=True)
    with col_fi2:
        fig_pie_fi = go.Figure(data=[go.Pie(labels=marcas_int, values=val_int, hole=.4)])
        fig_pie_fi.update_layout(title="% Mercado Global", template='plotly_dark')
        st.plotly_chart(fig_pie_fi, use_container_width=True)

elif menu == "🌍 Soberania & Reservas":
    st.title("🌍 Soberania Nacional e Reservas Mundiais")
    reserva_sel = st.selectbox("Ativo Estratégico:", ["GC=F (Ouro)", "SI=F (Prata)", "BZ=F (Brent)", "VALE3.SA (Vale)"])
    render_corretora_chart(reserva_sel.split(" (")[1].replace(")", ""), reserva_sel)
    st.subheader("🏛️ RESERVAS DE OURO MUNDIAIS")
    col_int1, col_int2 = st.columns([3, 2])
    with col_int1:
        fig_bar_int = go.Figure(data=[go.Bar(x=['EUA', 'Alemanha', 'FMI', 'Itália', 'França', 'Rússia', 'China'], y=[8133, 3355, 2814, 2451, 2436, 2332, 2191], marker_color='#d4af37')])
        fig_bar_int.update_layout(title="Toneladas Físicas", template='plotly_dark')
        st.plotly_chart(fig_bar_int, use_container_width=True)
    with col_int2:
        fig_pie_int = go.Figure(data=[go.Pie(labels=['EUA', 'Alemanha', 'FMI', 'Outros'], values=[8133, 3355, 2814, 15000], hole=.4)])
        st.plotly_chart(fig_pie_int, use_container_width=True)

elif menu == "🙏 Devocional de Poder":
    st.title("🙏 Sabedoria, Propósito e Legado")
    st.markdown("""
        <div class='state-message'>
            <h2 style='text-align: center; color: #d4af37;'>O FUNDAMENTO DA SOBERANIA REAL</h2>
            <p align='center' style='font-style: italic;'> "Minha é a prata, e meu é o ouro, diz o Senhor dos Exércitos."</p>
        </div>
    """, unsafe_allow_html=True)
    col_d1, col_d2 = st.columns([1, 2])
    with col_d1:
        st.markdown("<div style='text-align: center; padding: 20px; border: 2px solid #d4af37; border-radius: 100%;'><h1 style='font-size: 5rem;'>Ω</h1></div>", unsafe_allow_html=True)
    with col_d2:
        st.markdown("<h3>O PRINCÍPIO DA DEPENDÊNCIA SOBERANA</h3><p>Toda riqueza é um empréstimo divino para gestão do Reino.</p>", unsafe_allow_html=True)

elif menu == "🤝 Conselho de Elite":
    st.title("🤝 Conselho de Elite & Diretrizes")
    st.markdown("<div class='card-quantum'>Protocolo final de execução e gestão de risco.</div>", unsafe_allow_html=True)
    st.checkbox("Devocional realizado?")
    st.checkbox("Gestão de risco calculada?")
    st.metric("META E-COMMERCE PET", "R$ 50k", "+12%")
