import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# =================================================================
# CONFIGURAÇÃO
# =================================================================
st.set_page_config(
    page_title="Quantum Nexus Elite Pro", 
    layout="wide", 
    initial_sidebar_state="collapsed"  # Sidebar desabilitada
)

# =================================================================
# SISTEMA DE NAVEGAÇÃO COM SESSION STATE
# =================================================================
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'
if 'subpagina' not in st.session_state:
    st.session_state.subpagina = None

def ir_para(destino, sub=None):
    st.session_state.pagina = destino
    st.session_state.subpagina = sub
    st.rerun()

def voltar():
    if st.session_state.subpagina:
        st.session_state.subpagina = None
    else:
        st.session_state.pagina = 'home'
    st.rerun()

# =================================================================
# CSS ESTILO APP BANCÁRIO MODERNO
# =================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

/* RESET E BASE */
* { margin: 0; padding: 0; box-sizing: border-box; }

.stApp { 
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    color: #FFFFFF; 
    font-family: 'Inter', sans-serif; 
}

/* ESCONDER ELEMENTOS STREAMLIT */
#MainMenu, footer, header, [data-testid="stSidebar"] { display: none !important; }
.stDeployButton { display: none !important; }

/* HEADER FIXO TIPO BANCO */
.header-banco {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: linear-gradient(135deg, #000 0%, #1a1a1a 100%);
    padding: 12px 20px;
    border-bottom: 2px solid #d4af37;
    z-index: 9999;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 20px rgba(212,175,55,0.4);
}

.header-logo {
    color: #d4af37;
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: 3px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.header-logo-icon {
    font-size: 1.5rem;
}

/* BOTÃO VOLTAR DESTAQUE */
.btn-voltar-container {
    position: fixed;
    top: 70px;
    left: 10px;
    z-index: 9998;
}

/* ESPAÇAMENTO PARA HEADER */
.container-principal {
    margin-top: 60px;
    padding: 15px;
    max-width: 1400px;
    margin-left: auto;
    margin-right: auto;
}

/* GRID DE CARDS TIPO BANCO */
.cards-bancarios {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    padding: 20px 0;
}

/* CARD INDIVIDUAL ESTILO BANCO */
.card-banco {
    background: linear-gradient(145deg, #1a1a1a, #0f0f0f);
    border: 1px solid #333;
    border-radius: 20px;
    padding: 30px 25px;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}

.card-banco::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, #d4af37, transparent, #d4af37);
    border-radius: 20px;
    opacity: 0;
    transition: opacity 0.3s;
    z-index: -1;
}

.card-banco:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 50px rgba(212,175,55,0.3);
    border-color: #d4af37;
}

.card-banco:hover::before {
    opacity: 0.3;
}

.card-banco:active {
    transform: translateY(-5px) scale(1.01);
}

.card-icon-grande {
    font-size: 3.5rem;
    margin-bottom: 15px;
    display: block;
    text-align: center;
    background: linear-gradient(135deg, #d4af37 0%, #f9e295 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.card-titulo {
    color: #d4af37;
    font-size: 1.4rem;
    font-weight: 700;
    margin: 15px 0 10px 0;
    text-align: center;
    letter-spacing: 1px;
}

.card-descricao {
    color: #999;
    font-size: 0.95rem;
    line-height: 1.6;
    text-align: center;
    margin: 10px 0;
    min-height: 48px;
}

.card-badge {
    display: inline-block;
    background: rgba(212,175,55,0.15);
    color: #d4af37;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    margin-top: 12px;
    border: 1px solid rgba(212,175,55,0.3);
}

/* TÍTULO DA PÁGINA */
.titulo-pagina {
    text-align: center;
    margin: 40px 0 20px 0;
}

.titulo-pagina h1 {
    color: #d4af37;
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 10px;
    text-shadow: 0 0 30px rgba(212,175,55,0.5);
}

.titulo-pagina p {
    color: #888;
    font-size: 1rem;
    margin-top: 10px;
}

/* BOTÕES STREAMLIT CUSTOMIZADOS */
.stButton > button {
    border-radius: 15px;
    border: 1px solid #d4af37;
    background: linear-gradient(135deg, #1a1a1a 0%, #000 100%);
    color: #d4af37 !important;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    width: 100%;
    height: 60px;
    transition: all 0.3s;
    font-size: 0.95rem;
}

.stButton > button:hover {
    transform: translateY(-3px);
    background: linear-gradient(135deg, #d4af37 0%, #f9e295 100%);
    color: #000 !important;
    box-shadow: 0 10px 30px rgba(212,175,55,0.5);
}

/* MÉTRICAS */
[data-testid="stMetricValue"] {
    color: #d4af37 !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}

[data-testid="stMetricDelta"] {
    font-size: 1rem !important;
}

/* CARDS DE CONTEÚDO */
.card-quantum {
    background: linear-gradient(145deg, #0f0f0f, #050505);
    border: 1px solid #222;
    border-radius: 20px;
    padding: 30px;
    margin: 20px 0;
    box-shadow: 10px 10px 30px rgba(0,0,0,0.5);
}

.trend-card {
    background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
    border: 1px solid #d4af37;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
}

.state-message {
    border-left: 5px solid #d4af37;
    padding: 25px;
    background: rgba(10, 10, 10, 0.8);
    line-height: 1.8;
    border-radius: 0 15px 15px 0;
    margin: 20px 0;
}

/* CORES SENTIMENT */
.sentiment-positive { color: #00ff88; font-weight: bold; }
.sentiment-neutral { color: #ffd700; font-weight: bold; }
.sentiment-negative { color: #ff4444; font-weight: bold; }

/* SCROLLBAR CUSTOMIZADA */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { 
    background: #d4af37; 
    border-radius: 10px; 
}
::-webkit-scrollbar-thumb:hover { background: #f9e295; }

/* ANIMAÇÕES */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.card-banco {
    animation: fadeInUp 0.5s ease-out backwards;
}

.card-banco:nth-child(1) { animation-delay: 0.05s; }
.card-banco:nth-child(2) { animation-delay: 0.1s; }
.card-banco:nth-child(3) { animation-delay: 0.15s; }
.card-banco:nth-child(4) { animation-delay: 0.2s; }
.card-banco:nth-child(5) { animation-delay: 0.25s; }
.card-banco:nth-child(6) { animation-delay: 0.3s; }
.card-banco:nth-child(7) { animation-delay: 0.35s; }
.card-banco:nth-child(8) { animation-delay: 0.4s; }

/* RESPONSIVO MOBILE */
@media (max-width: 768px) {
    .cards-bancarios {
        grid-template-columns: 1fr;
        gap: 15px;
        padding: 10px 0;
    }
    
    .card-banco {
        padding: 25px 20px;
    }
    
    .card-icon-grande {
        font-size: 3rem;
    }
    
    .card-titulo {
        font-size: 1.2rem;
    }
    
    .titulo-pagina h1 {
        font-size: 1.6rem;
    }
    
    .header-logo {
        font-size: 1rem;
    }
    
    .container-principal {
        padding: 10px;
    }
}

/* TABELAS */
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
# FUNÇÕES PRESERVADAS DO CÓDIGO ORIGINAL
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

def calcular_bollinger_bands(data, periodo=20):
    sma = data['Close'].rolling(window=periodo).mean()
    std = data['Close'].rolling(window=periodo).std()
    return sma, sma + (std * 2), sma - (std * 2)

def analisar_tendencia(data):
    rsi = calcular_rsi(data).iloc[-1]
    macd, signal, _ = calcular_macd(data)
    preco_atual = data['Close'].iloc[-1]
    sma_20 = data['Close'].rolling(window=20).mean().iloc[-1]
    sma_50 = data['Close'].rolling(window=50).mean().iloc[-1]
    
    sinais_alta = 0
    sinais_baixa = 0
    
    if rsi < 30: sinais_alta += 1
    elif rsi > 70: sinais_baixa += 1
    if macd.iloc[-1] > signal.iloc[-1]: sinais_alta += 1
    else: sinais_baixa += 1
    if preco_atual > sma_20 > sma_50: sinais_alta += 1
    elif preco_atual < sma_20 < sma_50: sinais_baixa += 1
    
    if sinais_alta > sinais_baixa:
        tendencia, forca = "ALTA", sinais_alta * 33.3
    elif sinais_baixa > sinais_alta:
        tendencia, forca = "BAIXA", sinais_baixa * 33.3
    else:
        tendencia, forca = "NEUTRA", 50
    
    return {
        'tendencia': tendencia, 'forca': forca, 'rsi': rsi,
        'macd': macd.iloc[-1], 'signal': signal.iloc[-1],
        'preco': preco_atual, 'sma_20': sma_20, 'sma_50': sma_50
    }

def render_analise_tecnica_avancada(ticker, nome):
    try:
        data = yf.download(ticker, period="180d", progress=False, auto_adjust=True)
        if data.empty:
            st.error(f"Dados não disponíveis para {nome}")
            return
        
        data['RSI'] = calcular_rsi(data)
        macd, signal, _ = calcular_macd(data)
        data['MACD'], data['Signal'] = macd, signal
        sma, upper_bb, lower_bb = calcular_bollinger_bands(data)
        data['SMA_20'], data['BB_Upper'], data['BB_Lower'] = sma, upper_bb, lower_bb
        
        analise = analisar_tendencia(data)
        
        fig = make_subplots(
            rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05,
            row_heights=[0.5, 0.25, 0.25],
            subplot_titles=('Preço & Bollinger Bands', 'RSI', 'MACD')
        )
        
        fig.add_trace(go.Candlestick(
            x=data.index, open=data['Open'], high=data['High'],
            low=data['Low'], close=data['Close'],
            increasing_line_color='#d4af37', decreasing_line_color='#ff4b4b',
            name="Preço"), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['SMA_20'],
            line=dict(color='#00ff88', width=1.5), name='SMA 20'), row=1, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['RSI'],
            line=dict(color='#d4af37', width=2), name='RSI'), row=2, col=1)
        
        fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['MACD'],
            line=dict(color='#00ff88', width=2), name='MACD'), row=3, col=1)
        
        fig.add_trace(go.Scatter(
            x=data.index, y=data['Signal'],
            line=dict(color='#ff4444', width=2), name='Signal'), row=3, col=1)
        
        fig.update_layout(
            template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)', height=800, showlegend=True,
            xaxis_rangeslider_visible=False,
            title=dict(text=f"📊 {nome.upper()}", font=dict(color='#d4af37', size=20))
        )
        
        fig.update_xaxes(showgrid=False, color='#444')
        fig.update_yaxes(showgrid=True, gridcolor='#222', color='#444')
        
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        atual = data['Close'].iloc[-1]
        anterior = data['Close'].iloc[-2]
        delta_perc = ((atual / anterior) - 1) * 100
        
        cor_tendencia = "🟢" if analise['tendencia'] == "ALTA" else "🔴" if analise['tendencia'] == "BAIXA" else "🟡"
        
        col1.metric("PREÇO", f"${atual:.2f}", f"{delta_perc:+.2f}%")
        col2.metric("RSI", f"{analise['rsi']:.1f}")
        col3.metric("TENDÊNCIA", f"{cor_tendencia} {analise['tendencia']}")
        col4.metric("VOLUME", f"{data['Volume'].iloc[-1]/1e6:.1f}M")
        col5.metric("VOLATILIDADE", f"{data['Close'].pct_change().std()*100:.2f}%")
        
    except Exception as e:
        st.error(f"Erro: {str(e)}")

def logic_astrolabio_tesla(max_n, qtd, modalidade):
    def reduzir(numero):
        while numero > 9:
            numero = sum(int(d) for d in str(numero))
        return numero
    
    random.seed(int(time.time() * 1000) % 10000)
    candidatos = list(range(1, max_n + 1))
    vortex = [n for n in candidatos if reduzir(n) in [3, 6, 9]]
    comuns = [n for n in candidatos if n not in vortex]
    
    qtd_vortex = int(qtd * 0.4)
    selecao = random.sample(vortex, min(qtd_vortex, len(vortex)))
    selecao += random.sample(comuns, qtd - len(selecao))
    
    while len(selecao) < qtd:
        novo = random.choice(candidatos)
        if novo not in selecao:
            selecao.append(novo)
    
    trevos = sorted(random.sample(range(1, 7), 2)) if modalidade == "Milionária" else []
    return sorted(selecao[:qtd]), trevos

# =================================================================
# HEADER FIXO
# =================================================================
titulo_header = {
    'home': '⚡ NEXUS ELITE PRO',
    'dashboard': '🎯 Dashboard',
    'ia_tesla': '💎 IA Tesla',
    'pet': '🐾 Pet Market',
    'trade': '💹 Trading',
    'fashion': '👗 Fashion',
    'soberania': '🌍 Soberania',
    'devocional': '🙏 Devocional',
    'conselho': '🤝 Conselho'
}.get(st.session_state.pagina, '⚡ NEXUS ELITE PRO')

st.markdown(f"""
<div class='header-banco'>
    <div class='header-logo'>
        <span class='header-logo-icon'>⚡</span>
        <span>{titulo_header}</span>
    </div>
    <div style='color: #888; font-size: 0.85rem;'>{datetime.now().strftime('%H:%M')}</div>
</div>
""", unsafe_allow_html=True)

# BOTÃO VOLTAR (SEMPRE VISÍVEL QUANDO NÃO ESTÁ NA HOME)
if st.session_state.pagina != 'home':
    col_btn_voltar, _ = st.columns([1, 5])
    with col_btn_voltar:
        if st.button("← VOLTAR", key="btn_voltar_main", use_container_width=True):
            voltar()

st.markdown("<div class='container-principal'>", unsafe_allow_html=True)

# =================================================================
# TELA HOME - MENU PRINCIPAL
# =================================================================

if st.session_state.pagina == 'home':
    
    st.markdown("""
    <div class='titulo-pagina'>
        <h1>SISTEMA DE GESTÃO ELITE</h1>
        <p>Selecione um módulo para começar</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Definir cards
    cards_menu = [
        {'icon': '🎯', 'titulo': 'Dashboard', 'desc': 'Visão executiva de mercados globais', 'badge': 'Tempo Real', 'dest': 'dashboard'},
        {'icon': '💎', 'titulo': 'IA Quântico', 'desc': 'Algoritmo Tesla para jogos', 'badge': 'Vórtice 3-6-9', 'dest': 'ia_tesla'},
        {'icon': '🐾', 'titulo': 'Pet Market', 'desc': 'Inteligência do mercado pet', 'badge': 'R$ 66 Bi', 'dest': 'pet'},
        {'icon': '💹', 'titulo': 'Trading', 'desc': 'Análise técnica profissional', 'badge': 'RSI + MACD', 'dest': 'trade'},
        {'icon': '👗', 'titulo': 'Fashion Luxo', 'desc': 'Marcas de alto valor global', 'badge': 'Top 20', 'dest': 'fashion'},
        {'icon': '🌍', 'titulo': 'Soberania', 'desc': 'Agro, minerais e reservas', 'badge': 'Estratégico', 'dest': 'soberania'},
        {'icon': '🙏', 'titulo': 'Devocional', 'desc': 'Alinhamento espiritual', 'badge': 'Propósito', 'dest': 'devocional'},
        {'icon': '🤝', 'titulo': 'Conselho', 'desc': 'Diretrizes e protocolos', 'badge': '7 Leis', 'dest': 'conselho'},
    ]
    
    # Renderizar grid de cards
    col1, col2 = st.columns(2)
    
    for i, card in enumerate(cards_menu):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            if st.button(f"{card['icon']} {card['titulo']}", key=f"btn_card_{card['dest']}", use_container_width=True):
                ir_para(card['dest'])
            
            st.markdown(f"""
            <div style='text-align: center; margin-top: -15px; margin-bottom: 20px;'>
                <p style='color: #888; font-size: 0.9rem; margin-bottom: 5px;'>{card['desc']}</p>
                <span style='display: inline-block; background: rgba(212,175,55,0.15); 
                             color: #d4af37; padding: 4px 12px; border-radius: 15px; 
                             font-size: 0.75rem; font-weight: 700; 
                             border: 1px solid rgba(212,175,55,0.3);'>
                    ● {card['badge']}
                </span>
            </div>
            """, unsafe_allow_html=True)

# =================================================================
# PÁGINAS INTERNAS (COM TODO CONTEÚDO PRESERVADO)
# =================================================================

elif st.session_state.pagina == 'dashboard':
    st.markdown("<div class='card-quantum'>", unsafe_allow_html=True)
    st.subheader("📊 Indicadores Principais")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    try:
        tickers = {
            "GC=F": ("Ouro", col1),
            "^GSPC": ("S&P 500", col2),
            "BTC-USD": ("Bitcoin", col3),
            "VALE3.SA": ("Vale", col4),
            "^BVSP": ("Ibovespa", col5)
        }
        
        for ticker, (nome, coluna) in tickers.items():
            try:
                data = yf.Ticker(ticker).history(period="2d")
                if not data.empty and len(data) >= 2:
                    atual = data['Close'].iloc[-1]
                    var = ((atual / data['Close'].iloc[-2]) - 1) * 100
                    coluna.metric(nome, f"${atual:,.0f}", f"{var:+.2f}%")
            except:
                continue
    except:
        st.info("Carregando...")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Ranking
    st.markdown("<div class='card-quantum'>", unsafe_allow_html=True)
    st.subheader("🏆 Top Performers 7 Dias")
    
    try:
        ativos = {"AAPL": "Apple", "GOOGL": "Google", "MSFT": "Microsoft", 
                  "VALE3.SA": "Vale", "GC=F": "Ouro", "BTC-USD": "Bitcoin"}
        perf = []
        
        for ticker, nome in ativos.items():
            try:
                data = yf.download(ticker, period="7d", progress=False)
                if not data.empty and len(data) >= 2:
                    ret = ((data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1) * 100
                    perf.append({'Ativo': nome, 'Retorno 7D': f"{ret:+.2f}%"})
            except:
                continue
        
        if perf:
            df = pd.DataFrame(perf).sort_values('Retorno 7D', ascending=False)
            st.dataframe(df, use_container_width=True, hide_index=True)
    except:
        st.info("Carregando ranking...")
    
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.pagina == 'ia_tesla':
    st.markdown("<div class='card-quantum'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        jogo = st.selectbox("Modalidade:", 
            ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    with col2:
        freq = st.select_slider("Freq (Hz):", [369, 432, 528, 963])
    with col3:
        num_jogos = st.number_input("Jogos:", 1, 10, 1)
    
    if st.button("⚡ GERAR NÚMEROS"):
        configs = {
            "Mega-Sena": (60, 6), "Lotofácil": (25, 15), 
            "Quina": (80, 5), "Lotomania": (100, 50), "Milionária": (50, 6)
        }
        n_max, n_qtd = configs[jogo]
        
        for i in range(num_jogos):
            nums, trevos = logic_astrolabio_tesla(n_max, n_qtd, jogo)
            
            st.markdown(f"""
            <div class='trend-card' style='text-align: center; border: 2px solid #d4af37;'>
                <h4 style='color: #888; margin-bottom: 15px;'>JOGO #{i+1}</h4>
                <h1 style='font-size: 2.5rem; color: #FFF; letter-spacing: 3px;'>
                    {', '.join(map(str, nums))}
                </h1>
                {f"<p style='color: #d4af37; margin-top: 15px;'>☘️ Trevos: {trevos[0]}, {trevos[1]}</p>" if trevos else ""}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.pagina == 'pet':
    st.markdown("<div class='card-quantum'>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mercado Global", "US$ 261 Bi", "+8.5%")
    col2.metric("Brasil", "R$ 66 Bi", "+12%")
    col3.metric("Pets BR", "162 Mi", "1º AL")
    col4.metric("CAGR", "9.2%", "2024-30")
    
    st.write("---")
    st.subheader("💰 Oportunidades E-commerce")
    
    oportunidades = [
        ("🥩 Alimentação Premium", "Margem 40-60%, Ticket R$ 200-400/mês", "MUITO ALTO"),
        ("💊 Nutraceuticals", "Margem 50-70%, Crescimento 25% a.a.", "ALTO"),
        ("🎁 Assinatura", "LTV alto, baixo CAC após setup", "ALTO"),
        ("🏥 Telemedicina", "Modelo SaaS escalável", "MÉDIO-ALTO"),
    ]
    
    for titulo, desc, pot in oportunidades:
        st.markdown(f"""
        <div class='trend-card'>
            <h4 style='color: #d4af37;'>{titulo}</h4>
            <p style='color: #ccc;'>{desc}</p>
            <p><b>Potencial:</b> <span class='sentiment-positive'>{pot}</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.pagina == 'trade':
    st.markdown("<div class='card-quantum'>", unsafe_allow_html=True)
    
    ativo = st.selectbox("Selecione o Ativo:", [
        "GC=F (Ouro)", "SI=F (Prata)", "BTC-USD (Bitcoin)", 
        "VALE3.SA (Vale)", "PETR4.SA (Petrobras)"
    ])
    
    ticker = ativo.split(" (")[0]
    render_analise_tecnica_avancada(ticker, ativo)
    
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.pagina == 'fashion':
    st.markdown("<div class='card-quantum'>", unsafe_allow_html=True)
    st.subheader("👑 Top 10 Marcas de Luxo")
    
    marcas = ['Louis Vuitton', 'Hermès', 'Gucci', 'Chanel', 'Dior', 
              'Cartier', 'Rolex', 'Prada', 'Burberry', 'Fendi']
    valores = [124.8, 110.5, 89.2, 78.1, 71.4, 65.3, 61.2, 52.8, 48.6, 42.1]
    
    fig = go.Figure(go.Bar(
        x=valores, y=marcas, orientation='h', marker_color='#d4af37',
        text=[f'${v}B' for v in valores], textposition='outside'
    ))
    
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        height=500, title="Valor de Marca 2024 (US$ Bilhões)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Mercado Global", "€ 362 Bi", "+8%")
    col2.metric("E-commerce", "23%", "+5pp")
    col3.metric("Margem Média", "28%", "Hermès: 42%")
    
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.pagina == 'soberania':
    st.markdown("<div class='card-quantum'>", unsafe_allow_html=True)
    st.subheader("🥇 Análise do Ouro")
    
    render_analise_tecnica_avancada("GC=F", "Ouro Futuro")
    
    st.write("---")
    st.subheader("🌎 Top 5 Reservas de Ouro")
    
    paises = ['EUA', 'Alemanha', 'Itália', 'França', 'Rússia']
    tons = [8133, 3352, 2452, 2437, 2332]
    
    fig = go.Figure(go.Bar(
        x=paises, y=tons, marker_color='#d4af37',
        text=[f'{t}t' for t in tons], textposition='outside'
    ))
    
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)',
        height=350, title="Reservas Oficiais (Toneladas)"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.pagina == 'devocional':
    st.markdown("<div class='card-quantum'>", unsafe_allow_html=True)
    
    st.markdown("""
    <h3 style='color: #d4af37; text-align: center;'>📖 Provérbios 3:5-6</h3>
    <p style='font-size: 1.1rem; font-style: italic; text-align: center; padding: 20px;'>
        "Confia no Senhor de todo o teu coração e não te estribes no teu próprio entendimento. 
        Reconhece-o em todos os teus caminhos, e ele endireitará as tuas veredas."
    </p>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.subheader("✅ Checkpoint")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Antes de Operar:**")
        st.checkbox("Orei e busquei direção")
        st.checkbox("Estou equilibrado emocionalmente")
        st.checkbox("Tenho stop-loss definido")
    
    with col2:
        st.markdown("**Após Operar:**")
        st.checkbox("Registrei no diário")
        st.checkbox("Analisei erros/acertos")
        st.checkbox("Separei 10% para propósito maior")
    
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.pagina == 'conselho':
    st.markdown("<div class='card-quantum'>", unsafe_allow_html=True)
    st.subheader("📜 As 7 Leis de Ferro")
    
    leis = [
        ("1. Preservação", "Não perder o lastro principal"),
        ("2. Paciência", "Dinheiro dos impacientes para pacientes"),
        ("3. Confluência", "3+ indicadores confirmarem"),
        ("4. Escalabilidade", "Escala sem você = ativo"),
        ("5. Diversificação", "Parte em ativos físicos"),
        ("6. High-Ticket", "Topo da pirâmide"),
        ("7. Transbordo", "Capital flui para legados")
    ]
    
    for titulo, desc in leis:
        st.markdown(f"""
        <div class='trend-card'>
            <b style='color: #d4af37;'>{titulo}:</b> {desc}
        </div>
        """, unsafe_allow_html=True)
    
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Meta E-commerce", "R$ 50k/mês", "+12%")
    col2.metric("Yield Trade", "4.2% a.m", "Acima")
    col3.metric("Reserva", "15%", "Ouro/BTC")
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
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
