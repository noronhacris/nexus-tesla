# Quantum Nexus Elite - v2.0
# Refatorado por um profissional para performance, estabilidade e clareza.

import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go
import time
from datetime import datetime

# =================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO (ALTA FIDELIDADE)
# =================================================================
# A configuração da página deve ser o primeiro comando do Streamlit.
st.set_page_config(
    page_title="Quantum Nexus Elite - Terminal de Estado",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização CSS otimizada e centralizada.
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=JetBrains+Mono:wght@400;700&display=swap' );
    
    body {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp { 
        background-color: #000000; 
        color: #FFFFFF; 
    }
    
    /* Sidebar Profissional com Gradiente de Borda Áurea */
    [data-testid="stSidebar"] { 
        background-color: #050505; 
        border-right: 2px solid #d4af37; 
        box-shadow: 10px 0px 30px rgba(212, 175, 55, 0.1);
    }
    
    /* Botão de Execução com Efeito de Brilho e Pulso */
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
# 2. NÚCLEO DE DADOS E VISUALIZAÇÃO (MOTORES OTIMIZADOS)
# =================================================================

# Otimização com cache: Evita baixar os mesmos dados repetidamente.
@st.cache_data(ttl=300) # Cache de 5 minutos
def fetch_market_data(ticker, period="90d", interval="1d"):
    """Busca dados de mercado de forma segura e eficiente."""
    try:
        data = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
        if data.empty:
            return None, f"Sinal de {ticker} não detectado ou ativo inválido."
        return data, None
    except Exception as e:
        return None, f"Erro de conexão ao buscar {ticker}: {e}"

def render_market_chart(ticker, nome_amigavel):
    """Renderiza o gráfico de mercado e as métricas em tempo real."""
    data, error = fetch_market_data(ticker)
    
    if error:
        st.error(f"⚠️ Erro de Sincronização: {error}")
        return

    # Adiciona a Média Móvel Simples (SMA) para mais insights
    data['SMA20'] = data['Close'].rolling(window=20).mean()

    fig = go.Figure()

    # Gráfico de Candlestick
    fig.add_trace(go.Candlestick(
        x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
        name='Candles',
        increasing_line_color='#d4af37', decreasing_line_color='#ff4b4b',
        increasing_fillcolor='rgba(212, 175, 55, 0.5)', decreasing_fillcolor='rgba(255, 75, 75, 0.5)'
    ))

    # Linha da Média Móvel
    fig.add_trace(go.Scatter(
        x=data.index, y=data['SMA20'],
        mode='lines', name='Média Móvel (20 dias)',
        line=dict(color='cyan', width=2)
    ))
    
    fig.update_layout(
        template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(10,10,10,0.5)', height=550,
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=50, b=10),
        title=dict(text=f"TERMINAL ANALÍTICO: {nome_amigavel.upper()}", font=dict(color='#d4af37', size=20)),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Container para o gráfico, para permitir atualização automática
    chart_placeholder = st.empty()
    chart_placeholder.plotly_chart(fig, use_container_width=True)
    
    # Containers para as métricas
    m1, m2, m3, m4 = st.columns(4)
    metric_placeholders = [m1.empty(), m2.empty(), m3.empty(), m4.empty()]

    # Loop para atualização "em tempo real"
    while True:
        live_data, _ = fetch_market_data(ticker, period="2d", interval="1m") # Busca dados do último minuto
        if live_data is not None and not live_data.empty:
            atual = live_data['Close'].iloc[-1]
            anterior = data['Close'].iloc[-2] # Compara com o fechamento do dia anterior
            delta_p = ((atual - anterior) / anterior) * 100
            
            metric_placeholders[0].metric("PREÇO ATUAL", f"{atual:.2f}")
            metric_placeholders[1].metric("VARIAÇÃO (vs D-1)", f"{delta_p:.2f}%", delta=f"{delta_p:.2f}%")
            metric_placeholders[2].metric("MÁXIMA (90D)", f"{data['High'].max():.2f}")
            metric_placeholders[3].metric("MÍNIMA (90D)", f"{data['Low'].min():.2f}")
        
        time.sleep(30) # Atualiza a cada 30 segundos

def logic_astrolabio_tesla(max_n, qtd, modalidade):
    """Gera números com base na lógica de Vórtice."""
    with st.status("🌀 Sincronizando Astrolábio Quântico...", expanded=True) as status:
        time.sleep(1.5) # Reduzido para melhor UX
        random.seed(datetime.now().microsecond) # Semente mais aleatória
        
        # Lógica de Vórtice (3-6-9)
        vortex_numbers = {n for n in range(1, max_n + 1) if n % 3 == 0}
        
        # Pool de números aleatórios para garantir variedade
        random_pool_size = int(max_n * 0.5)
        random_pool = set(random.sample(range(1, max_n + 1), random_pool_size))
        
        combined_pool = list(vortex_numbers.union(random_pool))
        
        # Garante que temos números suficientes para amostra
        if len(combined_pool) < qtd:
            combined_pool.extend(range(1, max_n + 1))
            
        principais = sorted(random.sample(combined_pool, qtd))
        
        status.update(label="Frequência Harmônica Estabelecida!", state="complete", expanded=False)
        
        if modalidade == "Milionária":
            trevos = sorted(random.sample(range(1, 7), 2))
            return principais, trevos
        
        return principais, None

# =================================================================
# 3. SIDEBAR - COMANDO CENTRAL DO OPERADOR
# =================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>⚡ NEXUS ELITE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d4af37;'>SISTEMA DE ESTADO v4.2</p>", unsafe_allow_html=True)
    st.write("---")
    
    # Dicionário para simplificar a gestão do menu
    menu_options = {
        "💎 IA Quântico Tesla": "ia_tesla",
        "🐾 Pet Global Intelligence": "pet_intel",
        "💹 Trade & Commodities": "trade",
        "👗 Fashion High-Ticket": "fashion",
        "🌍 Soberania & Reservas": "soberania",
        "🙏 Devocional de Poder": "devocional",
        "🤝 Conselho de Elite": "conselho"
    }
    
    menu_selecionado = st.radio(
        "COMANDOS DISPONÍVEIS:", 
        menu_options.keys()
    )
    
    st.write("---")
    st.markdown("**Status do Sistema:** <span style='color: #29B6F6;'>Operacional</span>", unsafe_allow_html=True)
    st.markdown("**Nível de Acesso:** <span style='color: #d4af37;'>Administrador Sênior</span>", unsafe_allow_html=True)
    
    # Placeholder para o relógio
    clock_placeholder = st.empty()
    while True:
        clock_placeholder.caption(f"Pulso Temporal: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        time.sleep(1)

# =================================================================
# 4. ROTEAMENTO E EXECUÇÃO DOS MÓDULOS
# =================================================================

# Mapeamento de ativos para evitar manipulação de strings e erros
ATIVOS = {
    "pet_intel": {
        "PETZ3.SA (Petz BR)": "PETZ3.SA",
        "ZTS (Zoetis)": "ZTS",
        "CHWY (Chewy)": "CHWY",
        "IDXX (IDEXX Labs)": "IDXX"
    },
    "trade": {
        "BTC-USD (Bitcoin)": "BTC-USD",
        "ETH-USD (Ethereum)": "ETH-USD",
        "USDBRL=X (Dólar)": "USDBRL=X",
        "EURBRL=X (Euro)": "EURBRL=X"
    },
    "fashion": {
        "MC.PA (LVMH)": "MC.PA",
        "RMS.PA (Hermès)": "RMS.PA",
        "NKE (Nike)": "NKE",
        "ARZZ3.SA (Arezzo)": "ARZZ3.SA"
    },
    "soberania": {
        "GC=F (Ouro)": "GC=F",
        "SI=F (Prata)": "SI=F",
        "BZ=F (Petróleo Brent)": "BZ=F",
        "VALE3.SA (Vale - Minério)": "VALE3.SA" # Corrigido para ticker válido
    }
}

# Bloco principal de execução
if menu_selecionado == "💎 IA Quântico Tesla":
    st.title("💎 IA Quântico Tesla & Astrolábio")
    st.markdown("<div class='card-quantum'>Algoritmo de análise universal baseado na Matemática de Vórtice (3-6-9) para decifrar padrões de confluência.</div>", unsafe_allow_html=True)
    
    jogo = st.selectbox("Selecione a Modalidade Operacional:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])

    if st.button("EXECUTAR CONFLUÊNCIA DE VÓRTICE"):
        configs = {"Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5), "Lotomania": (100, 50), "Milionária": (50, 6)}
        n_max, n_qtd = configs[jogo]
        nums, trevos = logic_astrolabio_tesla(n_max, n_qtd, jogo)
        
        st.markdown(f"<div class='card-quantum' style='text-align: center; border: 2px solid #d4af37;'><h3>NÚMEROS IDENTIFICADOS</h3><h1 style='font-size: 3.8rem; color: #FFF;'>{', '.join(map(str, nums))}</h1></div>", unsafe_allow_html=True)
        if trevos:
            st.markdown(f"<div style='text-align: center;'><h2>☘️ TREVOS DA SORTE: {trevos[0]} e {trevos[1]}</h2></div>", unsafe_allow_html=True)

elif menu_selecionado in ["🐾 Pet Global Intelligence", "💹 Trade & Commodities", "👗 Fashion High-Ticket", "🌍 Soberania & Reservas"]:
    
    # Títulos dinâmicos
    st.title(menu_selecionado)
    
    # Seleção de ativos baseada no menu
    key = menu_options[menu_selecionado]
    opcoes_ativos = ATIVOS[key]
    nome_amigavel_selecionado = st.selectbox("Selecione o Ativo:", opcoes_ativos.keys())
    
    # Busca o ticker correto no dicionário
    ticker_selecionado = opcoes_ativos[nome_amigavel_selecionado]
    
    # Renderiza o gráfico e as métricas
    render_market_chart(ticker_selecionado, nome_amigavel_selecionado)

elif menu_selecionado == "🙏 Devocional de Poder":
    st.title("🙏 Sabedoria, Propósito e Legado")
    st.markdown("<div class='card-quantum'><h2 style='text-align: center;'>O FUNDAMENTO DA VERDADEIRA RIQUEZA</h2><p align='center' style='font-size: 1.2rem; font-style: italic;'>'Minha é a prata, e meu é o ouro, diz o Senhor dos Exércitos...'</p><p style='text-align: justify; line-height: 1.8;'>A compreensão de que os recursos globais possuem um dono soberano redefine a forma como operamos. Não buscamos posse, mas sim uma gestão sábia e um domínio estratégico, alinhados a um propósito maior. A paciência, a sabedoria e a visão de longo prazo são os ativos mais valiosos neste terminal.</p></div>", unsafe_allow_html=True)

elif menu_selecionado == "🤝 Conselho de Elite":
    st.title("🤝 Conselho de Elite: Alianças e Blindagem")
    st.markdown("<div class='card-quantum'>Foco na expansão estratégica e na preservação de ativos. Defina as diretrizes para o próximo ciclo operacional.</div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Diretrizes Estratégicas")
        st.checkbox("Consolidação de Reservas de Ouro", value=True)
        st.checkbox("Expansão do Market Share (E-commerce Pet)")
        st.checkbox("Análise de Aquisição no Setor de Luxo")
    with c2:
        st.subheader("Notas do Conselho")
        st.info("A paciência é o ativo mais escasso do mercado.")
        st.warning("Monitorar volatilidade cambial (USD/BRL).")
        st.success("Posições em commodities estratégicas performando acima do esperado.")

