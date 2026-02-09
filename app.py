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
    initial_sidebar_state="collapsed"
)

# =================================================================
# 2. ESTILIZAÇÃO VISUAL CUSTOMIZADA (CSS ESTILO APP BANCÁRIO)
# =================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Configuração Geral da Aplicação */
    .stApp { 
        background: linear-gradient(180deg, #0a0a0a 0%, #000000 100%);
        color: #FFFFFF; 
        font-family: 'Inter', sans-serif; 
    }
    
    /* Header Fixo Estilo App Bancário */
    .app-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 15px 20px;
        border-radius: 0 0 25px 25px;
        margin: -80px -80px 20px -80px;
        box-shadow: 0 10px 40px rgba(212, 175, 55, 0.2);
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    /* Botão de Voltar Estilo App */
    .back-button {
        background: linear-gradient(135deg, #d4af37 0%, #b8922a 100%);
        color: #000 !important;
        border: none;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }
    
    .back-button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.6);
    }
    
    /* Cards de Menu Estilo App Bancário */
    .menu-card {
        background: linear-gradient(145deg, #1a1a2e 0%, #0f0f1a 100%);
        border-radius: 20px;
        padding: 25px 20px;
        border: 1px solid rgba(212, 175, 55, 0.3);
        margin-bottom: 15px;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .menu-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .menu-card:hover::before {
        left: 100%;
    }
    
    .menu-card:hover {
        transform: translateY(-8px) scale(1.02);
        border-color: #d4af37;
        box-shadow: 0 20px 50px rgba(212, 175, 55, 0.25);
    }
    
    .menu-card:active {
        transform: scale(0.98);
    }
    
    .menu-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        display: block;
    }
    
    .menu-title {
        color: #d4af37;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    
    .menu-desc {
        color: #888;
        font-size: 0.75rem;
        line-height: 1.4;
    }
    
    /* Cards de Módulos (Container de Informação) */
    .card-quantum { 
        border-radius: 25px; 
        background: linear-gradient(145deg, #0f0f1a, #1a1a2e); 
        padding: 30px; 
        border: 1px solid rgba(212, 175, 55, 0.2); 
        margin-bottom: 25px;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
    }
    
    /* Estilização de Métricas de Mercado */
    [data-testid="stMetricValue"] { 
        color: #d4af37 !important; 
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 2.5rem !important; 
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricDelta"] { 
        font-size: 1.1rem !important; 
        background: rgba(0,0,0,0.3);
        padding: 5px 12px;
        border-radius: 12px;
    }
    
    /* Botões Operacionais */
    .stButton>button { 
        border-radius: 18px; 
        border: 2px solid #d4af37; 
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1a 100%); 
        color: #d4af37 !important; 
        font-weight: 700; 
        text-transform: uppercase;
        letter-spacing: 2px;
        width: 100%; 
        height: 55px; 
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
    }
    
    .stButton>button:hover { 
        transform: translateY(-3px) scale(1.02); 
        background: linear-gradient(135deg, #d4af37 0%, #f9e295 100%); 
        color: #000 !important;
        box-shadow: 0 12px 40px rgba(212, 175, 55, 0.4);
    }
    
    /* Card de Análise de Tendência */
    .trend-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1a 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* Indicador de Sentimento */
    .sentiment-positive { color: #00ff88; font-weight: bold; }
    .sentiment-neutral { color: #ffd700; font-weight: bold; }
    .sentiment-negative { color: #ff4444; font-weight: bold; }
    
    /* Mensagens de Estado */
    .state-message { 
        border-left: 5px solid #d4af37; 
        padding: 30px; 
        background: linear-gradient(145deg, #0f0f1a, #1a1a2e); 
        line-height: 2; 
        font-size: 1.1rem;
        border-radius: 0 20px 20px 0;
        box-shadow: 10px 10px 30px rgba(0,0,0,0.4);
        margin: 20px 0;
    }
    
    /* Bottom Navigation Bar */
    .bottom-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%);
        padding: 15px 20px;
        border-top: 1px solid rgba(212, 175, 55, 0.3);
        display: flex;
        justify-content: space-around;
        align-items: center;
        z-index: 1000;
        box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.5);
    }
    
    .nav-item {
        color: #666;
        text-align: center;
        font-size: 0.7rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-item:hover {
        color: #d4af37;
    }
    
    .nav-item.active {
        color: #d4af37;
    }
    
    .nav-icon {
        font-size: 1.5rem;
        display: block;
        margin-bottom: 3px;
    }
    
    /* Escondendo Elementos Desnecessários do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar de Luxo */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: #d4af37; border-radius: 10px; }
    
    /* Tabelas Profissionais */
    .dataframe { 
        background-color: #0f0f1a !important;
        color: #fff !important;
        border-radius: 15px;
        overflow: hidden;
    }
    .dataframe th {
        background-color: #1a1a2e !important;
        color: #d4af37 !important;
        font-weight: bold !important;
        padding: 15px !important;
    }
    .dataframe td {
        padding: 12px 15px !important;
    }
    
    /* Selectbox Estilo App */
    .stSelectbox > div > div {
        background: linear-gradient(145deg, #1a1a2e, #0f0f1a) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 15px !important;
        color: #fff !important;
    }
    
    /* Input Estilo App */
    .stNumberInput > div > div > input {
        background: linear-gradient(145deg, #1a1a2e, #0f0f1a) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 15px !important;
        color: #fff !important;
    }
    
    /* Slider Estilo App */
    .stSlider > div > div {
        background: #1a1a2e !important;
    }
    
    /* Checkbox Estilo App */
    .stCheckbox > label {
        color: #fff !important;
    }
    
    /* Radio Estilo App */
    .stRadio > div {
        background: linear-gradient(145deg, #1a1a2e, #0f0f1a);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    /* Título da Página */
    .page-title {
        font-family: 'JetBrains Mono', monospace;
        color: #d4af37;
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    /* Header com Botão Voltar */
    .page-header {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 25px;
        padding: 15px 0;
        border-bottom: 1px solid rgba(212, 175, 55, 0.2);
    }
    
    .back-btn-container {
        background: linear-gradient(135deg, #d4af37 0%, #b8922a 100%);
        border-radius: 50%;
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }
    
    .back-btn-container:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.6);
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(145deg, #1a1a2e, #0f0f1a);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(212, 175, 55, 0.2);
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .kpi-card:hover {
        border-color: #d4af37;
        transform: translateY(-5px);
    }
    
    .kpi-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2rem;
        color: #d4af37;
        font-weight: 700;
    }
    
    .kpi-label {
        color: #888;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 5px;
    }
    
    .kpi-delta {
        font-size: 0.9rem;
        margin-top: 8px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 3. FUNÇÕES ANALÍTICAS AVANÇADAS (NÚCLEO DE INTELIGÊNCIA)
# =================================================================

def calcular_rsi(data, periodo=14):
    """Calcula o RSI (Relative Strength Index)"""
    delta = data['Close'].diff()
    ganho = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    perda = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
    rs = ganho / perda
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calcular_macd(data):
    """Calcula MACD (Moving Average Convergence Divergence)"""
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def calcular_bollinger_bands(data, periodo=20):
    """Calcula Bandas de Bollinger"""
    sma = data['Close'].rolling(window=periodo).mean()
    std = data['Close'].rolling(window=periodo).std()
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    return sma, upper_band, lower_band

def analisar_tendencia(data):
    """Análise de tendência usando múltiplos indicadores"""
    rsi = calcular_rsi(data).iloc[-1]
    macd, signal, _ = calcular_macd(data)
    macd_atual = macd.iloc[-1]
    signal_atual = signal.iloc[-1]
    
    preco_atual = data['Close'].iloc[-1]
    sma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
    sma_50 = data['Close'].rolling(window=50).mean().iloc[-1]
    
    # Contagem de sinais
    sinais_alta = 0
    sinais_baixa = 0
    
    if rsi < 30:
        sinais_alta += 1
    elif rsi > 70:
        sinais_baixa += 1
    
    if macd_atual > signal_atual:
        sinais_alta += 1
    else:
        sinais_baixa += 1
    
    if preco_atual > sma_20 > sma_50:
        sinais_alta += 1
    elif preco_atual < sma_20 < sma_50:
        sinais_baixa += 1
    
    if sinais_alta > sinais_baixa:
        tendencia = "ALTA"
        forca = sinais_alta * 33.3
    elif sinais_baixa > sinais_alta:
        tendencia = "BAIXA"
        forca = sinais_baixa * 33.3
    else:
        tendencia = "NEUTRA"
        forca = 50
    
    return {
        'tendencia': tendencia,
        'forca': forca,
        'rsi': rsi,
        'macd': macd_atual,
        'signal': signal_atual,
        'preco': preco_atual,
        'sma_20': sma_20,
        'sma_50': sma_50
    }

def render_analise_tecnica_avancada(ticker, nome):
    """
    Motor de Análise Técnica Profissional com múltiplos indicadores
    """
    try:
        # Busca dados de 180 dias para análises mais robustas
        data = yf.download(ticker, period="180d", interval="1d", progress=False, auto_adjust=True)
        
        if data.empty:
            st.error(f"⚠️ FALHA NA SINCRONIZAÇÃO: O ativo {nome} está fora de alcance no momento.")
            return
        
        # Calcular indicadores
        data['RSI'] = calcular_rsi(data)
        macd, signal, histogram = calcular_macd(data)
        data['MACD'] = macd
        data['Signal'] = signal
        sma, upper_bb, lower_bb = calcular_bollinger_bands(data)
        data['SMA_20'] = sma
        data['BB_Upper'] = upper_bb
        data['BB_Lower'] = lower_bb
        
        # Análise de tendência
        analise = analisar_tendencia(data)
        
        # Criar subplots (3 gráficos verticais)
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.5, 0.25, 0.25],
            subplot_titles=('Preço & Bollinger Bands', 'RSI', 'MACD')
        )
        
        # Gráfico 1: Candlestick + Bollinger Bands
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            increasing_line_color='#d4af37',
            decreasing_line_color='#ff4b4b',
            name="Preço"
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['SMA_20'],
            line=dict(color='#00ff88', width=1.5),
            name='SMA 20'
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['BB_Upper'],
            line=dict(color='rgba(255,255,255,0.3)', width=1, dash='dash'),
            name='BB Superior',
            showlegend=False
        ), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['BB_Lower'],
            line=dict(color='rgba(255,255,255,0.3)', width=1, dash='dash'),
            fill='tonexty',
            fillcolor='rgba(255,255,255,0.05)',
            name='BB Inferior',
            showlegend=False
        ), row=1, col=1)
        
        # Gráfico 2: RSI
        fig.add_trace(go.Scatter(
            x=data.index, y=data['RSI'],
            line=dict(color='#d4af37', width=2),
            name='RSI'
        ), row=2, col=1)
        
        # Linhas de referência RSI
        fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)
        
        # Gráfico 3: MACD
        fig.add_trace(go.Scatter(
            x=data.index, y=data['MACD'],
            line=dict(color='#00ff88', width=2),
            name='MACD'
        ), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['Signal'],
            line=dict(color='#ff4444', width=2),
            name='Signal'
        ), row=3, col=1)
        
        # Layout geral
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=900,
            showlegend=True,
            xaxis_rangeslider_visible=False,
            margin=dict(l=0, r=0, t=60, b=0),
            title=dict(
                text=f"🔬 ANÁLISE TÉCNICA COMPLETA: {nome.upper()}",
                font=dict(color='#d4af37', size=24, family='JetBrains Mono')
            )
        )
        
        # Atualizar eixos
        fig.update_xaxes(showgrid=False, color='#444')
        fig.update_yaxes(showgrid=True, gridcolor='#222', color='#444')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Grid de Métricas Avançadas
        col1, col2, col3, col4, col5 = st.columns(5)
        
        atual = data['Close'].iloc[-1]
        anterior = data['Close'].iloc[-2]
        delta_abs = atual - anterior
        delta_perc = (delta_abs / anterior) * 100
        
        # Determinar cor da tendência
        if analise['tendencia'] == "ALTA":
            cor_tendencia = "🟢"
        elif analise['tendencia'] == "BAIXA":
            cor_tendencia = "🔴"
        else:
            cor_tendencia = "🟡"
        
        col1.metric("PREÇO ATUAL", f"${atual:.2f}", delta=f"{delta_perc:.2f}%")
        col2.metric("RSI (14)", f"{analise['rsi']:.1f}", 
                   "Sobrecompra" if analise['rsi'] > 70 else "Sobrevenda" if analise['rsi'] < 30 else "Neutro")
        col3.metric("TENDÊNCIA", f"{cor_tendencia} {analise['tendencia']}", 
                   f"Força: {analise['forca']:.0f}%")
        col4.metric("VOLUME 24H", f"{data['Volume'].iloc[-1]/1e6:.1f}M")
        col5.metric("VOLATILIDADE", f"{data['Close'].pct_change().std()*100:.2f}%")
        
        # Análise textual inteligente
        st.markdown(f"""
        <div class='trend-card'>
            <h3 style='color: #d4af37; margin-top: 0;'>📊 RELATÓRIO DE INTELIGÊNCIA</h3>
            <p style='line-height: 1.8; color: #ccc;'>
                <b>Status Técnico:</b> O ativo {nome} apresenta tendência de <b>{analise['tendencia']}</b> 
                com força de <b>{analise['forca']:.0f}%</b>.<br><br>
                
                <b>Indicadores-Chave:</b><br>
                • RSI em <b>{analise['rsi']:.1f}</b> - 
                {'<span class="sentiment-negative">Zona de sobrecompra, possível correção</span>' if analise['rsi'] > 70 
                 else '<span class="sentiment-positive">Zona de sobrevenda, possível recuperação</span>' if analise['rsi'] < 30
                 else '<span class="sentiment-neutral">Neutro, sem sinais extremos</span>'}<br>
                
                • MACD {'<span class="sentiment-positive">acima</span>' if analise['macd'] > analise['signal'] else '<span class="sentiment-negative">abaixo</span>'} 
                da linha de sinal - Momentum {'positivo' if analise['macd'] > analise['signal'] else 'negativo'}<br>
                
                • Preço {'<span class="sentiment-positive">acima</span>' if analise['preco'] > analise['sma_20'] else '<span class="sentiment-negative">abaixo</span>'} 
                da SMA 20 - Tendência de {'curto prazo positiva' if analise['preco'] > analise['sma_20'] else 'curto prazo negativa'}<br><br>
                
                <b>Recomendação:</b> 
                {f'Monitorar oportunidade de entrada com stop loss em ${analise["sma_20"]:.2f}' if analise['tendencia'] == 'ALTA'
                 else f'Aguardar confirmação de reversão ou considerar proteção de posições' if analise['tendencia'] == 'BAIXA'
                 else 'Manter posição neutra até confirmação de tendência'}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.warning(f"🔄 Conexão instável com o servidor de dados para {nome}. {str(e)}")

def logic_astrolabio_tesla(max_n, qtd, modalidade):
    """
    Algoritmo baseado na Matemática de Vórtice de Nikola Tesla.
    Utiliza redução numérica (3, 6, 9) e equilíbrio de paridade.
    """
    def reduzir_para_unico(numero):
        while numero > 9:
            numero = sum(int(d) for d in str(numero))
        return numero
    
    # Gerar números base usando seed temporal
    seed = int(time.time() * 1000) % 10000
    random.seed(seed)
    
    numeros_candidatos = list(range(1, max_n + 1))
    
    # Aplicar filtro de vórtice (preferência para números com redução 3, 6, 9)
    numeros_vortex = [n for n in numeros_candidatos if reduzir_para_unico(n) in [3, 6, 9]]
    numeros_comuns = [n for n in numeros_candidatos if n not in numeros_vortex]
    
    # Proporcionar equilíbrio: 40% Vórtice + 60% Comuns
    qtd_vortex = int(qtd * 0.4)
    qtd_comuns = qtd - qtd_vortex
    
    selecao = []
    if len(numeros_vortex) >= qtd_vortex:
        selecao += random.sample(numeros_vortex, qtd_vortex)
    else:
        selecao += numeros_vortex
        qtd_comuns += qtd_vortex - len(numeros_vortex)
    
    selecao += random.sample(numeros_comuns, min(qtd_comuns, len(numeros_comuns)))
    
    # Garantir quantidade exata
    while len(selecao) < qtd:
        novo = random.choice(numeros_candidatos)
        if novo not in selecao:
            selecao.append(novo)
    
    selecao = sorted(selecao[:qtd])
    
    # Trevos especiais para Milionária
    trevos = []
    if modalidade == "Milionária":
        trevos = sorted(random.sample(range(1, 7), 2))
    
    return selecao, trevos

# =================================================================
# 4. NAVEGAÇÃO DO APP BANCÁRIO
# =================================================================

# Inicializar estado da sessão
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 'menu'
if 'menu_selecionado' not in st.session_state:
    st.session_state.menu_selecionado = None

def voltar_menu():
    st.session_state.pagina_atual = 'menu'
    st.session_state.menu_selecionado = None

def abrir_modulo(modulo):
    st.session_state.pagina_atual = 'modulo'
    st.session_state.menu_selecionado = modulo

# Definição dos módulos
modulos = {
    "dashboard": {
        "titulo": "Dashboard Executivo",
        "icone": "🎯",
        "descricao": "Visão panorâmica de ativos estratégicos e KPIs",
        "cor": "linear-gradient(145deg, #1a1a2e, #0f0f1a)"
    },
    "tesla": {
        "titulo": "IA Quântico Tesla",
        "icone": "💎",
        "descricao": "Matemática de Vórtice para análise de padrões",
        "cor": "linear-gradient(145deg, #2d1a3d, #1a0f2e)"
    },
    "pet": {
        "titulo": "Pet Global Intelligence",
        "icone": "🐾",
        "descricao": "Análise do mercado Pet global e oportunidades",
        "cor": "linear-gradient(145deg, #1a3d2d, #0f2e1a)"
    },
    "trade": {
        "titulo": "Trade & Commodities",
        "icone": "💹",
        "descricao": "Terminal de trading profissional avançado",
        "cor": "linear-gradient(145deg, #3d2d1a, #2e1a0f)"
    },
    "fashion": {
        "titulo": "Fashion High-Ticket",
        "icone": "👗",
        "descricao": "Radar de marcas de luxo e market share",
        "cor": "linear-gradient(145deg, #3d1a2d, #2e0f1a)"
    },
    "soberania": {
        "titulo": "Soberania & Reservas",
        "icone": "🌍",
        "descricao": "Monitoramento de ativos de soberania nacional",
        "cor": "linear-gradient(145deg, #1a2d3d, #0f1a2e)"
    },
    "devocional": {
        "titulo": "Devocional de Poder",
        "icone": "🙏",
        "descricao": "Alinhamento espiritual e mental para operadores",
        "cor": "linear-gradient(145deg, #2d2d1a, #1e1e0f)"
    },
    "conselho": {
        "titulo": "Conselho de Elite",
        "icone": "🤝",
        "descricao": "Diretrizes e protocolos estratégicos",
        "cor": "linear-gradient(145deg, #2d1a1a, #1e0f0f)"
    }
}

# =================================================================
# 5. TELA DE MENU PRINCIPAL (CARDS CLICÁVEIS)
# =================================================================

def render_menu_principal():
    # Header do App
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 20px 0;">
        <h1 style="font-family: 'JetBrains Mono', monospace; color: #d4af37; 
                   font-size: 2rem; margin-bottom: 5px; letter-spacing: 3px;">
            ⚡ NEXUS ELITE PRO
        </h1>
        <p style="color: #888; font-size: 0.9rem; letter-spacing: 2px;">
            TERMINAL DE ESTADO v5.0
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Status do sistema
    col_status1, col_status2, col_status3 = st.columns(3)
    with col_status1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-value" style="font-size: 1.2rem;">✅</div>
            <div class="kpi-label">Sistema</div>
            <div class="kpi-delta sentiment-positive">Operacional</div>
        </div>
        """, unsafe_allow_html=True)
    with col_status2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-value" style="font-size: 1.2rem;">🔐</div>
            <div class="kpi-label">Acesso</div>
            <div class="kpi-delta sentiment-positive">Administrator</div>
        </div>
        """, unsafe_allow_html=True)
    with col_status3:
        hora_atual = datetime.now().strftime('%H:%M:%S')
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value" style="font-size: 1.2rem;">🕐</div>
            <div class="kpi-label">Uptime</div>
            <div class="kpi-delta sentiment-neutral">{hora_atual}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grid de Cards
    st.markdown("<h3 style='color: #d4af37; font-family: JetBrains Mono; margin-bottom: 20px;'>📱 MÓDULOS DISPONÍVEIS</h3>", unsafe_allow_html=True)
    
    # Primeira linha de cards
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎯\n\n**DASHBOARD**\n\nExecutivo", key="btn_dashboard", use_container_width=True):
            abrir_modulo("dashboard")
            st.rerun()
    
    with col2:
        if st.button("💎\n\n**IA QUÂNTICO**\n\nTesla", key="btn_tesla", use_container_width=True):
            abrir_modulo("tesla")
            st.rerun()
    
    # Segunda linha
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("🐾\n\n**PET GLOBAL**\n\nIntelligence", key="btn_pet", use_container_width=True):
            abrir_modulo("pet")
            st.rerun()
    
    with col4:
        if st.button("💹\n\n**TRADE &**\n\nCommodities", key="btn_trade", use_container_width=True):
            abrir_modulo("trade")
            st.rerun()
    
    # Terceira linha
    col5, col6 = st.columns(2)
    
    with col5:
        if st.button("👗\n\n**FASHION**\n\nHigh-Ticket", key="btn_fashion", use_container_width=True):
            abrir_modulo("fashion")
            st.rerun()
    
    with col6:
        if st.button("🌍\n\n**SOBERANIA**\n\n& Reservas", key="btn_soberania", use_container_width=True):
            abrir_modulo("soberania")
            st.rerun()
    
    # Quarta linha
    col7, col8 = st.columns(2)
    
    with col7:
        if st.button("🙏\n\n**DEVOCIONAL**\n\nDe Poder", key="btn_devocional", use_container_width=True):
            abrir_modulo("devocional")
            st.rerun()
    
    with col8:
        if st.button("🤝\n\n**CONSELHO**\n\nDe Elite", key="btn_conselho", use_container_width=True):
            abrir_modulo("conselho")
            st.rerun()
    
    # Footer
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; padding: 20px; 
                background: linear-gradient(145deg, #0f0f1a, #1a1a2e);
                border-radius: 20px; border: 1px solid rgba(212, 175, 55, 0.2);">
        <p style="color: #666; font-size: 0.75rem; margin: 0;">
            <b style="color: #d4af37;">QUANTUM NEXUS ELITE PRO v5.0</b><br>
            Status: <span style="color: #00ff88;">PROTEGIDO POR CRIPTOGRAFIA</span><br>
            © 2026 - Todos os direitos reservados
        </p>
    </div>
    """, unsafe_allow_html=True)

# =================================================================
# 6. HEADER COM BOTÃO VOLTAR
# =================================================================

def render_header_com_voltar(titulo, icone):
    col1, col2 = st.columns([1, 8])
    
    with col1:
        if st.button("←", key="btn_voltar", help="Voltar ao menu"):
            voltar_menu()
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <h1 style="font-family: 'JetBrains Mono', monospace; color: #d4af37; 
                   font-size: 1.5rem; margin: 0; letter-spacing: 2px;">
            {icone} {titulo.upper()}
        </h1>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border-color: rgba(212, 175, 55, 0.2); margin: 15px 0 25px 0;'>", unsafe_allow_html=True)

# =================================================================
# 7. CONTEÚDO DOS MÓDULOS (ABSTRAÇÃO DAS TELAS)
# =================================================================

# Nota: As funções dos módulos (render_dashboard, render_tesla, etc.) 
# devem ser chamadas conforme a navegação.
