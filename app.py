import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import random
import time
from datetime import datetime

# --- CONFIGURAÇÃO DE INTERFACE SUPREMA ---
st.set_page_config(page_title="Quantum Nexus Elite", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 2px solid #d4af37; }
    h1, h2, h3 { color: #d4af37; font-family: 'Inter', sans-serif; text-transform: uppercase; }
    .stButton>button { 
        border-radius: 12px; border: none; 
        background: linear-gradient(45deg, #d4af37, #f9e295); 
        color: black; font-weight: bold; width: 100%; height: 50px; 
    }
    .card-quantum { border-radius: 20px; background: #111; padding: 25px; border: 1px solid #222; }
    .devocional-texto { line-height: 1.8; font-size: 1.1rem; color: #f2f2f2; font-style: italic; border-left: 4px solid #d4af37; padding-left: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE DE DADOS (PRECISÃO DE CORRETORA) ---
def get_market_data(ticker, label):
    try:
        # Forçamos a limpeza de cache para dados novos
        data = yf.download(ticker, period="60d", interval="1d", progress=False, auto_adjust=True)
        if data.empty:
            st.warning(f"⚠️ Sincronizando dados de {label}... Tente novamente em instantes.")
            return None
        
        fig = go.Figure(data=[go.Candlestick(
            x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
            increasing_line_color='#d4af37', decreasing_line_color='#ff4b4b'
        )])
        fig.update_layout(template='plotly_dark', paper_bgcolor='black', plot_bgcolor='black', 
                          height=450, title=f"TERMINAL REAL: {label}", margin=dict(l=0, r=0, t=40, b=0))
        return fig
    except Exception as e:
        st.error(f"Erro de Conexão no Terminal {label}")
        return None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 22px;'>⚡ NEXUS ELITE</h1>", unsafe_allow_html=True)
    menu = st.radio("SISTEMAS OPERACIONAIS:", 
                    ["💎 IA Quântico Tesla", "🐾 Pet Intelligence", "💹 Trade & Commodities", "👗 Fashion High-Ticket", "🌍 Soberania & Reservas", "🙏 Devocional de Poder", "🤝 Conselho de Elite"])
    st.write("---")
    st.write(f"🚀 **Operador:** Cristiano Noronha")
    st.caption(f"Pulso: {datetime.now().strftime('%H:%M:%S')}")

# --- MÓDULOS ---

if menu == "💎 IA Quântico Tesla":
    st.title("💎 IA Quântico Tesla & Astrolábio")
    st.info("Algoritmo de Frequência 3-6-9 Ativado.")
    jogo = st.selectbox("Selecione a Modalidade de Ganho:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    
    if st.button("GERAR CONFLUÊNCIA QUÂNTICA"):
        with st.status("🌀 Alinhando Astrolábio Quântico...", expanded=True):
            time.sleep(1.5)
            config = {"Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5), "Lotomania": (100, 50), "Milionária": (50, 6)}
            n_max, n_qtd = config[jogo]
            # Lógica Tesla Cirúrgica
            base = [n for n in range(1, n_max + 1) if (n % 9 in [3, 6, 0]) or (sum(int(d) for d in str(n)) % 9 == 0)]
            if len(base) < n_qtd: base = list(range(1, n_max + 1))
            res = sorted(random.sample(base, n_qtd))
            st.markdown(f"<div class='card-quantum'><h1 style='text-align:center; color:#d4af37;'>{', '.join(map(str, res))}</h1></div>", unsafe_allow_html=True)

elif menu == "🐾 Pet Intelligence":
    st.title("🐾 Pet Global Intelligence - Top 10 Elite")
    
    # 1. DICIONÁRIO TOP 10 (Nacional e Internacional)
    tickers_pet = {
        "Petz (Brasil)": "PETZ3.SA",
        "Zoetis (Saúde Animal)": "ZTS",
        "IDEXX (Laboratórios)": "IDXX",
        "Chewy (E-commerce)": "CHWY",
        "PetMed Express": "PETS",
        "Freshpaw": "FRPT",
        "Trupanion (Seguros)": "TRUP",
        "Central Garden": "CENT",
        "Dechra Pharma": "DPH.L",
        "Phibro Animal Health": "PAHC"
    }
    
    selecao = st.selectbox("Selecione a Gigante para Análise:", list(tickers_pet.keys()))
    ticker_final = tickers_pet[selecao]

    # 2. GRÁFICO DE CORRETORA (ALTA E BAIXA)
    try:
        # Buscando dados reais
        df_pet = yf.download(ticker_final, period="60d", interval="1d", progress=False)
        
        if not df_pet.empty:
            # Força a limpeza para o gráfico não vir vazio
            df_pet.columns = [col[0] if isinstance(col, tuple) else col for col in df_pet.columns]
            
            fig_pet = go.Figure(data=[go.Candlestick(
                x=df_pet.index,
                open=df_pet['Open'],
                high=df_pet['High'],
                low=df_pet['Low'],
                close=df_pet['Close'],
                increasing_line_color='#00FF00', # Verde
                decreasing_line_color='#FF0000'  # Vermelho
            )])
            
            fig_pet.update_layout(
                title=f"Terminal Pro: {selecao}",
                template='plotly_dark',
                xaxis_rangeslider_visible=False,
                height=500,
                paper_bgcolor='black',
                plot_bgcolor='black'
            )
            st.plotly_chart(fig_pet, use_container_width=True)
            
            # Métricas Reais
            v_atual = float(df_pet['Close'].iloc[-1])
            v_abertura = float(df_pet['Open'].iloc[-1])
            delta = v_atual - v_abertura
            st.metric("PREÇO ATUAL", f"$ {v_atual:.2f}", f"{delta:.2f}")
        else:
            st.warning("Conectando aos servidores da Bolsa... aguarde.")
    except Exception as e:
        st.error(f"Erro técnico na renderização: {e}")

    # 3. TENDÊNCIAS GLOBAIS (CARDS MODERNOS)
    st.markdown("---")
    st.subheader("🌍 Tendências Globais Pet")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div style='background:#111; padding:15px; border-radius:10px; border-left:4px solid #d4af37;'><b>🧬 Longevidade</b><br>Aumento de 25% em suplementação premium.</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='background:#111; padding:15px; border-radius:10px; border-left:4px solid #d4af37;'><b>🏠 Pet-as-Family</b><br>Imobiliário de luxo adaptado para pets.</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div style='background:#111; padding:15px; border-radius:10px; border-left:4px solid #d4af37;'><b>📊 Market Share</b><br>Saúde Animal lidera com 42% do lucro do setor.</div>", unsafe_allow_html=True)

elif menu == "💹 Trade & Commodities":
    st.title("💹 Terminal Trade & Commodities de Estado")
    
    # 1. LISTA DE ATIVOS (Incluindo Nióbio, Grafeno e Metais)
    ativos_commodities = {
        "Ouro (Reserva de Valor)": "GC=F",
        "Prata (Industrial/Refúgio)": "SI=F",
        "Cobre (Base Tecnológica)": "HG=F",
        "Petróleo Brent (Energia)": "BZ=F",
        "Nióbio (Via Vale - Proxy BR)": "VALE3.SA",
        "Grafeno (Via Applied Graphene)": "AGM.L",
        "Bitcoin (Ouro Digital)": "BTC-USD",
        "Dólar (DXY Index)": "DX-Y.NYB"
    }
    
    selecao_c = st.selectbox("Selecione o Ativo Estratégico:", list(ativos_commodities.keys()))
    ticker_c = ativos_commodities[selecao_c]

    # 2. GRÁFICO DE CORRETORA (VELAS DE ALTA E BAIXA)
    try:
        df_c = yf.download(ticker_c, period="60d", interval="1d", progress=False)
        
        if not df_c.empty:
            # Limpeza de colunas para garantir que o gráfico de velas funcione
            df_c.columns = [col[0] if isinstance(col, tuple) else col for col in df_c.columns]
            df_c = df_c.dropna()

            fig_c = go.Figure(data=[go.Candlestick(
                x=df_c.index,
                open=df_c['Open'],
                high=df_c['High'],
                low=df_c['Low'],
                close=df_c['Close'],
                increasing_line_color='#00FF00', # Verde de Alta
                decreasing_line_color='#FF0000'  # Vermelho de Baixa
            )])
            
            fig_c.update_layout(
                title=f"Terminal Pro: {selecao_c}",
                template='plotly_dark',
                xaxis_rangeslider_visible=False,
                height=500,
                paper_bgcolor='black',
                plot_bgcolor='black'
            )
            st.plotly_chart(fig_c, use_container_width=True)
            
            # Métricas em Tempo Real
            v_atual = float(df_c['Close'].iloc[-1])
            v_abertura = float(df_c['Open'].iloc[-1])
            delta_perc = ((v_atual - v_abertura) / v_abertura) * 100
            st.metric("COTAÇÃO ATUAL", f"$ {v_atual:.2f}", f"{delta_perc:.2f}%")
        else:
            st.warning("⚠️ Ativo em negociação ou mercado fechado. Tente novamente.")
    except Exception as e:
        st.error(f"Erro na conexão com o mercado: {e}")

    # 3. GRÁFICO DE PIZZA (RESERVAS GLOBAIS - SOBERANIA)
    st.markdown("---")
    st.subheader("🌍 Soberania: Maiores Reservas por País")
    
    # Lógica para mudar a pizza conforme o material selecionado
    if "Nióbio" in selecao_c:
        labels_p = ['Brasil', 'Canadá', 'Austrália', 'Outros']
        values_p = [92, 7, 0.5, 0.5]
    elif "Ouro" in selecao_c:
        labels_p = ['EUA', 'Alemanha', 'FMI', 'Itália', 'Outros']
        values_p = [25, 10, 8, 7, 50]
    else:
        labels_p = ['China', 'EUA', 'Brasil', 'Rússia', 'Outros']
        values_p = [35, 20, 15, 10, 20]

    fig_pizza_c = go.Figure(data=[go.Pie(labels=labels_p, values=values_p, hole=.4)])
    fig_pizza_c.update_layout(template='plotly_dark', title="Distribuição de Poder/Reserva")
    st.plotly_chart(fig_pizza_c)

    # 4. PAINEL DE INFORMAÇÕES TÉCNICAS (MATERIAIS)
    st.markdown("---")
    st.subheader("💎 Inteligência de Materiais")
    col1, col2 = st.columns(2)
    with col1:
        st.info("🚀 **Nióbio & Grafeno:** Materiais críticos para a indústria aeroespacial e baterias de ultra-rápida carga.")
    with col2:
        st.success("📈 **Prata & Cobre:** Demanda crescente devido à transição energética (Painéis Solares e Carros Elétricos).")
        # --- INSERIR LOGO ABAIXO DO MÓDULO TRADE & COMMODITIES ---

elif menu == "👗 Fashion High-Ticket":
    st.title("👗 Fashion High-Ticket: Bolsa de Valores da Moda")
    st.markdown("<div class='card-quantum'>Monitoramento das 20 potências do Luxo Global e Nacional.</div>", unsafe_allow_html=True)

    # 1. DICIONÁRIO DE ATIVOS FASHION
    marcas_moda = {
        "GLOBAL: LVMH (Louis Vuitton)": "MC.PA",
        "GLOBAL: Hermès": "RMS.PA",
        "GLOBAL: Kering (Gucci)": "KER.PA",
        "GLOBAL: Prada": "1913.HK",
        "GLOBAL: Nike": "NKE",
        "GLOBAL: Ralph Lauren": "RL",
        "GLOBAL: Moncler": "MONC.MI",
        "GLOBAL: Burberry": "BRBY.L",
        "GLOBAL: Capri (Versace)": "CPRI",
        "GLOBAL: Tapestry (Coach)": "TPR",
        "BRASIL: Arezzo&Co": "ARZZ3.SA",
        "BRASIL: Grupo Soma (Farm)": "SOMA3.SA",
        "BRASIL: Track&Field": "TFCO4.SA",
        "BRASIL: Vivara": "VIVA3.SA",
        "BRASIL: Lojas Renner": "LREN3.SA",
        "BRASIL: Alpargatas": "ALPA4.SA",
        "BRASIL: Guararapes": "GUAR3.SA",
        "BRASIL: Vulcabras": "VULC3.SA",
        "BRASIL: Grendene": "GRND3.SA",
        "BRASIL: Hering (Soma)": "SOMA3.SA"
    }

    selecao_moda = st.selectbox("Escolha a Marca para Análise:", list(marcas_moda.keys()))
    ticker_moda = marcas_moda[selecao_moda]

    # 2. GRÁFICO DE CORRETORA (CANDLESTICK)
    try:
        df_moda = yf.download(ticker_moda, period="60d", interval="1d", progress=False)
        if not df_moda.empty:
            df_moda.columns = [col[0] if isinstance(col, tuple) else col for col in df_moda.columns]
            df_moda = df_moda.dropna()

            fig_moda = go.Figure(data=[go.Candlestick(
                x=df_moda.index,
                open=df_moda['Open'],
                high=df_moda['High'],
                low=df_moda['Low'],
                close=df_moda['Close'],
                increasing_line_color='#00FF00', # Verde
                decreasing_line_color='#FF0000'  # Vermelho
            )])
            
            fig_moda.update_layout(
                title=f"Terminal High-Ticket: {selecao_moda}",
                template='plotly_dark',
                xaxis_rangeslider_visible=False,
                height=500,
                paper_bgcolor='black', plot_bgcolor='black'
            )
            st.plotly_chart(fig_moda, use_container_width=True)

            # MÉTRICAS
            v_atual = float(df_moda['Close'].iloc[-1])
            v_abertura = float(df_moda['Open'].iloc[-1])
            delta_p = ((v_atual - v_abertura) / v_abertura) * 100
            st.metric("VALOR DA AÇÃO", f" {v_atual:.2f}", f"{delta_p:.2f}%")
    except:
        st.warning("Buscando dados na Bolsa de Paris/Milão/NY/B3...")

    # 3. GRÁFICOS DE PIZZA (MARKET SHARE)
    st.markdown("---")
    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.subheader("Dominância por Gênero")
        fig_gen = go.Figure(data=[go.Pie(labels=['Feminino', 'Masculino', 'Unissex'], 
                                       values=[55, 35, 10], hole=.4)])
        fig_gen.update_layout(template='plotly_dark')
        st.plotly_chart(fig_gen)

    with col_p2:
        st.subheader("Market Share Global Luxo")
        fig_share = go.Figure(data=[go.Pie(labels=['LVMH', 'Hermès', 'Kering', 'Chanel', 'Outros'], 
                                         values=[35, 20, 15, 10, 20], hole=.4)])
        fig_share.update_layout(template='plotly_dark')
        st.plotly_chart(fig_share)
        elif menu == "🌍 Soberania & Reservas":
    st.title("🌍 Soberania & Reservas: O Poder das Nações")
    st.markdown("<div class='card-quantum'>Monitoramento de ativos estratégicos e reservas de segurança nacional.</div>", unsafe_allow_html=True)

    # 1. ATIVOS ESTRATÉGICOS
    ativos_soberania = {
        "Ouro (Reserva Global)": "GC=F",
        "Prata (Metal Industrial)": "SI=F",
        "Nióbio (Via Vale - Proxy)": "VALE3.SA",
        "Petróleo Brent (Energia)": "BZ=F",
        "Urânio (Energia Nuclear)": "URA",
        "Cobre (Transição Energética)": "HG=F"
    }

    selecao_s = st.selectbox("Selecione o Ativo de Estado:", list(ativos_soberania.keys()))
    ticker_s = ativos_soberania[selecao_s]

    # 2. GRÁFICO DE CORRETORA (CANDLESTICK)
    try:
        df_s = yf.download(ticker_s, period="60d", interval="1d", progress=False)
        if not df_s.empty:
            df_s.columns = [col[0] if isinstance(col, tuple) else col for col in df_s.columns]
            df_s = df_s.dropna()

            fig_s = go.Figure(data=[go.Candlestick(
                x=df_s.index,
                open=df_s['Open'],
                high=df_s['High'],
                low=df_s['Low'],
                close=df_s['Close'],
                increasing_line_color='#d4af37', # Dourado para alta
                decreasing_line_color='#ff4b4b'  # Vermelho para queda
            )])
            
            fig_s.update_layout(
                title=f"Monitoramento de Soberania: {selecao_s}",
                template='plotly_dark',
                xaxis_rangeslider_visible=False,
                height=500,
                paper_bgcolor='black', plot_bgcolor='black'
            )
            st.plotly_chart(fig_s, use_container_width=True)

            # MÉTRICAS DE VALOR ESTRATÉGICO
            v_atual = float(df_s['Close'].iloc[-1])
            v_ontem = float(df_s['Close'].iloc[-2])
            variacao = ((v_atual - v_ontem) / v_ontem) * 100
            st.metric("PREÇO DE MERCADO", f"$ {v_atual:.2f}", f"{variacao:.2f}%")
    except:
        st.warning("Sincronizando com o Banco Mundial e bolsas de commodities...")

    # 3. GRÁFICOS DE PIZZA (QUEM DETÉM O PODER)
    st.markdown("---")
    st.subheader("📊 Distribuição de Reservas Mundiais (%)")
    col_r1, col_r2 = st.columns(2)

    with col_r1:
        # Dinâmica para Nióbio ou Ouro
        if "Nióbio" in selecao_s:
            labels_p = ['Brasil', 'Canadá', 'Austrália', 'Outros']
            values_p = [92, 7, 0.5, 0.5]
            st.write("**Reservas de Nióbio**")
        elif "Ouro" in selecao_s:
            labels_p = ['EUA', 'Alemanha', 'FMI', 'Itália', 'França', 'Rússia', 'China']
            values_p = [25, 10, 8, 7, 7, 6, 5]
            st.write("**Reservas de Ouro (Bancos Centrais)**")
        else:
            labels_p = ['China', 'EUA', 'Brasil', 'Rússia', 'Outros']
            values_p = [35, 20, 15, 10, 20]
            st.write("**Reservas Estratégicas Gerais**")

        fig_res = go.Figure(data=[go.Pie(labels=labels_p, values=values_p, hole=.4)])
        fig_res.update_layout(template='plotly_dark')
        st.plotly_chart(fig_res)

    with col_r2:
        st.info("💡 **Destaque Geopolítico:**")
        if "Nióbio" in selecao_s:
            st.write("O Brasil possui o monopólio prático do Nióbio. É o material essencial para turbinas de aviões e foguetes. Sem o Brasil, a indústria aeroespacial para.")
        elif "Ouro" in selecao_s:
            st.write("Bancos Centrais compraram níveis recordes de Ouro em 2024 e 2025 para reduzir a dependência do Dólar.")
        else:
            st.write("A transição energética depende de Cobre e Lítio. A China hoje domina 60% do processamento desses materiais.")

    # 4. TABELA DE SOBERANIA NACIONAL
    st.markdown("---")
    st.subheader("🇧🇷 Brasil: Potencial de Exportação Estratégica")
    st.table({
        "Material": ["Nióbio", "Minério de Ferro", "Petróleo", "Soja", "Lítio"],
        "Posição Mundial": ["1º", "2º", "9º", "1º", "5º"],
        "Status": ["Domínio Total", "Liderança de Mercado", "Expansão OPEP+", "Celeiro do Mundo", "Nova Fronteira"]
    })

elif menu == "🙏 Devocional de Poder":
    st.title("🙏 Conexão com o Alto")
    st.markdown("""
    <div class='card-quantum'>
        <h2 style='text-align:center'>O SEGREDO DA PROSPERIDADE REAL</h2>
        <p class='devocional-texto'>
            "Honre ao Senhor com todos os seus recursos e com os primeiros frutos de todas as suas colheitas..." (Provérbios 3:9)
        </p>
        <p style='color:#ccc'>
            Cristiano, meu irmão, o sucesso sem propósito é apenas um número. Quando você alinha sua mente com o Criador, 
            cada operação financeira se torna uma ferramenta de construção de legado. <br><br>
            <b>Explicação Emotiva:</b> Não foque apenas no lucro, foque na sabedoria que vem do alto. O lucro é a consequência 
            natural de uma mente em paz e obediente. Que sua noite seja de descanso, pois o Dono do Ouro guarda seus passos.
        </p>
    </div>
    """, unsafe_allow_html=True)

elif menu == "🤝 Conselho de Elite":
    st.title("🤝 Conselho de Elite")
    st.success("Mindset Ativado: 'O Operador de Elite antecipa o que o mundo ainda não viu.'")
    st.markdown("<div class='card-quantum'>🚀 Foco: Legado, Expansão e Domínio de Mercado.</div>", unsafe_allow_html=True)
