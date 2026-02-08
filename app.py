import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go
import time
import pandas as pd
from datetime import datetime

# =================================================================
# 1. CONFIGURAÇÃO DE ALTA PERFORMANCE (NEXUS ELITE)
# =================================================================
st.set_page_config(
    page_title="Quantum Nexus Elite - Terminal de Estado", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# =================================================================
# 2. ESTILIZAÇÃO VISUAL (CSS INTEGRAL - DESIGN DE LUXO)
# =================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    .stApp { background-color: #000000; color: #FFFFFF; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { 
        background-color: #050505; 
        border-right: 2px solid #d4af37; 
        box-shadow: 10px 0px 40px rgba(212, 175, 55, 0.15); 
    }
    
    h1, h2, h3 { 
        color: #d4af37; 
        font-family: 'JetBrains Mono', monospace; 
        letter-spacing: 4px; 
        text-transform: uppercase; 
        font-weight: 700; 
    }
    
    .stButton>button { 
        border-radius: 15px; border: 1px solid #d4af37; background: linear-gradient(135deg, #1a1a1a 0%, #000 100%); 
        color: #d4af37 !important; font-weight: 800; text-transform: uppercase; letter-spacing: 2px;
        width: 100%; height: 65px; transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover { 
        transform: translateY(-5px); background: linear-gradient(135deg, #d4af37 0%, #f9e295 100%); color: #000 !important;
        box-shadow: 0px 15px 50px rgba(212, 175, 55, 0.4);
    }
    
    .card-quantum { 
        border-radius: 30px; background: linear-gradient(145deg, #0f0f0f, #050505); 
        padding: 40px; border: 1px solid #222; margin-bottom: 30px; 
        box-shadow: 20px 20px 60px #000;
    }
    
    [data-testid="stMetricValue"] { color: #d4af37 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 2.8rem !important; }
    .state-message { border-left: 10px solid #d4af37; padding: 40px; background: rgba(10, 10, 10, 0.8); line-height: 2.4; font-size: 1.25rem; border-radius: 0 40px 40px 0; margin: 20px 0; }
    
    #MainMenu, footer, header {visibility: hidden;}
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #d4af37; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 3. MOTORES ANALÍTICOS (CORREÇÃO DE GRÁFICOS E LÓGICA)
# =================================================================

def render_corretora_chart(ticker, nome):
    try:
        data = yf.download(ticker, period="1y", interval="1d", progress=False, auto_adjust=True)
        
        # ESSENCIAL: Resolve o erro do gráfico vazio limpando os cabeçalhos do Yahoo
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        if data.empty:
            st.error(f"⚠️ FALHA NA SINCRONIZAÇÃO: {nome} indisponível.")
            return

        fig = go.Figure(data=[go.Candlestick(
            x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
            increasing_line_color='#d4af37', decreasing_line_color='#ff4b4b',
            increasing_fillcolor='#d4af37', decreasing_fillcolor='#ff4b4b'
        )])
        fig.update_layout(
            template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
            height=550, xaxis_rangeslider_visible=False,
            title=dict(text=f"TERMINAL ANALÍTICO: {nome.upper()}", font=dict(color='#d4af37', size=22))
        )
        st.plotly_chart(fig, use_container_width=True)
        
        m1, m2, m3, m4 = st.columns(4)
        atual = data['Close'].iloc[-1]
        anterior = data['Close'].iloc[-2]
        m1.metric("PREÇO ATUAL", f"{atual:.2f}")
        m2.metric("VARIAÇÃO DIA", f"{((atual-anterior)/anterior*100):.2f}%", delta=f"{(atual-anterior):.2f}")
        m3.metric("MÁXIMA 52W", f"{data['High'].max():.2f}")
        m4.metric("MÍNIMA 52W", f"{data['Low'].min():.2f}")
    except Exception as e:
        st.warning(f"🔄 Terminal em reconexão... Erro: {e}")

def logic_astrolabio_tesla(max_n, qtd, modalidade):
    random.seed(int(time.time() * 1000))
    populacao_total = list(range(1, max_n + 1))
    vortex_base = [n for n in populacao_total if (n % 3 == 0 or n % 6 == 0 or n % 9 == 0)]
    
    # PROTEÇÃO: Se o vortex for menor que a quantidade, usa a população total (Resolve o ValueError do print)
    pool_final = vortex_base if len(vortex_base) >= qtd else populacao_total
        
    selecionados = sorted(random.sample(pool_final, qtd))
    trevos = sorted(random.sample(range(1, 7), 2)) if modalidade == "Milionária" else None
    return selecionados, trevos

# =================================================================
# 4. SIDEBAR - COMANDO CENTRAL
# =================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>⚡ NEXUS ELITE</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("COMANDOS DISPONÍVEIS:", [
        "💎 IA Quântico Tesla", 
        "🐾 Pet Global Intelligence", 
        "💹 Trade & Commodities", 
        "👗 Fashion High-Ticket", 
        "🌍 Soberania & Reservas", 
        "🙏 Devocional de Poder", 
        "🤝 Conselho de Elite"
    ])
    st.write("---")
    st.markdown("**Status:** Operacional")
    st.markdown("**Nível:** Administrator")
    st.caption(f"Sync: {datetime.now().strftime('%H:%M:%S')}")

# =================================================================
# 5. EXECUÇÃO INTEGRAL DOS MÓDULOS (O QUE ESTAVA FALTANDO)
# =================================================================

if menu == "💎 IA Quântico Tesla":
    st.title("💎 IA Quântico Tesla & Astrolábio")
    st.markdown("<div class='card-quantum'>Algoritmo de confluência baseado na Matemática de Vórtice 3-6-9.</div>", unsafe_allow_html=True)
    col_j1, col_j2 = st.columns([2, 1])
    with col_j1:
        jogo = st.selectbox("Modalidade:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    with col_j2:
        esfera = st.select_slider("Frequência (Hz):", options=[369, 432, 528, 963])

    if st.button("EXECUTAR CONFLUÊNCIA DE VÓRTICE"):
        configs = {"Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5), "Lotomania": (100, 50), "Milionária": (50, 6)}
        n_max, n_qtd = configs[jogo]
        nums, trevos = logic_astrolabio_tesla(n_max, n_qtd, jogo)
        st.markdown(f"<div class='card-quantum' style='text-align: center;'><h1 style='font-size: 3rem;'>{nums}</h1></div>", unsafe_allow_html=True)
        if trevos: st.markdown(f"<h2 style='text-align: center; color: #d4af37;'>☘️ TREVOS: {trevos}</h2>", unsafe_allow_html=True)

elif menu == "🐾 Pet Global Intelligence":
    st.title("🐾 Pet Global Intelligence")
    render_corretora_chart("PETZ3.SA", "PETZ BRASIL")
    st.subheader("📊 Estrutura de Mercado Pet")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.plotly_chart(go.Figure(data=[go.Bar(x=['Petz', 'Cobasi', 'Petlove', 'Amazon'], y=[28, 24, 22, 12], marker_color='#d4af37')], layout=dict(template='plotly_dark', title="Market Share (%)")), use_container_width=True)
    with col_p2:
        st.plotly_chart(go.Figure(data=[go.Pie(labels=['Alimentos', 'Higiene', 'Luxo', 'Serviços'], values=[40, 25, 20, 15], hole=.4)], layout=dict(template='plotly_dark', title="Distribuição de Receita")), use_container_width=True)

elif menu == "💹 Trade & Commodities":
    st.title("💹 Terminal de Trading")
    render_corretora_chart("BTC-USD", "BITCOIN")
    render_corretora_chart("GC=F", "OURO FUTUROS")

elif menu == "👗 Fashion High-Ticket":
    st.title("👗 Radar Fashion Luxo")
    render_corretora_chart("MC.PA", "LVMH (LOUIS VUITTON)")
    st.subheader("🏛️ Valuation Global de Luxo (Billion USD)")
    marcas = ['LVMH', 'Hermès', 'Dior', 'Chanel', 'Richemont', 'Kering']
    valores = [420, 210, 150, 110, 85, 70]
    st.plotly_chart(go.Figure(data=[go.Bar(x=marcas, y=valores, marker_color='#d4af37')], layout=dict(template='plotly_dark')), use_container_width=True)

elif menu == "🌍 Soberania & Reservas":
    st.title("🌍 Soberania & Reservas")
    st.subheader("🏛️ Reservas de Ouro (Toneladas Médricas)")
    paises = ['EUA', 'Alemanha', 'FMI', 'Itália', 'França', 'Rússia', 'China']
    ton = [8133, 3355, 2814, 2451, 2436, 2332, 2191]
    st.plotly_chart(go.Figure(data=[go.Pie(labels=paises, values=ton, hole=.4)], layout=dict(template='plotly_dark')), use_container_width=True)
    st.markdown("> **Dossiê:** Brasil detém 98% do Nióbio mundial. Soberania absoluta em minerais críticos.")

elif menu == "🙏 Devocional de Poder":
    st.markdown("<div class='state-message'><h2>O FUNDAMENTO DA SOBERANIA</h2><p>A riqueza serve ao propósito, o propósito serve ao Reino. Soli Deo Gloria.</p></div>", unsafe_allow_html=True)

elif menu == "🤝 Conselho de Elite":
    st.title("🤝 Conselho de Elite")
    st.metric("META E-COMMERCE PET", "R$ 50.000,00", "+15%")
    st.checkbox("Checklist Devocional Realizado")
    st.checkbox("Análise de Risco Tesla Concluída")
