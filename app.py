import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests

# =================================================================
# 1. CONFIGURAÇÃO DE ALTA PERFORMANCE E CABEÇALHO DO SISTEMA
# =================================================================
st.set_page_config(
    page_title="Quantum Nexus Elite Pro - Terminal de Estado", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# =================================================================
# 2. ESTILIZAÇÃO VISUAL CUSTOMIZADA (CSS DE ELITE APRIMORADO)
# =================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Configuração Geral da Aplicação */
    .stApp { 
        background-color: #000000; 
        color: #FFFFFF; 
        font-family: 'Inter', sans-serif; 
    }
    
    /* Sidebar com Design de Painel de Controle */
    [data-testid="stSidebar"] { 
        background-color: #050505; 
        border-right: 2px solid #d4af37; 
        box-shadow: 10px 0px 40px rgba(212, 175, 55, 0.15);
    }
    
    /* Customização de Títulos e Textos */
    h1, h2, h3 { 
        color: #d4af37; 
        font-family: 'JetBrains Mono', monospace; 
        letter-spacing: 4px; 
        text-transform: uppercase;
        font-weight: 700;
    }
    
    /* Botões Operacionais com Efeito Tesla-Gold */
    .stButton>button { 
        border-radius: 15px; 
        border: 1px solid #d4af37; 
        background: linear-gradient(135deg, #1a1a1a 0%, #000 100%); 
        color: #d4af37 !important; 
        font-weight: 800; 
        text-transform: uppercase;
        letter-spacing: 2px;
        width: 100%; 
        height: 65px; 
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.5);
    }
    .stButton>button:hover { 
        transform: translateY(-5px) scale(1.01); 
        background: linear-gradient(135deg, #d4af37 0%, #f9e295 100%); 
        color: #000 !important;
        box-shadow: 0px 15px 50px rgba(212, 175, 55, 0.4);
    }
    
    /* Cards de Módulos (Container de Informação) */
    .card-quantum { 
        border-radius: 30px; 
        background: linear-gradient(145deg, #0f0f0f, #050505); 
        padding: 40px; 
        border: 1px solid #222; 
        margin-bottom: 30px;
        box-shadow: 20px 20px 60px #000, -5px -5px 20px #111;
    }
    
    /* Estilização de Métricas de Mercado */
    [data-testid="stMetricValue"] { 
        color: #d4af37 !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 2.8rem !important; 
        font-weight: 700 !important;
    }

    /* Mensagens de Estado */
    .state-message { 
        border-left: 10px solid #d4af37; 
        padding: 40px; 
        background: rgba(10, 10, 10, 0.8); 
        line-height: 2.4; 
        font-size: 1.25rem;
        border-radius: 0 40px 40px 0;
        margin: 20px 0;
    }
    
    .trend-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
        border: 1px solid #d4af37;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
    }
    
    .sentiment-positive { color: #00ff88; font-weight: bold; }
    .sentiment-neutral { color: #ffd700; font-weight: bold; }
    .sentiment-negative { color: #ff4444; font-weight: bold; }

    #MainMenu, footer, header {visibility: hidden;}
    
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #d4af37; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 3. FUNÇÕES ANALÍTICAS AVANÇADAS (NÚCLEO DE INTELIGÊNCIA)
# =================================================================

def calcular_rsi(data, periodo=14):
    delta = data['Close'].diff()
    ganho = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    perda = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
    rs = ganho / perda
    return 100 - (100 / (1 + rs))

def calcular_macd(data):
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd, signal, macd - signal

def analisar_tendencia(data):
    rsi = calcular_rsi(data).iloc[-1]
    macd, signal, _ = calcular_macd(data)
    macd_atual = macd.iloc[-1]
    signal_atual = signal.iloc[-1]
    preco_atual = data['Close'].iloc[-1]
    sma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
    
    sinais_alta = 0
    sinais_baixa = 0
    
    if rsi < 30: sinais_alta += 1
    elif rsi > 70: sinais_baixa += 1
    
    if macd_atual > signal_atual: sinais_alta += 1
    else: sinais_baixa += 1
    
    if preco_atual > sma_20: sinais_alta += 1
    else: sinais_baixa += 1
    
    if sinais_alta > sinais_baixa: tendencia, forca = "ALTA", sinais_alta * 33.3
    elif sinais_baixa > sinais_alta: tendencia, forca = "BAIXA", sinais_baixa * 33.3
    else: tendencia, forca = "NEUTRA", 50
    
    return {'tendencia': tendencia, 'forca': forca, 'rsi': rsi, 'macd': macd_atual, 'signal': signal_atual, 'preco': preco_atual, 'sma_20': sma_20}

def render_analise_tecnica_avancada(ticker, nome):
    try:
        data = yf.download(ticker, period="180d", interval="1d", progress=False, auto_adjust=True)
        if data.empty:
            st.error(f"⚠️ FALHA NA SINCRONIZAÇÃO: {nome}")
            return
        
        # Correção para MultiIndex se necessário
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        analise = analisar_tendencia(data)
        
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.5, 0.25, 0.25])
        
        fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name="Preço"), row=1, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=calcular_rsi(data), name='RSI', line=dict(color='#d4af37')), row=2, col=1)
        
        m, s, _ = calcular_macd(data)
        fig.add_trace(go.Scatter(x=data.index, y=m, name='MACD', line=dict(color='#00ff88')), row=3, col=1)
        fig.add_trace(go.Scatter(x=data.index, y=s, name='Signal', line=dict(color='#ff4444')), row=3, col=1)

        fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=800, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("PREÇO", f"${analise['preco']:.2f}")
        c2.metric("TENDÊNCIA", analise['tendencia'], f"Força: {analise['forca']:.0f}%")
        c3.metric("RSI", f"{analise['rsi']:.1f}")
        
    except Exception as e:
        st.warning(f"🔄 Erro no motor de dados: {e}")

def logic_astrolabio_tesla(max_n, qtd, modalidade):
    def reduzir(n):
        while n > 9: n = sum(int(d) for d in str(n))
        return n
    random.seed(int(time.time() * 1000) % 10000)
    numeros_vortex = [n for n in range(1, max_n + 1) if reduzir(n) in [3, 6, 9]]
    numeros_comuns = [n for n in range(1, max_n + 1) if n not in numeros_vortex]
    
    qtd_vortex = int(qtd * 0.4)
    selecao = random.sample(numeros_vortex, min(qtd_vortex, len(numeros_vortex)))
    selecao += random.sample(numeros_comuns, qtd - len(selecao))
    
    trevos = sorted(random.sample(range(1, 7), 2)) if modalidade == "Milionária" else []
    return sorted(selecao), trevos

# =================================================================
# 4. SIDEBAR - PAINEL DE COMANDO CENTRAL
# =================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>⚡ NEXUS ELITE PRO</h1>", unsafe_allow_html=True)
    menu = st.radio("COMANDOS:", ["🎯 Dashboard", "💎 IA Tesla", "🐾 Pet Intel", "💹 Trade", "👗 Fashion", "🌍 Soberania", "🙏 Devocional", "🤝 Conselho"])

# =================================================================
# 5. MÓDULOS (ESTRUTURA COMPLETA)
# =================================================================

if menu == "🎯 Dashboard":
    st.title("🎯 Dashboard Executivo")
    st.markdown("<div class='card-quantum'>Visão Panorâmica de Ativos e KPIs de Estado.</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("OURO (GC=F)", "Ativo", "Soberania")
    col2.metric("BITCOIN", "Ativo", "Hedge Quântico")
    col3.metric("PET MARKET", "R$ 66Bi", "Expansão")

elif menu == "💎 IA Tesla":
    st.title("💎 IA Quântico Tesla")
    jogo = st.selectbox("Modalidade:", ["Mega-Sena", "Lotofácil", "Quina", "Milionária"])
    if st.button("⚡ EXECUTAR VÓRTICE 3-6-9"):
        configs = {"Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5), "Milionária": (50, 6)}
        n_max, n_qtd = configs[jogo]
        nums, trevos = logic_astrolabio_tesla(n_max, n_qtd, jogo)
        st.markdown(f"<div class='card-quantum' style='text-align: center;'><h1 style='font-size: 4rem;'>{nums}</h1></div>", unsafe_allow_html=True)
        if trevos: st.subheader(f"☘️ TREVOS: {trevos}")

elif menu == "🐾 Pet Intel":
    st.title("🐾 Pet Global Intelligence")
    st.markdown("<div class='card-quantum'>Análise de Mercado Petz e E-commerce especializado.</div>", unsafe_allow_html=True)
    render_analise_tecnica_avancada("PETZ3.SA", "Petz Brasil")

elif menu == "💹 Trade":
    st.title("💹 Terminal de Trading")
    ativo = st.selectbox("Ativo:", ["BTC-USD", "GC=F", "VALE3.SA", "PETR4.SA"])
    render_analise_tecnica_avancada(ativo, ativo)

elif menu == "👗 Fashion":
    st.title("👗 Fashion High-Ticket")
    render_analise_tecnica_avancada("MC.PA", "LVMH (Louis Vuitton)")

elif menu == "🌍 Soberania":
    st.title("🌍 Soberania & Reservas")
    st.subheader("🥇 Reserva de Ouro")
    render_analise_tecnica_avancada("GC=F", "Ouro")

elif menu == "🙏 Devocional":
    st.title("🙏 Devocional de Poder")
    st.markdown("<div class='state-message'><h3>Soli Deo Gloria</h3>Ouro e Prata pertencem ao Criador. Nós somos gestores da abundância.</div>", unsafe_allow_html=True)

elif menu == "🤝 Conselho":
    st.title("🤝 Conselho de Elite")
    st.markdown("<div class='trend-card'>1. Preservação do Capital<br>2. Visão High-Ticket<br>3. Governança Divina</div>", unsafe_allow_html=True)
