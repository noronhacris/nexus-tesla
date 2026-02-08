
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
    page_title="APP NORONHA - Terminal de Estado" 
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
            empresas líderes, oportunidades de investimento e insights para e-commerce especializa
