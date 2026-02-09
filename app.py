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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300 ;400;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
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
    [data-testid="stMetricDelta"] { 
        font-size: 1.2rem !important; 
        background: rgba(0,0,0,0.2);
        padding: 5px 10px;
        border-radius: 10px;
    }

    /* Mensagens de Estado (Devocional e Conselhos) */
    .state-message { 
        border-left: 10px solid #d4af37; 
        padding: 40px; 
        background: rgba(10, 10, 10, 0.8); 
        line-height: 2.4; 
        font-size: 1.25rem;
        border-radius: 0 40px 40px 0;
        box-shadow: 10px 10px 30px rgba(0,0,0,0.5);
        margin: 20px 0;
    }
    
    /* Card de Análise de Tendência */
    .trend-card {
        background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
        border: 1px solid #d4af37;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
    }
    
    /* Indicador de Sentimento */
    .sentiment-positive { color: #00ff88; font-weight: bold; }
    .sentiment-neutral { color: #ffd700; font-weight: bold; }
    .sentiment-negative { color: #ff4444; font-weight: bold; }

    /* Escondendo Elementos Desnecessários do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar de Luxo */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #d4af37; border-radius: 10px; }
    
    /* Tabelas Profissionais */
    .dataframe { 
        background-color: #0a0a0a !important;
        color: #fff !important;
    }
    .dataframe th {
        background-color: #1a1a1a !important;
        color: #d4af37 !important;
        font-weight: bold !important;
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
# 4. SIDEBAR - PAINEL DE COMANDO CENTRAL
# =================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>⚡ NEXUS ELITE PRO</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d4af37;'>SISTEMA DE ESTADO v5.0</p>", unsafe_allow_html=True)
    st.write("---")
    
    # Navegação por Módulos Profissionais
    menu = st.radio(
        "COMANDOS DISPONÍVEIS:", 
        [
            "🎯 Dashboard Executivo",
            "💎 IA Quântico Tesla", 
            "🐾 Pet Global Intelligence", 
            "💹 Trade & Commodities", 
            "👗 Fashion High-Ticket", 
            "🌍 Soberania & Reservas", 
            "🙏 Devocional de Poder", 
            "🤝 Conselho de Elite"
        ]
    )
    
    st.write("---")
    st.markdown("**Status:** ✅ Operacional")
    st.markdown("**Nível:** 🔐 Administrator")
    st.markdown(f"**Uptime:** {datetime.now().strftime('%H:%M:%S')}")
    
    # Métricas rápidas do mercado
    st.write("---")
    st.markdown("**📊 MERCADO GLOBAL**")
    try:
        sp500 = yf.Ticker("^GSPC").history(period="1d")
        if not sp500.empty:
            var_sp = ((sp500['Close'].iloc[-1] / sp500['Open'].iloc[-1]) - 1) * 100
            st.metric("S&P 500", f"{sp500['Close'].iloc[-1]:.0f}", f"{var_sp:+.2f}%")
    except:
        pass

# =================================================================
# 5. DASHBOARD EXECUTIVO (NOVO MÓDULO)
# =================================================================

if menu == "🎯 Dashboard Executivo":
    st.title("🎯 Dashboard Executivo de Alta Performance")
    
    st.markdown("""
    <div class='card-quantum'>
        Central de Comando com visão panorâmica de todos os ativos estratégicos, 
        tendências de mercado e indicadores de performance em tempo real.
    </div>
    """, unsafe_allow_html=True)
    
    # KPIs Principais
    st.subheader("📊 Indicadores-Chave de Performance (KPIs)")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    try:
        # Buscar dados de ativos principais
        tickers_principais = {
            "GC=F": "Ouro",
            "^GSPC": "S&P 500",
            "BTC-USD": "Bitcoin",
            "VALE3.SA": "Vale",
            "^BVSP": "Ibovespa"
        }
        
        for i, (ticker, nome) in enumerate(tickers_principais.items()):
            try:
                data = yf.Ticker(ticker).history(period="5d")
                if not data.empty:
                    atual = data['Close'].iloc[-1]
                    anterior = data['Close'].iloc[-2]
                    var = ((atual / anterior) - 1) * 100
                    
                    if i == 0:
                        col1.metric(nome, f"${atual:.0f}", f"{var:+.2f}%")
                    elif i == 1:
                        col2.metric(nome, f"{atual:.0f}", f"{var:+.2f}%")
                    elif i == 2:
                        col3.metric(nome, f"${atual:,.0f}", f"{var:+.2f}%")
                    elif i == 3:
                        col4.metric(nome, f"R${atual:.2f}", f"{var:+.2f}%")
                    else:
                        col5.metric(nome, f"{atual:,.0f}", f"{var:+.2f}%")
            except:
                continue
    except:
        st.info("Carregando dados do mercado...")
    
    st.write("---")
    
    # Gráfico de Correlação entre Ativos
    st.subheader("🔗 Mapa de Correlação de Ativos Estratégicos")
    
    col_corr1, col_corr2 = st.columns([2, 1])
    
    with col_corr1:
        try:
            ativos_corr = ["GC=F", "^GSPC", "BTC-USD", "VALE3.SA", "PETR4.SA"]
            dados_corr = pd.DataFrame()
            
            for ticker in ativos_corr:
                try:
                    hist = yf.download(ticker, period="90d", progress=False)['Close']
                    dados_corr[ticker] = hist
                except:
                    continue
            
            if not dados_corr.empty:
                correlacao = dados_corr.corr()
                
                fig_corr = go.Figure(data=go.Heatmap(
                    z=correlacao.values,
                    x=['Ouro', 'S&P500', 'Bitcoin', 'Vale', 'Petrobras'],
                    y=['Ouro', 'S&P500', 'Bitcoin', 'Vale', 'Petrobras'],
                    colorscale='RdYlGn',
                    zmid=0,
                    text=correlacao.values,
                    texttemplate='%{text:.2f}',
                    textfont={"size": 14},
                    colorbar=dict(title="Correlação")
                ))
                
                fig_corr.update_layout(
                    template='plotly_dark',
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    height=400,
                    title="Matriz de Correlação (90 dias)"
                )
                
                st.plotly_chart(fig_corr, use_container_width=True)
        except Exception as e:
            st.warning("Carregando mapa de correlação...")
    
    with col_corr2:
        st.markdown("""
        <div class='trend-card'>
            <h4 style='color: #d4af37;'>💡 Insights de Correlação</h4>
            <p style='font-size: 0.9rem; line-height: 1.6;'>
                <b>Correlação Positiva (>0.5):</b><br>
                Ativos se movem juntos. Ideal para confirmar tendências.<br><br>
                
                <b>Correlação Negativa (<-0.5):</b><br>
                Ativos se movem em direções opostas. Perfeito para hedge.<br><br>
                
                <b>Correlação Neutra (~0):</b><br>
                Movimentos independentes. Ótimo para diversificação.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Ranking de Performance Semanal
    st.subheader("🏆 Top Performers da Semana")
    
    try:
        ativos_ranking = {
            "AAPL": "Apple", "GOOGL": "Google", "MSFT": "Microsoft",
            "VALE3.SA": "Vale", "PETR4.SA": "Petrobras", "ITUB4.SA": "Itaú",
            "GC=F": "Ouro", "SI=F": "Prata", "BTC-USD": "Bitcoin"
        }
        
        performance = []
        for ticker, nome in ativos_ranking.items():
            try:
                data = yf.download(ticker, period="7d", progress=False)
                if not data.empty and len(data) >= 2:
                    retorno = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
                    performance.append({'Ativo': nome, 'Retorno 7D (%)': retorno, 'Ticker': ticker})
            except:
                continue
        
        if performance:
            df_performance = pd.DataFrame(performance).sort_values('Retorno 7D (%)', ascending=False)
            
            # Gráfico de barras horizontal
            fig_rank = go.Figure(go.Bar(
                x=df_performance['Retorno 7D (%)'],
                y=df_performance['Ativo'],
                orientation='h',
                marker=dict(
                    color=df_performance['Retorno 7D (%)'],
                    colorscale='RdYlGn',
                    cmid=0
                ),
                text=df_performance['Retorno 7D (%)'].apply(lambda x: f'{x:+.2f}%'),
                textposition='outside'
            ))
            
            fig_rank.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=400,
                title="Performance Semanal dos Ativos",
                xaxis_title="Retorno (%)",
                showlegend=False
            )
            
            st.plotly_chart(fig_rank, use_container_width=True)
    except:
        st.info("Carregando ranking de performance...")
    
    # Análise de Sentimento do Mercado (Simulada)
    st.write("---")
    st.subheader("🧠 Índice de Sentimento do Mercado")
    
    col_sent1, col_sent2, col_sent3 = st.columns(3)
    
    # Simular sentimento baseado na volatilidade do S&P 500
    try:
        sp_data = yf.download("^GSPC", period="30d", progress=False)
        if not sp_data.empty:
            volatilidade = sp_data['Close'].pct_change().std() * 100
            retorno_mensal = ((sp_data['Close'].iloc[-1] / sp_data['Close'].iloc[0]) - 1) * 100
            
            # Determinar sentimento
            if retorno_mensal > 3 and volatilidade < 1.5:
                sentimento = "OTIMISTA"
                cor_sent = "sentiment-positive"
                emoji_sent = "🚀"
                score = 85
            elif retorno_mensal < -3 or volatilidade > 2:
                sentimento = "PESSIMISTA"
                cor_sent = "sentiment-negative"
                emoji_sent = "⚠️"
                score = 35
            else:
                sentimento = "NEUTRO"
                cor_sent = "sentiment-neutral"
                emoji_sent = "⚖️"
                score = 60
            
            col_sent1.markdown(f"""
            <div class='trend-card' style='text-align: center;'>
                <h2 style='font-size: 4rem; margin: 0;'>{emoji_sent}</h2>
                <h3 class='{cor_sent}' style='margin: 10px 0;'>{sentimento}</h3>
                <p style='color: #888;'>Score: {score}/100</p>
            </div>
            """, unsafe_allow_html=True)
            
            col_sent2.metric("Volatilidade 30D", f"{volatilidade:.2f}%", 
                           "Alto" if volatilidade > 2 else "Baixo" if volatilidade < 1 else "Médio")
            col_sent3.metric("Retorno 30D", f"{retorno_mensal:+.2f}%")
    except:
        pass

# =================================================================
# 6. MÓDULO: IA QUÂNTICO TESLA
# =================================================================

elif menu == "💎 IA Quântico Tesla":
    st.title("💎 IA Quântico Tesla & Astrolábio")
    st.markdown("""
        <div class='card-quantum'>
            Este módulo utiliza a Matemática de Vórtice para identificar padrões de confluência 
            em jogos de alta volatilidade. A análise foca no equilíbrio geométrico dos números 
            baseado nas frequências 3-6-9 de Nikola Tesla.
        </div>
    """, unsafe_allow_html=True)
    
    # Interface de Seleção
    col_j1, col_j2, col_j3 = st.columns([2, 1, 1])
    with col_j1:
        jogo = st.selectbox(
            "Selecione a Modalidade Operacional:", 
            ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"]
        )
    with col_j2:
        esfera = st.select_slider(
            "Frequência (Hz):", 
            options=[369, 432, 528, 963],
            help="Sintonização da frequência de cálculo Tesla."
        )
    with col_j3:
        num_jogos = st.number_input("Nº de Jogos:", min_value=1, max_value=10, value=1)

    # Botão de Ativação do Algoritmo
    if st.button("⚡ EXECUTAR CONFLUÊNCIA DE VÓRTICE"):
        configs = {
            "Mega-Sena": (60, 6), 
            "Lotofácil": (25, 15), 
            "Quina": (80, 5), 
            "Lotomania": (100, 50), 
            "Milionária": (50, 6)
        }
        
        n_max, n_qtd = configs[jogo]
        
        # Gerar múltiplos jogos
        for i in range(num_jogos):
            nums, trevos = logic_astrolabio_tesla(n_max, n_qtd, jogo)
            
            # Exibição dos Números Principais
            st.markdown(f"""
                <div class='card-quantum' style='text-align: center; border: 2px solid #d4af37; margin-bottom: 20px;'>
                    <h4 style='color: #888; letter-spacing: 5px;'>JOGO #{i+1} - NÚMEROS IDENTIFICADOS</h4>
                    <h1 style='font-size: 3.2rem; color: #FFF; text-shadow: 0 0 20px rgba(212,175,55,0.5);'>
                        {', '.join(map(str, nums))}
                    </h1>
                </div>
            """, unsafe_allow_html=True)
            
            # Exibição Especial para os Trevos da Milionária
            if jogo == "Milionária" and trevos:
                st.markdown(f"""
                    <div style='text-align: center; margin-top: -15px; margin-bottom: 30px;'>
                        <h3 style='color: #d4af37; font-family: "JetBrains Mono";'>
                            ☘️ TREVOS DA SORTE: 
                            <span style='color:#FFF; border: 1px solid #d4af37; padding: 5px 15px; border-radius: 10px;'>{trevos[0]}</span> 
                            e 
                            <span style='color:#FFF; border: 1px solid #d4af37; padding: 5px 15px; border-radius: 10px;'>{trevos[1]}</span>
                        </h3>
                    </div>
                """, unsafe_allow_html=True)
        
        # Análise do padrão gerado
        st.write("---")
        st.subheader("📊 Análise do Padrão Vórtice")
        
        col_a1, col_a2 = st.columns(2)
        
        with col_a1:
            # Análise de distribuição
            pares = sum(1 for n in nums if n % 2 == 0)
            impares = len(nums) - pares
            
            fig_dist = go.Figure(data=[go.Pie(
                labels=['Pares', 'Ímpares'],
                values=[pares, impares],
                hole=0.4,
                marker=dict(colors=['#d4af37', '#888'])
            )])
            
            fig_dist.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                title="Distribuição Par/Ímpar",
                height=300
            )
            
            st.plotly_chart(fig_dist, use_container_width=True)
        
        with col_a2:
            # Análise de redução Tesla (3-6-9)
            def reduzir(n):
                while n > 9:
                    n = sum(int(d) for d in str(n))
                return n
            
            reducoes = [reduzir(n) for n in nums]
            tesla_nums = sum(1 for r in reducoes if r in [3, 6, 9])
            outros = len(reducoes) - tesla_nums
            
            fig_tesla = go.Figure(data=[go.Pie(
                labels=['Vórtice (3-6-9)', 'Outros'],
                values=[tesla_nums, outros],
                hole=0.4,
                marker=dict(colors=['#00ff88', '#444'])
            )])
            
            fig_tesla.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                title="Frequência Vórtice Tesla",
                height=300
            )
            
            st.plotly_chart(fig_tesla, use_container_width=True)
        
        st.markdown(f"""
        <div class='trend-card'>
            <h4 style='color: #d4af37;'>⚡ Análise Energética do Padrão</h4>
            <p style='line-height: 1.8;'>
                O jogo gerado possui <b>{pares} números pares</b> e <b>{impares} números ímpares</b>, 
                criando um equilíbrio energético de <b>{(pares/len(nums)*100):.1f}% / {(impares/len(nums)*100):.1f}%</b>.<br><br>
                
                <b>Frequência Vórtice:</b> {tesla_nums} dos {len(nums)} números ({(tesla_nums/len(nums)*100):.1f}%) 
                possuem redução numérica no padrão 3-6-9, considerado por Tesla como a "chave do universo".<br><br>
                
                <b>Frequência de Sintonização:</b> {esfera}Hz - Associada a {'manifestação e criatividade' if esfera == 369 
                else 'harmonia e equilíbrio' if esfera == 432 
                else 'transformação e cura' if esfera == 528 
                else 'conexão espiritual e intuição'}.
            </p>
        </div>
        """, unsafe_allow_html=True)

# =================================================================
# 7. MÓDULO: PET GLOBAL INTELLIGENCE (NOVO - IMPLEMENTADO)
# =================================================================

elif menu == "🐾 Pet Global Intelligence":
    st.title("🐾 Pet Global Intelligence & Market Analysis")
    
    st.markdown("""
        <div class='card-quantum'>
            Análise profunda do mercado Pet global e nacional. Monitoramento de tendências, 
            empresas líderes, oportunidades de investimento e insights para e-commerce especializado.
        </div>
    """, unsafe_allow_html=True)
    
    # KPIs do Mercado Pet
    st.subheader("📊 Panorama do Mercado Pet Global")
    
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    
    col_p1.metric("Mercado Global 2024", "US$ 261 Bi", "+8.5% YoY")
    col_p2.metric("Mercado Brasil 2024", "R$ 66 Bi", "+12% YoY")
    col_p3.metric("Pets no Brasil", "162 Milhões", "1º em AL")
    col_p4.metric("CAGR 2024-2030", "9.2%", "Projeção")
    
    st.write("---")
    
    # Gráfico de evolução do mercado
    st.subheader("📈 Evolução do Mercado Pet (Brasil)")
    
    anos = ['2020', '2021', '2022', '2023', '2024', '2025E', '2026E']
    valores = [40.8, 47.2, 54.5, 59.0, 66.0, 73.9, 82.8]
    
    fig_evolucao = go.Figure(data=[go.Scatter(
        x=anos,
        y=valores,
        mode='lines+markers+text',
        line=dict(color='#d4af37', width=3),
        marker=dict(size=12, color='#d4af37'),
        text=[f'R${v}B' for v in valores],
        textposition='top center',
        textfont=dict(size=14, color='#fff')
    )])
    
    fig_evolucao.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        title="Crescimento do Mercado Pet Brasileiro (R$ Bilhões)",
        xaxis_title="Ano",
        yaxis_title="Valor (R$ Bilhões)",
        yaxis=dict(showgrid=True, gridcolor='#222')
    )
    
    st.plotly_chart(fig_evolucao, use_container_width=True)
    
    st.write("---")
    
    # Segmentação do mercado
    st.subheader("🎯 Segmentação por Categoria")
    
    col_seg1, col_seg2 = st.columns([2, 1])
    
    with col_seg1:
        categorias = ['Alimentação', 'Veterinária', 'Pet Care', 'Acessórios', 'Pet Tech']
        participacao = [67, 15, 10, 5, 3]
        
        fig_seg = go.Figure(data=[go.Bar(
            x=categorias,
            y=participacao,
            marker_color=['#d4af37', '#b8922a', '#9c791d', '#816111', '#6b541a'],
            text=[f'{p}%' for p in participacao],
            textposition='outside'
        )])
        
        fig_seg.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400,
            title="Participação por Categoria (%)",
            showlegend=False
        )
        
        st.plotly_chart(fig_seg, use_container_width=True)
    
    with col_seg2:
        st.markdown("""
        <div class='trend-card'>
            <h4 style='color: #d4af37;'>💡 Insights Estratégicos</h4>
            <p style='font-size: 0.85rem; line-height: 1.6;'>
                <b>Alimentação Premium:</b> Segmento com maior margem, crescimento de 15% a.a.<br><br>
                
                <b>Pet Tech:</b> Categoria emergente, crescimento de 35% a.a. Apps, wearables e telemedicina.<br><br>
                
                <b>E-commerce:</b> 28% das vendas já são online, projetado para 45% em 2026.<br><br>
                
                <b>Mercado B2B:</b> Oportunidade em supplies para pet shops e veterinárias.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Empresas líderes
    st.subheader("🏢 Players Dominantes do Mercado")
    
    col_emp1, col_emp2 = st.columns(2)
    
    with col_emp1:
        st.markdown("""
        <div class='trend-card'>
            <h4 style='color: #d4af37;'>🌎 Global</h4>
            <table style='width: 100%; color: #ccc;'>
                <tr style='border-bottom: 1px solid #333;'>
                    <td style='padding: 10px;'><b>Mars Petcare</b></td>
                    <td style='padding: 10px; text-align: right;'>~US$ 20B</td>
                </tr>
                <tr style='border-bottom: 1px solid #333;'>
                    <td style='padding: 10px;'><b>Nestlé Purina</b></td>
                    <td style='padding: 10px; text-align: right;'>~US$ 18B</td>
                </tr>
                <tr style='border-bottom: 1px solid #333;'>
                    <td style='padding: 10px;'><b>Hill's (Colgate)</b></td>
                    <td style='padding: 10px; text-align: right;'>~US$ 3.5B</td>
                </tr>
                <tr>
                    <td style='padding: 10px;'><b>PetSmart</b></td>
                    <td style='padding: 10px; text-align: right;'>~US$ 8B</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    with col_emp2:
        st.markdown("""
        <div class='trend-card'>
            <h4 style='color: #d4af37;'>🇧🇷 Brasil</h4>
            <table style='width: 100%; color: #ccc;'>
                <tr style='border-bottom: 1px solid #333;'>
                    <td style='padding: 10px;'><b>Petz (PETZ3)</b></td>
                    <td style='padding: 10px; text-align: right;'>~R$ 4B</td>
                </tr>
                <tr style='border-bottom: 1px solid #333;'>
                    <td style='padding: 10px;'><b>Cobasi</b></td>
                    <td style='padding: 10px; text-align: right;'>~R$ 2.5B</td>
                </tr>
                <tr style='border-bottom: 1px solid #333;'>
                    <td style='padding: 10px;'><b>Total Alimentos</b></td>
                    <td style='padding: 10px; text-align: right;'>~R$ 2B</td>
                </tr>
                <tr>
                    <td style='padding: 10px;'><b>Petlove</b></td>
                    <td style='padding: 10px; text-align: right;'>~R$ 1.5B</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Oportunidades para E-commerce
    st.subheader("💰 Oportunidades de Alto Retorno para E-commerce")
    
    oportunidades = [
        {
            'titulo': '🥩 Alimentação Natural & Premium',
            'descricao': 'Rações super premium, alimentos congelados, dieta BARF. Margem: 40-60%. Ticket médio: R$ 200-400/mês.',
            'potencial': 'MUITO ALTO',
            'cor': 'sentiment-positive'
        },
        {
            'titulo': '💊 Nutraceuticals & Suplementos',
            'descricao': 'Vitaminas, probióticos, suplementos articulares. Margem: 50-70%. Crescimento: 25% a.a.',
            'potencial': 'ALTO',
            'cor': 'sentiment-positive'
        },
        {
            'titulo': '🎁 Assinatura & Clube de Benefícios',
            'descricao': 'Box mensal, descontos recorrentes, fidelização. LTV alto, baixo CAC após setup.',
            'potencial': 'ALTO',
            'cor': 'sentiment-positive'
        },
        {
            'titulo': '🏥 Telemedicina Veterinária',
            'descricao': 'Consultas online, segunda opinião, exames. Modelo SaaS escalável.',
            'potencial': 'MÉDIO-ALTO',
            'cor': 'sentiment-neutral'
        },
        {
            'titulo': '🎮 Pet Tech & Gadgets',
            'descricao': 'Coleiras GPS, câmeras, comedouros inteligentes. Ticket alto (R$ 300-800).',
            'potencial': 'MÉDIO',
            'cor': 'sentiment-neutral'
        }
    ]
    
    for oport in oportunidades:
        st.markdown(f"""
        <div class='trend-card'>
            <h4 style='color: #d4af37;'>{oport['titulo']}</h4>
            <p style='line-height: 1.6; color: #ccc;'>{oport['descricao']}</p>
            <p style='margin-top: 10px;'>
                <b>Potencial de Retorno:</b> <span class='{oport['cor']}'>{oport['potencial']}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Análise de tendências
    st.subheader("📡 Tendências Emergentes 2024-2026")
    
    tendencias = {
        'Humanização': 85,
        'Sustentabilidade': 72,
        'Saúde Preventiva': 78,
        'Personalização': 68,
        'Conveniência (entrega)': 90,
        'Pet Parenting': 82
    }
    
    fig_tend = go.Figure(go.Bar(
        x=list(tendencias.values()),
        y=list(tendencias.keys()),
        orientation='h',
        marker=dict(
            color=list(tendencias.values()),
            colorscale='YlOrRd',
            showscale=False
        ),
        text=[f'{v}%' for v in tendencias.values()],
        textposition='outside'
    ))
    
    fig_tend.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=400,
        title="Índice de Adoção das Tendências (%)",
        xaxis_title="Adoção (%)"
    )
    
    st.plotly_chart(fig_tend, use_container_width=True)
    
    # Recomendações estratégicas
    st.markdown("""
    <div class='state-message'>
        <h3 style='color: #d4af37; margin-top: 0;'>🎯 RECOMENDAÇÕES ESTRATÉGICAS</h3>
        <p style='line-height: 1.8;'>
            <b>Para E-commerce de Alto Ticket:</b><br>
            • Foco em alimentação premium e nutraceuticals (margens de 50%+)<br>
            • Implementar modelo de assinatura para previsibilidade de receita<br>
            • Investir em conteúdo educacional para posicionamento de autoridade<br>
            • Parcerias estratégicas com veterinários para indicação<br><br>
            
            <b>Canais de Aquisição com Melhor ROI:</b><br>
            • Google Ads (palavras long-tail específicas): ROI 3-5x<br>
            • Instagram/Facebook (público 25-45 anos, renda A/B): ROI 2-4x<br>
            • Parcerias com influenciadores pet: ROI 4-7x<br>
            • Marketing de Conteúdo (SEO): ROI 8-12x (longo prazo)<br><br>
            
            <b>Ticket Médio Ideal:</b> R$ 300-500 para viabilidade logística e margem competitiva.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =================================================================
# 8. MÓDULO: TRADE & COMMODITIES
# =================================================================

elif menu == "💹 Trade & Commodities":
    st.title("💹 Terminal de Trading Profissional")
    st.markdown("""
        <div class='card-quantum'>
            Monitoramento de ativos de alta liquidez e reserva de valor com análise técnica avançada.
        </div>
    """, unsafe_allow_html=True)
    
    # Seleção de ativo
    col_t1, col_t2 = st.columns([3, 1])
    
    with col_t1:
        ativo_trade = st.selectbox(
            "Selecione o Ativo para Análise Completa:",
            [
                "GC=F (Ouro Futuro)",
                "SI=F (Prata Futuro)",
                "CL=F (Petróleo WTI)",
                "BTC-USD (Bitcoin)",
                "ETH-USD (Ethereum)",
                "^GSPC (S&P 500)",
                "^DJI (Dow Jones)",
                "VALE3.SA (Vale)",
                "PETR4.SA (Petrobras)"
            ]
        )
    
    with col_t2:
        periodo_analise = st.selectbox(
            "Período:",
            ["90d", "180d", "1y", "2y"],
            index=1
        )
    
    ticker_trade = ativo_trade.split(" (")[0]
    
    # Renderizar análise técnica completa
    render_analise_tecnica_avancada(ticker_trade, ativo_trade)
    
    st.write("---")
    
    # Comparativo de commodities
    st.subheader("📊 Painel Comparativo de Commodities")
    
    commodities = {
        "GC=F": "Ouro",
        "SI=F": "Prata",
        "CL=F": "Petróleo",
        "NG=F": "Gás Natural",
        "HG=F": "Cobre"
    }
    
    col_comm1, col_comm2 = st.columns([2, 1])
    
    with col_comm1:
        # Gráfico de performance comparativa
        dados_comp = pd.DataFrame()
        
        for ticker, nome in commodities.items():
            try:
                hist = yf.download(ticker, period="180d", progress=False)['Close']
                if not hist.empty:
                    # Normalizar para base 100
                    hist_norm = (hist / hist.iloc[0]) * 100
                    dados_comp[nome] = hist_norm
            except:
                continue
        
        if not dados_comp.empty:
            fig_comp = go.Figure()
            
            cores = ['#d4af37', '#c0c0c0', '#000000', '#ff6b6b', '#ff8800']
            
            for i, col in enumerate(dados_comp.columns):
                fig_comp.add_trace(go.Scatter(
                    x=dados_comp.index,
                    y=dados_comp[col],
                    mode='lines',
                    name=col,
                    line=dict(color=cores[i], width=2.5)
                ))
            
            fig_comp.update_layout(
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=450,
                title="Performance Comparativa (Base 100)",
                yaxis_title="Índice (Base 100)",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_comp, use_container_width=True)
    
    with col_comm2:
        # Tabela de performance
        st.markdown("<h4 style='color: #d4af37;'>Performance 180D</h4>", unsafe_allow_html=True)
        
        perf_data = []
        for ticker, nome in commodities.items():
            try:
                hist = yf.download(ticker, period="180d", progress=False)
                if not hist.empty and len(hist) > 1:
                    retorno = ((hist['Close'].iloc[-1] / hist['Close'].iloc[0]) - 1) * 100
                    perf_data.append({'Commodity': nome, 'Retorno (%)': f"{retorno:+.2f}%"})
            except:
                continue
        
        if perf_data:
            df_perf = pd.DataFrame(perf_data)
            st.dataframe(df_perf, use_container_width=True, hide_index=True)

# =================================================================
# 9. MÓDULO: FASHION HIGH-TICKET
# =================================================================

elif menu == "👗 Fashion High-Ticket":
    st.title("👗 Radar Fashion Luxo & Market Share")
    st.markdown("""
        <div class='card-quantum'>
            Análise das detentoras das marcas mais valiosas do mundo com foco em exclusividade e alto valor de marca.
        </div>
    """, unsafe_allow_html=True)
    
    # Seleção de marca
    f_marca = st.selectbox(
        "Selecione o Ativo High-Ticket:",
        [
            "MC.PA (LVMH - Louis Vuitton/Dior)",
            "RMS.PA (Hermès)",
            "KER.PA (Kering - Gucci/YSL)",
            "ARZZ3.SA (Arezzo Brasil)",
            "SOMA3.SA (Grupo Soma)"
        ]
    )
    
    ticker_f = f_marca.split(" (")[1].split(")")[0]
    
    # Análise técnica do ativo
    render_analise_tecnica_avancada(ticker_f, f_marca)
    
    st.write("---")
    
    # Ranking de marcas de luxo
    st.subheader("👑 Top 10 Marcas de Luxo Global (Valor de Marca)")
    
    marcas = ['Louis Vuitton', 'Hermès', 'Gucci', 'Chanel', 'Dior', 'Cartier', 'Rolex', 'Prada', 'Burberry', 'Fendi']
    valores = [124.8, 110.5, 89.2, 78.1, 71.4, 65.3, 61.2, 52.8, 48.6, 42.1]
    
    fig_marcas = go.Figure(go.Bar(
        x=valores,
        y=marcas,
        orientation='h',
        marker=dict(
            color=valores,
            colorscale='YlOrBr',
            showscale=False
        ),
        text=[f'${v}B' for v in valores],
        textposition='outside'
    ))
    
    fig_marcas.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        title="Valor de Marca 2024 (US$ Bilhões)",
        xaxis_title="Valor (US$ Bilhões)"
    )
    
    st.plotly_chart(fig_marcas, use_container_width=True)
    
    st.write("---")
    
    # Insights do mercado de luxo
    st.subheader("💎 Análise do Mercado de Luxo")
    
    col_lux1, col_lux2, col_lux3 = st.columns(3)
    
    col_lux1.metric("Mercado Global 2024", "€ 362 Bi", "+8% YoY")
    col_lux2.metric("E-commerce Luxo", "23%", "+5pp vs 2023")
    col_lux3.metric("Margem EBITDA Média", "28%", "Hermès: 42%")
    
    st.markdown("""
    <div class='trend-card'>
        <h4 style='color: #d4af37;'>🎯 Tendências High-Ticket 2024-2025</h4>
        <ul style='line-height: 1.8;'>
            <li><b>Clientela Chinesa:</b> Representa 40% do consumo global de luxo</li>
            <li><b>Experiencialização:</b> Lojas-conceito e eventos exclusivos ganham força</li>
            <li><b>Resale Market:</b> Mercado de revenda de luxo cresce 65% (Vestiaire, Farfetch)</li>
            <li><b>Sustentabilidade Premium:</b> Materiais eco-luxury com markup de 30-50%</li>
            <li><b>Personalização:</b> Made-to-order com margens de 80%+</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =================================================================
# 10. MÓDULO: SOBERANIA & RESERVAS
# =================================================================

elif menu == "🌍 Soberania & Reservas":
    st.title("🌍 Soberania Nacional e Reservas Mundiais")
    st.markdown("""
        <div class='card-quantum'>
            Monitoramento de ativos que compõem o lastro de segurança das nações.
        </div>
    """, unsafe_allow_html=True)
    
    # Gráfico de preço do Ouro
    st.subheader("🥇 Terminal Operacional: Ouro (GC=F)")
    render_analise_tecnica_avancada("GC=F", "Ouro Futuro")
    
    st.write("---")
    
    # Reservas internacionais de ouro
    st.subheader("🌎 Top 10 Reservas Oficiais de Ouro")
    
    col_int1, col_int2 = st.columns([3, 2])
    
    paises_int = ['EUA', 'Alemanha', 'Itália', 'França', 'Rússia', 'China', 'Suíça', 'Japão', 'Índia', 'Holanda']
    toneladas_int = [8133, 3352, 2452, 2437, 2332, 2191, 1040, 846, 800, 612]
    
    with col_int1:
        fig_bar_int = go.Figure(data=[go.Bar(
            x=paises_int,
            y=toneladas_int,
            marker_color='#d4af37',
            text=[f"{t}t" for t in toneladas_int],
            textposition='outside'
        )])
        
        fig_bar_int.update_layout(
            title="Reservas Oficiais (Toneladas)",
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig_bar_int, use_container_width=True)
    
    with col_int2:
        fig_pie_int = go.Figure(data=[go.Pie(
            labels=paises_int,
            values=toneladas_int,
            hole=.4,
            marker=dict(colors=['#d4af37', '#b8922a', '#9c791d', '#816111', '#6b541a',
                               '#524013', '#392c0d', '#282828', '#1a1a1a', '#000'])
        )])
        
        fig_pie_int.update_layout(
            title="% Ocupação no Top 10",
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig_pie_int, use_container_width=True)
    
    st.write("---")
    
    # Ativos estratégicos brasileiros
    st.subheader("🇧🇷 Top 10 Ativos de Soberania Nacional")
    
    col_br1, col_br2 = st.columns([3, 2])
    
    ativos_br = ['VALE3', 'PETR4', 'ELET3', 'CSNA3', 'GGBR4', 'VBBR3', 'CMIG4', 'CPFE3', 'SUZB3', 'KLBN11']
    market_cap_br = [310, 420, 95, 25, 38, 22, 28, 40, 65, 24]
    
    with col_br1:
        fig_bar_br = go.Figure(data=[go.Bar(
            x=ativos_br,
            y=market_cap_br,
            marker_color='#888',
            text=[f"R${v}B" for v in market_cap_br],
            textposition='outside'
        )])
        
        fig_bar_br.update_layout(
            title="Capitalização Estratégica (Bilhões BRL)",
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig_bar_br, use_container_width=True)
    
    with col_br2:
        fig_pie_br = go.Figure(data=[go.Pie(
            labels=ativos_br,
            values=market_cap_br,
            hole=.4
        )])
        
        fig_pie_br.update_layout(
            title="% Relevância Patrimonial",
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        st.plotly_chart(fig_pie_br, use_container_width=True)
    
    st.markdown("""
    <div class='state-message'>
        <b>ANÁLISE DE ESTADO:</b> A soberania brasileira é sustentada pela matriz energética e mineral.
        A dominância global no Nióbio e a autossuficiência da Petrobras garantem poder de negociação no BRICS+.
        Aumentar a reserva física de Ouro é estratégico para estabilidade do Real no cenário global.
    </div>
    """, unsafe_allow_html=True)

# =================================================================
# 11. MÓDULO: DEVOCIONAL DE PODER (NOVO - IMPLEMENTADO)
# =================================================================

elif menu == "🙏 Devocional de Poder":
    st.title("🙏 Devocional de Poder & Alinhamento")
    
    st.markdown("""
    <div class='card-quantum'>
        Centro de alinhamento espiritual e mental para operadores de elite. 
        Antes de qualquer decisão de mercado, alinhe seu estado interior com princípios fundamentais.
    </div>
    """, unsafe_allow_html=True)
    
    # Seção Alfa e Ômega
    col_d1, col_d2 = st.columns([1, 2])
    
    with col_d1:
        st.markdown("""
        <div style='text-align: center; padding: 20px; border: 2px solid #d4af37; border-radius: 100%; 
                    width: 250px; height: 250px; margin: 0 auto; display: flex; 
                    align-items: center; justify-content: center;'>
            <h1 style='color: #d4af37; font-size: 5rem; margin: 0;'>Ω</h1>
        </div>
        <p align='center' style='color: #d4af37; margin-top: 15px; letter-spacing: 3px;'>
            <b>O ALFA E O ÔMEGA</b>
        </p>
        """, unsafe_allow_html=True)
    
    with col_d2:
        st.markdown("""
        <h3 style='color: #d4af37;'>O PRINCÍPIO DA DEPENDÊNCIA SOBERANA</h3>
        <p style='line-height: 1.8; color: #eee; font-size: 1.1rem;'>
            O verdadeiro operador de elite reconhece que a inteligência artificial, os gráficos de candlestick 
            e as reservas de nióbio são apenas ferramentas. A <b>Fonte Primária</b> de toda ideia, 
            de todo "feeling" de mercado e de toda oportunidade é DEUS.<br><br>
            
            Governar ativos sem estar conectado ao Criador é apenas acumulação. 
            Governar sob a instrução d'Ele é <b>cumprir um propósito</b>. 
            Neste terminal, buscamos não apenas o lucro, mas a Sabedoria que vem do alto (Tiago 1:5), 
            que é pura, pacífica e cheia de bons frutos.
        </p>
        """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Decretos diários
    st.subheader("📜 Decretos de Alinhamento Diário")
    
    st.markdown("""
    <div class='card-quantum' style='background: linear-gradient(180deg, #050505 0%, #111 100%); 
                                      border: 1px solid #d4af37;'>
        <table style='width: 100%; border-collapse: collapse; color: #ccc;'>
            <tr style='border-bottom: 1px solid #222;'>
                <td style='padding: 15px; color: #d4af37; width: 20%;'><b>IDENTIDADE</b></td>
                <td style='padding: 15px;'>
                    Eu sou um gestor designado por Deus para dominar sobre os recursos da terra. 
                    Minha autoridade vem do Criador, não do mercado.
                </td>
            </tr>
            <tr style='border-bottom: 1px solid #222;'>
                <td style='padding: 15px; color: #d4af37;'><b>PROVISÃO</b></td>
                <td style='padding: 15px;'>
                    Minha segurança não vem do índice da bolsa, mas da Fonte que criou o ouro e a prata. 
                    Ele é o dono de tudo (Salmos 24:1).
                </td>
            </tr>
            <tr style='border-bottom: 1px solid #222;'>
                <td style='padding: 15px; color: #d4af37;'><b>DIREÇÃO</b></td>
                <td style='padding: 15px;'>
                    Peço discernimento para enxergar oportunidades onde outros veem caos. 
                    "Os passos do homem são dirigidos pelo Senhor" (Provérbios 16:9).
                </td>
            </tr>
            <tr style='border-bottom: 1px solid #222;'>
                <td style='padding: 15px; color: #d4af37;'><b>INTEGRIDADE</b></td>
                <td style='padding: 15px;'>
                    Rejeito atalhos desonrosos. Meu lucro será limpo, meu processo será transparente, 
                    minha palavra será firme.
                </td>
            </tr>
            <tr>
                <td style='padding: 15px; color: #d4af37;'><b>TRANSBORDO</b></td>
                <td style='padding: 15px;'>
                    O lucro gerado neste terminal servirá para abençoar famílias, gerar empregos 
                    e estabelecer o Reino. Não acumulo para mim, multiplico para muitos.
                </td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Versículos estratégicos
    st.subheader("📖 Fundamentos Escriturísticos para Gestão")
    
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.markdown("""
        <div class='trend-card'>
            <h4 style='color: #d4af37;'>💰 Sobre Riqueza & Prosperidade</h4>
            <p style='line-height: 1.8;'>
                <b>"Lembra-te do Senhor teu Deus, porque é ele que te dá força para adquirires riqueza."</b><br>
                <i>Deuteronômio 8:18</i><br><br>
                
                <b>"O abençoado do Senhor é que enriquece, e ele não lhe acrescenta dores."</b><br>
                <i>Provérbios 10:22</i><br><br>
                
                <b>"Trazei todos os dízimos... e provai-me nisto, diz o Senhor dos Exércitos, 
                se eu não vos abrir as janelas do céu."</b><br>
                <i>Malaquias 3:10</i>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_v2:
        st.markdown("""
        <div class='trend-card'>
            <h4 style='color: #d4af37;'>🧠 Sobre Sabedoria & Decisão</h4>
            <p style='line-height: 1.8;'>
                <b>"Se algum de vós tem falta de sabedoria, peça-a a Deus, que a todos dá liberalmente."</b><br>
                <i>Tiago 1:5</i><br><br>
                
                <b>"Confia no Senhor de todo o teu coração e não te estribes no teu próprio entendimento."</b><br>
                <i>Provérbios 3:5-6</i><br><br>
                
                <b>"Os planos do diligente tendem à abundância, mas todo precipitado à penúria."</b><br>
                <i>Provérbios 21:5</i>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Protocolo de oração pré-operacional
    st.subheader("🕊️ Protocolo de Oração Pré-Operacional")
    
    st.markdown("""
    <div class='state-message' style='background: linear-gradient(145deg, #0a0a0a, #000); 
                                       border: 2px solid #d4af37;'>
        <h4 style='color: #d4af37; text-align: center; margin-top: 0;'>ORAÇÃO DO TRADER DE ELITE</h4>
        <p style='line-height: 2; font-size: 1.15rem; text-align: justify;'>
            Senhor, diante deste terminal reconheço que toda sabedoria vem de Ti. 
            Peço clareza mental para analisar os dados, discernimento para identificar as oportunidades verdadeiras, 
            e autocontrole para não agir por impulso ou ganância.<br><br>
            
            Que meu lucro seja resultado de esforço disciplinado e não de especulação irresponsável. 
            Que minhas decisões honrem Teu nome e abençoem minha família.<br><br>
            
            Declaro que minha confiança não está nos gráficos, mas em Ti, 
            que és o Senhor da economia celestial e terrena.<br><br>
            
            Em nome de Jesus, amém.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Checkpoint de reflexão
    st.subheader("✅ Checkpoint de Consciência")
    
    col_check1, col_check2 = st.columns(2)
    
    with col_check1:
        st.markdown("<h4 style='color: #d4af37;'>Antes de Operar:</h4>", unsafe_allow_html=True)
        
        check1 = st.checkbox("Orei e busquei direção divina")
        check2 = st.checkbox("Estou emocionalmente equilibrado")
        check3 = st.checkbox("Tenho um plano de stop-loss definido")
        check4 = st.checkbox("Não estou operando por FOMO ou vingança")
        check5 = st.checkbox("Meu risco está dentro do aceitável (máx 2-3% do capital)")
        
        if check1 and check2 and check3 and check4 and check5:
            st.success("✅ LIBERADO PARA OPERAÇÃO - Estado Mental Alinhado")
        else:
            st.warning("⚠️ REVISAR PROTOCOLO - Alguns checkpoints não foram confirmados")
    
    with col_check2:
        st.markdown("<h4 style='color: #d4af37;'>Após Operar:</h4>", unsafe_allow_html=True)
        
        check_pos1 = st.checkbox("Registrei a operação no diário de trades")
        check_pos2 = st.checkbox("Analisei erros e acertos com honestidade")
        check_pos3 = st.checkbox("Separei 10% do lucro para propósito maior (dízimo/caridade)")
        check_pos4 = st.checkbox("Agradeci pela oportunidade, lucro ou não")
        check_pos5 = st.checkbox("Não carreguei emocional para a próxima operação")
        
        if check_pos1 and check_pos2 and check_pos3 and check_pos4 and check_pos5:
            st.success("✅ FECHAMENTO CORRETO - Operador em Estado de Excelência")
    
    # Footer de poder
    st.markdown("""
    <div style='text-align: center; margin-top: 50px; padding: 30px; 
                background: linear-gradient(180deg, #000 0%, #0a0a0a 100%); 
                border: 2px solid #d4af37; border-radius: 20px;'>
        <h3 style='color: #d4af37; margin-bottom: 10px;'>SOLI DEO GLORIA</h3>
        <p style='font-size: 0.9rem; color: #666; margin: 0;'>
            A Glória pertence somente a Ele.<br>
            "Dele, por Ele e para Ele são todas as coisas" - Romanos 11:36
        </p>
    </div>
    """, unsafe_allow_html=True)

# =================================================================
# 12. MÓDULO: CONSELHO DE ELITE
# =================================================================

elif menu == "🤝 Conselho de Elite":
    st.title("🤝 Conselho de Elite & Diretrizes")
    
    st.markdown("""
    <div class='card-quantum'>
        Centro de comando estratégico. Antes de qualquer execução no mercado, 
        verifique se o seu alinhamento operacional cumpre os requisitos de Soberania.
    </div>
    """, unsafe_allow_html=True)
    
    # Checklist operacional
    st.subheader("📋 Protocolo de Pré-Abertura")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.checkbox("Devocional realizado e mente em estado de governo")
        st.checkbox("Análise de Volatilidade de Vórtice (Tesla) concluída")
        st.checkbox("Conferência de calendários econômicos (Payroll/FED/IPCA)")
    
    with c2:
        st.checkbox("Verificação de margens em ativos High-Ticket")
        st.checkbox("Monitoramento de fluxo institucional em Commodities")
        st.checkbox("Backups de segurança e conexão de terminal ativos")
    
    st.write("---")
    
    # As 7 Leis de Ferro
    st.subheader("📜 As 7 Leis de Ferro do Capital")
    
    leis = {
        "1. Preservação": "O primeiro objetivo não é ganhar, é não perder o lastro principal.",
        "2. Paciência": "O mercado é o mecanismo que transfere dinheiro dos impacientes para os pacientes.",
        "3. Confluência": "Nunca opere por impulso. Espere o cruzamento de pelo menos 3 indicadores.",
        "4. Escalabilidade": "Se o seu negócio não escala sem você, você tem um emprego, não um ativo.",
        "5. Diversificação Soberana": "Mantenha parte do lucro em ativos físicos fora do sistema bancário.",
        "6. High-Ticket": "Foque no topo da pirâmide. O esforço é o mesmo, o retorno é 100x maior.",
        "7. Transbordo": "A riqueza que para em você apodrece. O capital deve fluir para gerar legados."
    }
    
    for titulo, desc in leis.items():
        st.markdown(f"""
        <div class='trend-card'>
            <b style='color: #d4af37; font-size: 1.1rem;'>{titulo}</b><br>
            <span style='color: #ccc;'>{desc}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    
    # Painel de metas
    st.subheader("🚀 Planejamento de Expansão")
    
    col_e1, col_e2, col_e3 = st.columns(3)
    
    col_e1.metric("META E-COMMERCE PET", "R$ 50k/mês", "+12% vs anterior")
    col_e2.metric("YIELD CARTEIRA TRADE", "4.2% a.m", "Acima Benchmark")
    col_e3.metric("RESERVA SOBERANIA", "15% Patrimônio", "Em Ouro/BTC")
    
    # Rodapé do sistema
    st.markdown("""
    <div class='state-message' style='text-align: center; border-left: none; 
                                      border: 1px solid #d4af37; margin-top: 50px;'>
        <h3 style='color: #d4af37; margin-bottom: 5px;'>QUANTUM NEXUS ELITE PRO v5.0</h3>
        <p style='color: #666; font-size: 0.8rem;'>
            Desenvolvido para Gestão de Estado e Soberania Financeira.<br>
            Status: <b style='color: #00ff88;'>PROTEGIDO POR CRIPTOGRAFIA DE VÓRTICE</b><br>
            © 2026 - Todos os direitos reservados à soberania do usuário.
        </p>
    </div>
    """, unsafe_allow_html=True)
