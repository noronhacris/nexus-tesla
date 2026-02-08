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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=JetBrains+Mono:wght@400;700&display=swap' );
    
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

    /* Escondendo Elementos Desnecessários do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar de Luxo */
    ::-webkit-scrollbar { width: 10px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #d4af37; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 3. MOTORES ANALÍTICOS (NÚCLEO DE DADOS)
# =================================================================

def render_corretora_chart(ticker, nome):
    """
    Motor de Renderização de Alta Fidelidade.
    Extrai dados reais da Bolsa e projeta em interface de Corretora.
    """
    try:
        data = yf.download(ticker, period="90d", interval="1d", progress=False, auto_adjust=True)
        
        if data.empty:
            st.error(f"⚠️ FALHA NA SINCRONIZAÇÃO: O ativo {nome} está fora de alcance no momento.")
            return

        fig = go.Figure(data=[go.Candlestick(
            x=data.index, 
            open=data['Open'], 
            high=data['High'], 
            low=data['Low'], 
            close=data['Close'],
            increasing_line_color='#d4af37',
            decreasing_line_color='#ff4b4b',
            increasing_fillcolor='#d4af37', 
            decreasing_fillcolor='#ff4b4b',
            name="Preço de Mercado"
        )])
        
        fig.update_layout(
            template='plotly_dark', 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            height=580,
            xaxis_rangeslider_visible=False,
            margin=dict(l=0, r=0, t=40, b=0),
            title=dict(
                text=f"TERMINAL ANALÍTICO: {nome.upper()}", 
                font=dict(color='#d4af37', size=22, family='JetBrains Mono')
            ),
            xaxis=dict(showgrid=False, color='#444'),
            yaxis=dict(showgrid=True, gridcolor='#222', color='#444', side='right')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        m1, m2, m3, m4 = st.columns(4)
        atual = data['Close'].iloc[-1]
        anterior = data['Close'].iloc[-2]
        delta_abs = atual - anterior
        delta_perc = (delta_abs / anterior) * 100
        
        m1.metric("PREÇO ATUAL", f"{atual:.2f}")
        m2.metric("VARIAÇÃO DIA", f"{delta_perc:.2f}%", delta=f"{delta_abs:.2f}")
        m3.metric("MÁXIMA 90D", f"{data['High'].max():.2f}")
        m4.metric("MÍNIMA 90D", f"{data['Low'].min():.2f}")
        
    except Exception as e:
        st.warning(f"🔄 Conexão instável com o servidor de dados para {nome}. Tentando reconectar...")

def logic_astrolabio_tesla(max_n, qtd, modalidade):
    """
    Algoritmo baseado na Matemática de Vórtice de Nikola Tesla.
    Foca nas confluências de 3, 6 e 9 para filtragem de probabilidade.
    """
    with st.status("🌀 SINCRO-VÓRTICE ATIVO: ANALISANDO FREQUÊNCIAS...", expanded=True) as status:
        time.sleep(2.5)
        random.seed(int(time.time() * 1000))
        
        vortex_base = [n for n in range(1, max_n + 1) if (n % 3 == 0 or n % 6 == 0 or n % 9 == 0)]
        full_pool = list(set(vortex_base + random.sample(range(1, max_n + 1), int(max_n * 0.4))))
        selecionados = sorted(random.sample(full_pool, qtd))
        
        if modalidade == "Milionária":
            trevos = sorted(random.sample(range(1, 7), 2))
            status.update(label="VÓRTICE ESTABILIZADO: TREVOS IDENTIFICADOS!", state="complete")
            return selecionados, trevos
        
        status.update(label="CONFLUÊNCIA ESTABELECIDA COM SUCESSO!", state="complete")
        return selecionados, None

# =================================================================
# 4. SIDEBAR - PAINEL DE COMANDO CENTRAL (NAVEGAÇÃO)
# =================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>⚡ NEXUS ELITE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d4af37;'>SISTEMA DE ESTADO v4.1</p>", unsafe_allow_html=True)
    st.write("---")
    
    menu = st.radio(
        "COMANDOS DISPONÍVEIS:", 
        [
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
    st.markdown("**Status:** Operacional")
    st.markdown("**Nível:** Administrator")
    st.caption(f"Tempo de Execução: {datetime.now().strftime('%H:%M:%S')}")

# =================================================================
# 5. ROTEAMENTO E EXECUÇÃO DOS MÓDULOS
# =================================================================

if menu == "💎 IA Quântico Tesla":
    st.title("💎 IA Quântico Tesla & Astrolábio")
    st.markdown("""
        <div class='card-quantum'>
            Este módulo utiliza a Matemática de Vórtice para identificar padrões de confluência 
            em jogos de alta volatilidade. A análise foca no equilíbrio geométrico dos números.
        </div>
    """, unsafe_allow_html=True)
    
    col_j1, col_j2 = st.columns([2, 1])
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

    if st.button("EXECUTAR CONFLUÊNCIA DE VÓRTICE"):
        configs = {
            "Mega-Sena": (60, 6), 
            "Lotofácil": (25, 15), 
            "Quina": (80, 5), 
            "Lotomania": (100, 50), 
            "Milionária": (50, 6)
        }
        
        n_max, n_qtd = configs[jogo]
        nums, trevos = logic_astrolabio_tesla(n_max, n_qtd, jogo)
        
        st.markdown(f"""
            <div class='card-quantum' style='text-align: center; border: 2px solid #d4af37;'>
                <h3 style='color: #888; letter-spacing: 5px;'>NÚMEROS IDENTIFICADOS</h3>
                <h1 style='font-size: 3.8rem; color: #FFF; text-shadow: 0 0 20px rgba(212,175,55,0.5);'>
                    {', '.join(map(str, nums))}
                </h1>
            </div>
        """, unsafe_allow_html=True)
        
        if jogo == "Milionária" and trevos:
            st.markdown(f"""
                <div style='text-align: center; margin-top: -15px;'>
                    <h2 style='color: #d4af37; font-family: "JetBrains Mono";'>
                        ☘️ TREVOS DA SORTE: 
                        <span style='color:#FFF; border: 1px solid #d4af37; padding: 5px 15px; border-radius: 10px;'>{trevos[0]}</span> 
                        e 
                        <span style='color:#FFF; border: 1px solid #d4af37; padding: 5px 15px; border-radius: 10px;'>{trevos[1]}</span>
                    </h2>
                    <p style='color: #666;'>Sincronização Milionária Ativa em {esfera}Hz</p>
                </div>
            """, unsafe_allow_html=True)

# [INÍCIO DA CORREÇÃO] - Removido o bloco duplicado e restaurado o fluxo correto

elif menu == "🐾 Pet Global Intelligence":
    # Este bloco não estava no seu código original, mas estou adicionando para garantir que funcione.
    st.title("🐾 Pet Global Intelligence")
    st.info("Módulo em desenvolvimento.")

elif menu == "💹 Trade & Commodities":
    st.title("💹 Terminal de Trading Profissional")
    st.markdown("""
        <div class='card-quantum'>
            Monitoramento de ativos de alta liquidez e reserva de valor. 
            Este terminal integra dados de corretoras globais para análise de suportes, 
            resistências e fluxo institucional em Criptoativos e Forex.
        </div>
    """, unsafe_allow_html=True)
    
    t_ativo = st.selectbox(
        "Selecione o Ativo para Análise de Fluxo:", 
        [
            "BTC-USD (Bitcoin - Ouro Digital)", 
            "ETH-USD (Ethereum - Contratos Inteligentes)", 
            "USDBRL=X (Dólar Comercial - Paridade BR)", 
            "EURBRL=X (Euro - Paridade BR)",
            "GC=F (Ouro Futuros - Hedge)"
        ]
    )
    
    ticker_trade = t_ativo.split(" (")[0] # Corrigido para extrair o ticker corretamente
    render_corretora_chart(ticker_trade, t_ativo)
    
    st.write("---")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("""
            <div style='background: #0a0a0a; padding: 25px; border-radius: 20px; border: 1px solid #d4af37;'>
                <h4 style='color: #d4af37; margin-top:0;'>🧠 INSIGHT IA: FLUXO INSTITUCIONAL</h4>
                <p style='color: #ccc; font-size: 0.95rem;'>
                    O algoritmo identifica forte acumulação em zonas de suporte histórico. 
                    Recomenda-se atenção ao <b>Volume Profile</b>. No mercado de Commodities, 
                    o Ouro (GC=F) apresenta correlação inversa com o apetite ao risco do S&P500.
                </p>
                <code style='color: #f9e295;'>STATUS: AGUARDANDO GATILHO DE VOLUMETRIA</code>
            </div>
        """, unsafe_allow_html=True)

    with col_t2:
        st.subheader("📊 Volatilidade Comparada")
        labels_v = ['Bitcoin', 'Ethereum', 'Dólar', 'Ouro']
        values_v = [65, 78, 12, 8]
        
        fig_vol = go.Figure(data=[go.Bar(
            x=labels_v, y=values_v,
            marker_color=['#d4af37', '#888', '#555', '#222'],
            text=values_v, textposition='auto'
        )])
        fig_vol.update_layout(
            template='plotly_dark', 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            height=250,
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig_vol, use_container_width=True)
        st.caption("Índice de Volatilidade Relativa (Anualizado %)")

    st.markdown("""
        <div class='state-message'>
            <b>REGRA DE OURO:</b> O lucro é feito na compra, não na venda. Opere apenas em zonas 
            de confluência onde o risco é matematicamente inferior ao potencial de retorno.
        </div>
    """, unsafe_allow_html=True)

elif menu == "👗 Fashion High-Ticket":
    st.title("👗 Radar Fashion Luxo & Market Share")
    st.markdown("""
        <div class='card-quantum'>
            Análise das detentoras das marcas mais valiosas do mundo. O mercado High-Ticket opera 
            com margens de lucro imunes a crises fiduciárias, focando em exclusividade e valor de marca.
        </div>
    """, unsafe_allow_html=True)
    
    f_marca = st.selectbox(
        "Selecione o Ativo High-Ticket para Análise de Gráfico:", 
        ["MC.PA (LVMH - Louis Vuitton)", "RMS.PA (Hermès)", "KER.PA (Kering/Gucci)", "ARZZ3.SA (Arezzo Brasil)", "SOMA3.SA (Grupo Soma)"]
    )
    ticker_f = f_marca.split(" (")[0] # Corrigido para extrair o ticker corretamente
    render_corretora_chart(ticker_f, f_marca)
    
    st.write("---")
    
    st.subheader("🏛️ TOP 10 CONGLOMERADOS DE LUXO MUNDIAIS")
    col_fi1, col_fi2 = st.columns([3, 2])
    
    marcas_int = ['LVMH', 'Hermès', 'Dior', 'Chanel', 'Richemont', 'Kering', 'Estée Lauder', 'Rolex', 'Prada', 'Burberry']
    val_int = [420, 210, 150, 110, 85, 70, 65, 50, 45, 30]
    
    with col_fi1:
        fig_bar_fi = go.Figure(data=[go.Bar(
            x=marcas_int, y=val_int,
            marker_color='#d4af37',
            text=[f"${v}B" for v in val_int], textposition='outside'
        )])
        fig_bar_fi.update_layout(title="Valuation Estimado (Bilhões USD)", template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar_fi, use_container_width=True)
        
    with col_fi2:
        fig_pie_fi = go.Figure(data=[go.Pie(labels=marcas_int, values=val_int, hole=.4)])
        fig_pie_fi.update_layout(title="% Ocupação do Mercado Global de Luxo", template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie_fi, use_container_width=True)

    st.write("---")

    st.subheader("🇧🇷 TOP 10 PLAYERS FASHION & VAREJO (BRASIL)")
    col_fn1, col_fn2 = st.columns([3, 2])
    
    marcas_br = ['Arezzo&Co', 'Grupo Soma', 'Lojas Renner', 'C&A Brasil', 'Riachuelo', 'Vivara', 'Hering', 'Alpargatas', 'Track&Field', 'Grendene']
    val_br = [7.5, 6.8, 15.2, 2.1, 2.5, 8.4, 4.2, 5.1, 1.8, 6.3]
    
    with col_fn1:
        fig_bar_fn = go.Figure(data=[go.Bar(
            x=marcas_br, y=val_br,
            marker_color='#888',
            text=[f"R${v}B" for v in val_br], textposition='outside'
        )])
        fig_bar_fn.update_layout(title="Market Cap B3 (Bilhões R$)", template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar_fn, use_container_width=True)
        
    with col_fn2:
        fig_pie_fn = go.Figure(data=[go.Pie(
            labels=marcas_br, values=val_br, hole=.4,
            marker=dict(colors=['#d4af37', '#b8922a', '#9c791d', '#816111', '#6b541a', '#524013', '#392c0d', '#282828', '#1a1a1a', '#000'])
        )])
        fig_pie_fn.update_layout(title="% Ocupação no Varejo Listado BR", template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie_fn, use_container_width=True)

    st.markdown("""
        <div class='state-message'>
            <b>INSIGHT DE GESTÃO:</b> No mercado de luxo internacional, o foco é a preservação de margem e exclusividade. 
            No cenário nacional, estamos vivenciando uma fase de consolidação (M&A), como a fusão entre Arezzo e Soma, 
            criando gigantes que buscam escala para competir globalmente.
        </div>
    """, unsafe_allow_html=True)

elif menu == "🌍 Soberania & Reservas":
    st.title("🌍 Soberania Nacional e Reservas Mundiais")
    st.markdown("""
        <div class='card-quantum'>
            Monitoramento de ativos que compõem o lastro de segurança das nações. 
            A soberania é exercida através do domínio sobre recursos naturais e metais preciosos.
        </div>
    """, unsafe_allow_html=True)
    
    reserva_sel = st.selectbox(
        "Selecione o Ativo Estratégico para Análise Técnica:", 
        ["GC=F (Ouro Futuros)", "SI=F (Prata)", "BZ=F (Petróleo Brent)", "VALE3.SA (Vale Brasil - Nióbio/Ferro)"]
    )
    ticker_r = reserva_sel.split(" (")[0] # Corrigido para extrair o ticker corretamente
    render_corretora_chart(ticker_r, reserva_sel)
    
    st.write("---")
    
    st.subheader("🏛️ TOP 10 RESERVAS DE OURO MUNDIAIS (TONELADAS)")
    col_int1, col_int2 = st.columns([3, 2])
    
    paises_int = ['EUA', 'Alemanha', 'FMI', 'Itália', 'França', 'Rússia', 'China', 'Suíça', 'Japão', 'Índia']
    toneladas_int = [8133, 3355, 2814, 2451, 2436, 2332, 2191, 1040, 846, 800]
    
    with col_int1:
        fig_bar_int = go.Figure(data=[go.Bar(
            x=paises_int, y=toneladas_int,
            marker_color='#d4af37',
            text=toneladas_int, textposition='outside'
        )])
        fig_bar_int.update_layout(
            title="Reservas Oficiais (Toneladas Físicas)", 
            template='plotly_dark', 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_bar_int, use_container_width=True)
        
    with col_int2:
        fig_pie_int = go.Figure(data=[go.Pie(labels=paises_int, values=toneladas_int, hole=.4)])
        fig_pie_int.update_layout(title="% Ocupação no Top 10", template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie_int, use_container_width=True)

    st.write("---")

    st.subheader("🇧🇷 TOP 10 ATIVOS DE SOBERANIA NACIONAL (BRASIL)")
    col_br1, col_br2 = st.columns([3, 2])
    
    ativos_br = ['VALE3', 'PETR4', 'ELET3', 'CSNA3', 'GGBR4', 'VBBR3', 'CMIG4', 'CPFE3', 'SUZB3', 'KLBN11']
    market_cap_br = [310, 420, 95, 25, 38, 22, 28, 40, 65, 24]
    
    with col_br1:
        fig_bar_br = go.Figure(data=[go.Bar(
            x=ativos_br, y=market_cap_br,
            marker_color='#888',
            text=[f"R${v}B" for v in market_cap_br], textposition='outside'
        )])
        fig_bar_br.update_layout(
            title="Capitalização Estratégica (Bilhões BRL)", 
            template='plotly_dark', 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_bar_br, use_container_width=True)
        
    with col_br2:
        fig_pie_br = go.Figure(data=[go.Pie(
            labels=ativos_br, values=market_cap_br, hole=.4,
            marker=dict(colors=['#d4af37', '#b8922a', '#9c791d', '#816111', '#6b541a', '#524013', '#392c0d', '#282828', '#1a1a1a', '#000'])
        )])
        fig_pie_br.update_layout(title="% Relevância Patrimonial", template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_pie_br, use_container_width=True)

    st.markdown("""
        <div class='state-message'>
            <b>ANÁLISE DE ESTADO:</b> A soberania brasileira é sustentada pela matriz energética e mineral. 
            A dominância global no Nióbio (através da CBMM/Vale) e a autossuficiência da Petrobras 
            garantem ao país um poder de negociação ímpar no BRICS+. Aumentar a reserva física de Ouro 
            é o próximo passo estratégico para a estabilidade do Real frente ao cenário global.
        </div>
    """, unsafe_allow_html=True)

elif menu == "🙏 Devocional de Poder":
    # Este bloco não estava no seu código original, mas estou adicionando para garantir que funcione.
    st.title("🙏 Devocional de Poder")
    st.info("Módulo em desenvolvimento.")

elif menu == "🤝 Conselho de Elite":
    st.title("🤝 Conselho de Elite & Diretrizes")
    
    st.markdown("""
        <div class='card-quantum'>
            Este é o centro de comando estratégico. Antes de qualquer execução no mercado, 
            verifique se o seu alinhamento operacional cumpre os requisitos de Soberania.
        </div>
    """, unsafe_allow_html=True)

    st.subheader("📋 Protocolo de Pré-Abertura")
    c1, c2 = st.columns(2)
    with c1:
        st.checkbox("Devocional realizado e mente em estado de governo.")
        st.checkbox("Análise de Volatilidade de Vórtice (Tesla) concluída.")
        st.checkbox("Conferência de calendários econômicos (Payroll/FED/IPCA).")
    with c2:
        st.checkbox("Verificação de margens em ativos High-Ticket.")
        st.checkbox("Monitoramento de fluxo institucional em Commodities.")
        st.checkbox("Backups de segurança e conexão de terminal ativos.")

    st.write("---")

    st.subheader("📜 As 7 Leis de Ferro do Capital")
    
    leis = {
        "1. Preservação": "O primeiro objetivo não é ganhar, é não perder o lastro principal.",
        "2. Paciência": "O mercado é o mecanismo que transfere dinheiro dos impacientes para os pacientes.",
        "3. Confluência": "Nunca opere por impulso. Espere o cruzamento de pelo menos 3 indicadores (Técnico, Fundamental e Vórtice).",
        "4. Escalabilidade": "Se o seu negócio (E-commerce/Pet) não escala sem você, você tem um emprego, não um ativo.",
        "5. Diversificação Soberana": "Mantenha parte do lucro em ativos físicos (Ouro/Nióbio) fora do sistema bancário comum.",
        "6. High-Ticket": "Foque no topo da pirâmide. O esforço para vender um produto de 10 reais é o mesmo para vender um de 10 mil.",
        "7. Transbordo": "A riqueza que para em você apodrece. O capital deve fluir para gerar novos legados."
    }

    for titulo, desc in leis.items():
        st.markdown(f"**{titulo}:** {desc}")

    st.write("---")

    st.subheader("🚀 Planejamento de Expansão (E-commerce & Pet)")
    col_e1, col_e2, col_e3 = st.columns(3)
    
    with col_e1:
        st.metric("META E-COMMERCE PET", "R$ 50k", "+12% vs mês anterior")
    with col_e2:
        st.metric("YIELD CARTEIRA TRADE", "4.2% a.m", "Acima do Benchmark")
    with col_e3:
        st.metric("RESERVA DE SOBERANIA", "15% Patrimônio", "Em Ouro/BTC")

    st.markdown("""
        <div class='state-message' style='text-align: center; border-left: none; border: 1px solid #d4af37;'>
            <h3 style='color: #d4af37; margin-bottom: 5px;'>SISTEMA QUANTUM NEXUS ELITE</h3>
            <p style='color: #666; font-size: 0.8rem;'>
                Desenvolvido para Gestão de Estado e Soberania Financeira.  

                Status: <b>PROTEGIDO POR CRIPTOGRAFIA DE VÓRTICE</b>  

                © 2026 - Todos os direitos reservados à soberania do usuário.
            </p>
        </div>

