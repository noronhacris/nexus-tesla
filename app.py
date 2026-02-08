
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import time

# 
# 1. CONFIGURAÇÃO DE ALTA PERFORMANCE E CABEÇALHO DO SISTEMA
# 
st.set_page_config(
    page_title="Quantum Nexus Elite - Terminal de Estado",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 
# 2. ESTILIZAÇÃO VISUAL CUSTOMIZADA (CSS DE ELITE)
# 
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=JetBrains+Mono:wght@400;700&display=swap');

    .stApp {
        background-color: #000000;<br/>
        color: #FFFFFF;<br/>
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #050505;<br/>
        border-right: 2px solid #d4af37;<br/>
        box-shadow: 10px 0px 40px rgba(212, 175, 55, 0.15);
    }
    [data-testid="stSidebar"] .stButton>button {
        border-radius: 10px;<br/>
        border: 1px solid #d4af37;<br/>
        background: linear-gradient(135deg, #1a1a1a 0%, #000 100%);<br/>
        color: #d4af37 !important;<br/>
        font-weight: 700;<br/>
        text-transform: uppercase;<br/>
        letter-spacing: 1px;<br/>
        width: 100%;<br/>
        height: 50px;<br/>
        transition: all 0.3s ease-in-out;<br/>
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);<br/>
        margin-bottom: 10px;
    }
    [data-testid="stSidebar"] .stButton>button:hover {<br/>
        transform: translateY(-3px) scale(1.01);<br/>
        background: linear-gradient(135deg, #d4af37 0%, #f9e295 100%);<br/>
        color: #000 !important;<br/>
        box-shadow: 0px 8px 20px rgba(212, 175, 55, 0.4);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #d4af37;<br/>
        font-family: 'JetBrains Mono', monospace;<br/>
        letter-spacing: 2px;<br/>
        text-transform: uppercase;<br/>
        font-weight: 700;<br/>
        margin-top: 1.5rem;<br/>
        margin-bottom: 1rem;
    }
    .stButton>button {
        border-radius: 15px;<br/>
        border: 1px solid #d4af37;<br/>
        background: linear-gradient(135deg, #1a1a1a 0%, #000 100%);<br/>
        color: #d4af37 !important;<br/>
        font-weight: 800;<br/>
        text-transform: uppercase;<br/>
        letter-spacing: 2px;<br/>
        width: 100%;<br/>
        height: 65px;<br/>
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);<br/>
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.5);
    }
    .stButton>button:hover {<br/>
        transform: translateY(-5px) scale(1.01);<br/>
        background: linear-gradient(135deg, #d4af37 0%, #f9e295 100%);<br/>
        color: #000 !important;<br/>
        box-shadow: 0px 15px 50px rgba(212, 175, 55, 0.4);
    }
    .stTextInput>div>div>input {
        background-color: #1a1a1a;<br/>
        color: #d4af37;<br/>
        border: 1px solid #d4af37;<br/>
        border-radius: 8px;<br/>
        padding: 10px;
    }
    .stSelectbox>div>div>div {
        background-color: #1a1a1a;<br/>
        color: #d4af37;<br/>
        border: 1px solid #d4af37;<br/>
        border-radius: 8px;<br/>
        padding: 10px;
    }
    .stMarkdown {
        color: #E0E0E0;
    }
    .stAlert {
        background-color: #2a2a2a;<br/>
        color: #d4af37;<br/>
        border-left: 5px solid #d4af37;<br/>
        border-radius: 5px;
    }
    .stMetric {
        background-color: #1a1a1a;<br/>
        border: 1px solid #333333;<br/>
        border-radius: 10px;<br/>
        padding: 15px;<br/>
        margin-bottom: 10px;<br/>
        box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.3);
    }
    .stMetric > div > div:first-child {<br/>
        color: #d4af37;<br/>
        font-family: 'JetBrains Mono', monospace;<br/>
        font-weight: 700;<br/>
        font-size: 1.2em;
    }
    .stMetric > div > div:last-child {<br/>
        color: #FFFFFF;<br/>
        font-family: 'Inter', sans-serif;<br/>
        font-size: 1.5em;
    }
    .stTable, .dataframe {
        color: #E0E0E0;<br/>
        background-color: #1a1a1a;<br/>
        border: 1px solid #333333;<br/>
        border-radius: 10px;<br/>
        padding: 10px;
    }
    .dataframe th {
        background-color: #d4af37;<br/>
        color: #000000;<br/>
        font-weight: bold;
    }
    .dataframe td {
        background-color: #0a0a0a;<br/>
        color: #E0E0E0;
    }
    .stExpander {
        border: 1px solid #d4af37;<br/>
        border-radius: 10px;<br/>
        padding: 10px;<br/>
        background-color: #0a0a0a;<br/>
        margin-bottom: 15px;
    }
    .stExpander > div > div > div > p {
        color: #E0E0E0;
    }
    .stExpander > div > div > div > div > p {
        color: #d4af37;<br/>
        font-family: 'JetBrains Mono', monospace;<br/>
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 
# 3. FUNÇÕES DE UTILIDADE E CACHE DE DADOS
# 

@st.cache_data(ttl=3600) # Cache por 1 hora
def get_stock_data(ticker, period='1y'):<br/>
    try:
        data = yf.download(ticker, period=period)
        if not data.empty:
            data.index = pd.to_datetime(data.index)
            data = data.dropna()
            return data
        return pd.DataFrame()
    except Exception as e:<br/>
        st.error(f"Erro ao buscar dados para {ticker}: {e}")
        return pd.DataFrame()

def plot_candlestick(df, title):<br/>
    if df.empty:
        return go.Figure().update_layout(title=title, template="plotly_dark",
                                         paper_bgcolor="#000000", plot_bgcolor="#000000",
                                         font_color="#d4af37")

    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                         open=df['Open'],
                                         high=df['High'],
                                         low=df['Low'],
                                         close=df['Close'],
                                         increasing_line_color='#26A69A', # Verde
                                         decreasing_line_color='#EF5350')]) # Vermelho

    fig.update_layout(
        title=f'<span style="color:#d4af37">{title}</span>',
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font_color="#E0E0E0",
        xaxis_title="Data",
        yaxis_title="Preço",
        xaxis=dict(showgrid=True, gridcolor="#333333"),
        yaxis=dict(showgrid=True, gridcolor="#333333"),
    )
    return fig

def calculate_support_resistance(df, window=20):<br/>
    if df.empty or len(df) < window:
        return None, None
    df['SMA'] = df['Close'].rolling(window=window).mean()
    support = df['Low'].rolling(window=window).min().iloc[-1]
    resistance = df['High'].rolling(window=window).max().iloc[-1]
    return support, resistance

def generate_simulated_data(ticker, days=365):
    dates = [datetime.now() - timedelta(days=i) for i in range(days)]
    dates.reverse()
    base_price = random.uniform(50, 500)
    data = []
    for date in dates:
        open_price = base_price + random.uniform(-5, 5)
        close_price = open_price + random.uniform(-10, 10)
        high_price = max(open_price, close_price) + random.uniform(0, 5)
        low_price = min(open_price, close_price) - random.uniform(0, 5)
        volume = random.randint(100000, 5000000)
        data.append([date, open_price, high_price, low_price, close_price, volume])
        base_price = close_price # Update base for next day
    df = pd.DataFrame(data, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    df.set_index('Date', inplace=True)
    return df

# 
# 4. NAVEGAÇÃO NA SIDEBAR
# 
st.sidebar.title("Quantum Nexus Elite")
st.sidebar.markdown("---")
st.sidebar.header("Módulos de Análise")

modules = {
    "PET GLOBAL": "🐾 Pet Global",<br/>
    "FASHION GLOBAL": "👗 Fashion Global",<br/>
    "SOBERANIA & AGRO": "🌾 Soberania & Agro",<br/>
    "IA QUÂNTICO TESLA": "🧠 IA Quântico Tesla",<br/>
    "DEVOCIONAL COM DEUS": "🙏 Devocional com Deus",
}

selected_module = st.sidebar.radio(
    "Selecione um Módulo:",
    list(modules.keys()),
    format_func=lambda x: modules[x],
    key="main_module_selector"
)
st.sidebar.markdown("---")
st.sidebar.info(f"Última Atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 
# 5. CONTEÚDO DOS MÓDULOS
# 

if selected_module == "PET GLOBAL":<br/>
    st.title("🐾 PET GLOBAL: Insights de Mercado e Tendências")
    st.markdown("Análise aprofundada do mercado pet em escala global, com foco em tendências, empresas líderes e o setor farmacêutico veterinário.")

    st.subheader("Tendências Globais do Mercado Pet")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 🇺🇸 EUA")
        st.metric("Crescimento Anual", "8.5%", "0.5%")
        st.markdown("O mercado pet dos EUA continua a ser o maior, impulsionado por humanização de pets e produtos premium.")
        fig_us = go.Figure(data=[go.Scatter(y=[random.uniform(100, 150) for _ in range(12)], mode='lines', line_color='#d4af37')])
        fig_us.update_layout(title="Crescimento Mensal (Simulado)", template="plotly_dark", paper_bgcolor="#000000", plot_bgcolor="#000000", font_color="#E0E0E0", height=200)
        st.plotly_chart(fig_us, use_container_width=True)

    with col2:
        st.markdown("#### 🇨🇳 China")
        st.metric("Crescimento Anual", "12.1%", "1.2%")
        st.markdown("A China apresenta o crescimento mais rápido, com a classe média adotando mais pets e demandando produtos de luxo.")
        fig_cn = go.Figure(data=[go.Scatter(y=[random.uniform(80, 180) for _ in range(12)], mode='lines', line_color='#d4af37')])
        fig_cn.update_layout(title="Crescimento Mensal (Simulado)", template="plotly_dark", paper_bgcolor="#000000", plot_bgcolor="#000000", font_color="#E0E0E0", height=200)
        st.plotly_chart(fig_cn, use_container_width=True)

    with col3:
        st.markdown("#### 🇪🇺 Europa")
        st.metric("Crescimento Anual", "6.9%", "0.2%")
        st.markdown("A Europa mantém um crescimento estável, com foco em sustentabilidade e bem-estar animal.")
        fig_eu = go.Figure(data=[go.Scatter(y=[random.uniform(90, 140) for _ in range(12)], mode='lines', line_color='#d4af37')])
        fig_eu.update_layout(title="Crescimento Mensal (Simulado)", template="plotly_dark", paper_bgcolor="#000000", plot_bgcolor="#000000", font_color="#E0E0E0", height=200)
        st.plotly_chart(fig_eu, use_container_width=True)

    st.subheader("Top 20 Empresas Pet por País")
    pet_companies = {
        "USA": {<br/>
            "Mars Petcare": {"MarketCap": "450B", "Change": "+1.2%", "Ticker": None},<br/>
            "Chewy Inc.": {"MarketCap": "15B", "Change": "-0.8%", "Ticker": "CHWY"},<br/>
            "Zoetis Inc.": {"MarketCap": "85B", "Change": "+0.5%", "Ticker": "ZTS"},<br/>
            "Freshpet Inc.": {"MarketCap": "3B", "Change": "+2.1%", "Ticker": "FRPT"},<br/>
            "IDEXX Laboratories": {"MarketCap": "40B", "Change": "+0.3%", "Ticker": "IDXX"},<br/>
            "Petco Health and Wellness": {"MarketCap": "2B", "Change": "-1.5%", "Ticker": "WOOF"},<br/>
            "Nestlé Purina PetCare": {"MarketCap": "200B", "Change": "+0.9%", "Ticker": None},<br/>
            "J.M. Smucker Co. (Pet Food)": {"MarketCap": "12B", "Change": "+0.1%", "Ticker": "SJM"},<br/>
            "Spectrum Brands (Pet Care)": {"MarketCap": "2B", "Change": "-0.2%", "Ticker": "SPB"},<br/>
            "Blue Buffalo (General Mills)": {"MarketCap": "40B", "Change": "+0.7%", "Ticker": "GIS"},<br/>
            "Hill's Pet Nutrition (Colgate-Palmolive)": {"MarketCap": "60B", "Change": "+0.4%", "Ticker": "CL"},<br/>
            "Elanco Animal Health": {"MarketCap": "7B", "Change": "-0.6%", "Ticker": "ELAN"},<br/>
            "Dechra Pharmaceuticals (US Ops)": {"MarketCap": "5B", "Change": "+0.1%", "Ticker": None}, # Simulated<br/>
            "VCA Animal Hospitals (Mars)": {"MarketCap": "50B", "Change": "+1.0%", "Ticker": None},<br/>
            "PetSmart": {"MarketCap": "20B", "Change": "-0.3%", "Ticker": None},<br/>
            "Trupanion": {"MarketCap": "1B", "Change": "+1.8%", "Ticker": "TRUP"},<br/>
            "Zomedica Corp.": {"MarketCap": "0.2B", "Change": "+3.0%", "Ticker": "ZOM"},<br/>
            "CVS Health (Vet Services)": {"MarketCap": "90B", "Change": "+0.2%", "Ticker": "CVS"},<br/>
            "Walmart (Pet Section)": {"MarketCap": "400B", "Change": "+0.6%", "Ticker": "WMT"},<br/>
            "Target (Pet Section)": {"MarketCap": "70B", "Change": "+0.4%", "Ticker": "TGT"},
        },
        "China": {<br/>
            "Bridge PetCare": {"MarketCap": "10B", "Change": "+3.5%", "Ticker": None},<br/>
            "Gambol Pet Group": {"MarketCap": "8B", "Change": "+2.8%", "Ticker": None},<br/>
            "Yantai China Pet Foods": {"MarketCap": "5B", "Change": "+4.1%", "Ticker": None},<br/>
            "Wenzhou Pet Products": {"MarketCap": "3B", "Change": "+2.0%", "Ticker": None},<br/>
            "Shanghai Pet Food": {"MarketCap": "2B", "Change": "+1.5%", "Ticker": None},<br/>
            "Guangzhou Pet Food": {"MarketCap": "1.5B", "Change": "+1.8%", "Ticker": None},<br/>
            "Hangzhou Pet Products": {"MarketCap": "1B", "Change": "+1.2%", "Ticker": None},<br/>
            "Beijing Pet Food": {"MarketCap": "0.8B", "Change": "+1.0%", "Ticker": None},<br/>
            "Chengdu Pet Food": {"MarketCap": "0.7B", "Change": "+0.9%", "Ticker": None},<br/>
            "Nanjing Pet Products": {"MarketCap": "0.6B", "Change": "+0.8%", "Ticker": None},<br/>
            "Shenzhen Pet Food": {"MarketCap": "0.5B", "Change": "+0.7%", "Ticker": None},<br/>
            "Tianjin Pet Products": {"MarketCap": "0.4B", "Change": "+0.6%", "Ticker": None},<br/>
            "Chongqing Pet Food": {"MarketCap": "0.3B", "Change": "+0.5%", "Ticker": None},<br/>
            "Suzhou Pet Products": {"MarketCap": "0.2B", "Change": "+0.4%", "Ticker": None},<br/>
            "Wuhan Pet Food": {"MarketCap": "0.1B", "Change": "+0.3%", "Ticker": None},<br/>
            "Xi'an Pet Products": {"MarketCap": "0.08B", "Change": "+0.2%", "Ticker": None},<br/>
            "Dalian Pet Food": {"MarketCap": "0.07B", "Change": "+0.1%", "Ticker": None},<br/>
            "Qingdao Pet Products": {"MarketCap": "0.06B", "Change": "+0.0%", "Ticker": None},<br/>
            "Harbin Pet Food": {"MarketCap": "0.05B", "Change": "-0.1%", "Ticker": None},<br/>
            "Jinan Pet Products": {"MarketCap": "0.04B", "Change": "-0.2%", "Ticker": None},
        },
        "Europa": {<br/>
            "Zooplus AG": {"MarketCap": "3B", "Change": "+1.8%", "Ticker": None}, # Private now, was ZOP.DE<br/>
            "Ceva Santé Animale": {"MarketCap": "6B", "Change": "+1.1%", "Ticker": None},<br/>
            "Virbac SA": {"MarketCap": "2B", "Change": "+0.7%", "Ticker": None},<br/>
            "Dechra Pharmaceuticals PLC": {"MarketCap": "4B", "Change": "+0.9%", "Ticker": None}, # DPH.L<br/>
            "Pets at Home Group Plc": {"MarketCap": "1B", "Change": "-0.5%", "Ticker": "PETS.L"},<br/>
            "Nestlé (Purina Europe)": {"MarketCap": "300B", "Change": "+0.4%", "Ticker": "NSRGY"},<br/>
            "Royal Canin (Mars)": {"MarketCap": "50B", "Change": "+1.0%", "Ticker": None},<br/>
            "Bayer Animal Health (Elanco)": {"MarketCap": "7B", "Change": "-0.6%", "Ticker": "ELAN"}, # Now part of Elanco<br/>
            "Boehringer Ingelheim Animal Health": {"MarketCap": "40B", "Change": "+0.8%", "Ticker": None},<br/>
            "ADM (Pet Nutrition)": {"MarketCap": "40B", "Change": "+0.2%", "Ticker": "ADM"},<br/>
            "Aller Petfood": {"MarketCap": "0.5B", "Change": "+0.3%", "Ticker": None},<br/>
            "United Petfood": {"MarketCap": "1B", "Change": "+0.6%", "Ticker": None},<br/>
            "Agrolimen (Affinity Petcare)": {"MarketCap": "3B", "Change": "+0.5%", "Ticker": None},<br/>
            "ScandiPet": {"MarketCap": "0.3B", "Change": "+0.2%", "Ticker": None},<br/>
            "Josera Petfood": {"MarketCap": "0.7B", "Change": "+0.4%", "Ticker": None},<br/>
            "Arden Grange": {"MarketCap": "0.2B", "Change": "+0.1%", "Ticker": None},<br/>
            "Forthglade": {"MarketCap": "0.1B", "Change": "+0.0%", "Ticker": None},<br/>
            "Burns Pet Nutrition": {"MarketCap": "0.08B", "Change": "-0.1%", "Ticker": None},<br/>
            "James Wellbeloved": {"MarketCap": "0.07B", "Change": "-0.2%", "Ticker": None},<br/>
            "Symrise (Pet Food Ingredients)": {"MarketCap": "15B", "Change": "+0.3%", "Ticker": "SY1.DE"},
        },
        "Brasil": {<br/>
            "Petz S.A.": {"MarketCap": "2B", "Change": "-2.5%", "Ticker": "PETZ3.SA"},<br/>
            "Cobasi": {"MarketCap": "1.5B", "Change": "+1.0%", "Ticker": None},<br/>
            "Premier Pet": {"MarketCap": "1B", "Change": "+0.8%", "Ticker": None},<br/>
            "Total Alimentos": {"MarketCap": "0.8B", "Change": "+0.5%", "Ticker": None},<br/>
            "Guabi Natural": {"MarketCap": "0.6B", "Change": "+0.3%", "Ticker": None},<br/>
            "Royal Canin Brasil (Mars)": {"MarketCap": "0.5B", "Change": "+0.7%", "Ticker": None},<br/>
            "Nestlé Purina Brasil": {"MarketCap": "0.4B", "Change": "+0.6%", "Ticker": None},<br/>
            "Adimax Pet": {"MarketCap": "0.3B", "Change": "+0.4%", "Ticker": None},<br/>
            "Nutrire": {"MarketCap": "0.2B", "Change": "+0.2%", "Ticker": None},<br/>
            "Supra Alimentos": {"MarketCap": "0.15B", "Change": "+0.1%", "Ticker": None},<br/>
            "M. Dias Branco (Pet Food)": {"MarketCap": "5B", "Change": "+0.0%", "Ticker": "MDIA3.SA"},<br/>
            "BRF (Pet Food)": {"MarketCap": "15B", "Change": "-0.1%", "Ticker": "BRFS3.SA"},<br/>
            "JBS (Pet Food)": {"MarketCap": "50B", "Change": "+0.3%", "Ticker": "JBSS3.SA"},<br/>
            "Agroceres Nutrição Animal": {"MarketCap": "0.1B", "Change": "+0.1%", "Ticker": None},<br/>
            "Nutriara Alimentos": {"MarketCap": "0.09B", "Change": "+0.0%", "Ticker": None},<br/>
            "Fri-Sabor": {"MarketCap": "0.08B", "Change": "-0.1%", "Ticker": None},<br/>
            "Special Dog": {"MarketCap": "0.07B", "Change": "-0.2%", "Ticker": None},<br/>
            "Magnus": {"MarketCap": "0.06B", "Change": "-0.3%", "Ticker": None},<br/>
            "Golden": {"MarketCap": "0.05B", "Change": "-0.4%", "Ticker": None},<br/>
            "GranPlus": {"MarketCap": "0.04B", "Change": "-0.5%", "Ticker": None},
        }
    }

    for country, companies in pet_companies.items():
        st.markdown(f"### {country}")
        df_companies = pd.DataFrame.from_dict(companies, orient='index')
        df_companies.index.name = "Empresa"
        st.dataframe(df_companies.head(20))

        # Candlestick para empresas com ticker
        tickers_to_plot = [info["Ticker"] for info in companies.values() if info["Ticker"]]
        if tickers_to_plot:
            st.markdown(f"#### Gráficos de Ações para Principais Empresas de {country}")
            cols_charts = st.columns(min(len(tickers_to_plot), 3))
            for i, ticker in enumerate(tickers_to_plot):<br/>
                with cols_charts[i % 3]:
                    data = get_stock_data(ticker)
                    if not data.empty:
                        st.plotly_chart(plot_candlestick(data, f"{ticker} - {country}"), use_container_width=True)
                        support, resistance = calculate_support_resistance(data)
                        if support and resistance:<br/>
                            st.markdown(f"**Suporte:** R$ {support:.2f} | **Resistência:** R$ {resistance:.2f}")<br/>
                    else:
                        st.warning(f"Dados não disponíveis para {ticker}")

    st.subheader("Mercado Farmacêutico Pet por País")
    pharma_data = {
        "USA": [random.uniform(5, 10) for _ in range(5)],<br/>
        "China": [random.uniform(3, 8) for _ in range(5)],<br/>
        "Europa": [random.uniform(4, 9) for _ in range(5)],<br/>
        "Brasil": [random.uniform(2, 6) for _ in range(5)],
    }
    pharma_df = pd.DataFrame(pharma_data, index=[f"Ano {i+1}" for i in range(5)])
    pharma_df.index.name = "Ano"
    st.dataframe(pharma_df.T.style.format("{:.2f} Bilhões USD"))

    fig_pharma = go.Figure()
    for country, data in pharma_data.items():
        fig_pharma.add_trace(go.Scatter(x=pharma_df.index, y=data, mode='lines+markers', name=country))
    fig_pharma.update_layout(
        title='<span style="color:#d4af37">Crescimento do Mercado Farmacêutico Pet (Simulado)</span>',
        template="plotly_dark",
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font_color="#E0E0E0",
        xaxis_title="Ano",
        yaxis_title="Valor de Mercado (Bilhões USD)",
        legend_title="País"
    )
    st.plotly_chart(fig_pharma, use_container_width=True)

    st.subheader("Dicas de Tendências Chegando ao Brasil")
    trends = [
        {"title": "Alimentos Funcionais Personalizados", "desc": "Dietas sob medida para pets com base em genética e saúde, com ingredientes premium e suplementos específicos."},<br/>
        {"title": "Tecnologia Wearable para Pets", "desc": "Monitores de atividade, saúde e localização para pets, integrados a apps e clínicas veterinárias."},<br/>
        {"title": "Serviços de Bem-Estar e Luxo", "desc": "Spas, hotéis boutique, creches com atividades enriquecedoras e terapias alternativas para pets."},<br/>
        {"title": "Produtos Sustentáveis e Eco-friendly", "desc": "Brinquedos biodegradáveis, rações com ingredientes de origem sustentável e embalagens recicláveis."},<br/>
        {"title": "Telemedicina Veterinária", "desc": "Consultas online, monitoramento remoto e diagnósticos à distância, facilitando o acesso a cuidados especializados."},
    ]
    for trend in trends:
        st.expander(f"**{trend['title']}**").markdown(trend['desc'])

elif selected_module == "FASHION GLOBAL":<br/>
    st.title("👗 FASHION GLOBAL: Marcas de Luxo e Mercado Brasileiro")
    st.markdown("Análise das maiores marcas de moda internacionais e brasileiras, com foco em valor de mercado, ações e tendências.")

    fashion_brands_global = {
        "LVMH Moët Hennessy Louis Vuitton": {"Ticker": "LVMUY", "MarketCap": "400B", "Share": "15%", "Country": "France"},<br/>
        "Hermès International": {"Ticker": "HESAY", "MarketCap": "200B", "Share": "8%", "Country": "France"},<br/>
        "Kering S.A.": {"Ticker": "PPRUY", "MarketCap": "70B", "Share": "5%", "Country": "France"},<br/>
        "Richemont": {"Ticker": "CFRUY", "MarketCap": "80B", "Share": "6%", "Country": "Switzerland"},<br/>
        "Chanel (Private)": {"Ticker": None, "MarketCap": "100B", "Share": "7%", "Country": "France"},<br/>
        "Prada S.p.A.": {"Ticker": "PRDSY", "MarketCap": "15B", "Share": "1%", "Country": "Italy"},<br/>
        "Moncler S.p.A.": {"Ticker": "MONRF", "MarketCap": "15B", "Share": "1%", "Country": "Italy"},<br/>
        "Burberry Group PLC": {"Ticker": "BURBY", "MarketCap": "7B", "Share": "0.5%", "Country": "UK"},<br/>
        "Ralph Lauren Corporation": {"Ticker": "RL", "MarketCap": "8B", "Share": "0.6%", "Country": "USA"},<br/>
        "Capri Holdings (Versace, Jimmy Choo, Michael Kors)": {"Ticker": "CPRI", "MarketCap": "5B", "Share": "0.4%", "Country": "USA"},<br/>
        "Tapestry Inc. (Coach, Kate Spade, Stuart Weitzman)": {"Ticker": "TPR", "MarketCap": "10B", "Share": "0.7%", "Country": "USA"},<br/>
        "PVH Corp. (Calvin Klein, Tommy Hilfiger)": {"Ticker": "PVH", "MarketCap": "7B", "Share": "0.5%", "Country": "USA"},<br/>
        "Levi Strauss & Co.": {"Ticker": "LEVI", "MarketCap": "7B", "Share": "0.5%", "Country": "USA"},<br/>
        "Adidas AG": {"Ticker": "ADDYY", "MarketCap": "40B", "Share": "3%", "Country": "Germany"},<br/>
        "Nike Inc.": {"Ticker": "NKE", "MarketCap": "150B", "Share": "10%", "Country": "USA"},<br/>
        "Inditex (Zara)": {"Ticker": "IDEXY", "MarketCap": "120B", "Share": "9%", "Country": "Spain"},<br/>
        "H&M Hennes & Mauritz AB": {"Ticker": "HMRZF", "MarketCap": "25B", "Share": "2%", "Country": "Sweden"},<br/>
        "Fast Retailing Co. Ltd. (Uniqlo)": {"Ticker": "FRCOY", "MarketCap": "80B", "Share": "6%", "Country": "Japan"},<br/>
        "Lululemon Athletica Inc.": {"Ticker": "LULU", "MarketCap": "50B", "Share": "4%", "Country": "USA"},<br/>
        "Farfetch (Luxury Platform)": {"Ticker": "FTCH", "MarketCap": "0.5B", "Share": "0.05%", "Country": "UK"},
    }

    fashion_brands_brazil = {
        "Lojas Renner S.A.": {"Ticker": "LREN3.SA", "MarketCap": "15B", "Share": "20%"},<br/>
        "Grupo Soma S.A.": {"Ticker": "SOMA3.SA", "MarketCap": "8B", "Share": "12%"},<br/>
        "Arezzo&Co S.A.": {"Ticker": "ARZZ3.SA", "MarketCap": "7B", "Share": "10%"},<br/>
        "Cia. Hering (Grupo Soma)": {"Ticker": "HGTX3.SA", "MarketCap": "3B", "Share": "5%"},<br/>
        "Track & Field Co.": {"Ticker": "TFCO4.SA", "MarketCap": "2B", "Share": "3%"},<br/>
        "Vivara S.A.": {"Ticker": "VIVA3.SA", "MarketCap": "6B", "Share": "8%"},<br/>
        "Riachuelo (Guararapes)": {"Ticker": "GUAR3.SA", "MarketCap": "1B", "Share": "2%"},<br/>
        "C&A Modas S.A.": {"Ticker": "CEAB3.SA", "MarketCap": "1B", "Share": "2%"},<br/>
        "Marisa Lojas S.A.": {"Ticker": "AMAR3.SA", "MarketCap": "0.2B", "Share": "0.5%"},<br/>
        "Dufry AG (Duty Free Brasil)": {"Ticker": "DUFRY.S", "MarketCap": "5B", "Share": "1%"}, # Swiss, but strong presence<br/>
        "Centauro (Grupo SBF)": {"Ticker": "SBFG3.SA", "MarketCap": "3B", "Share": "4%"},<br/>
        "Restoque Comércio e Confecções de Roupas S.A.": {"Ticker": "LLIS3.SA", "MarketCap": "0.5B", "Share": "0.8%"},<br/>
        "Vulcabras Azaleia S.A.": {"Ticker": "VULC3.SA", "MarketCap": "4B", "Share": "6%"},<br/>
        "Grendene S.A.": {"Ticker": "GRND3.SA", "MarketCap": "3B", "Share": "4%"},<br/>
        "Alpargatas S.A.": {"Ticker": "ALPA4.SA", "MarketCap": "2B", "Share": "3%"},<br/>
        "Grupo Hope": {"Ticker": None, "MarketCap": "0.3B", "Share": "0.6%"},<br/>
        "Reserva (Grupo Soma)": {"Ticker": "SOMA3.SA", "MarketCap": "8B", "Share": "1%"}, # Part of Soma<br/>
        "Farm (Grupo Soma)": {"Ticker": "SOMA3.SA", "MarketCap": "8B", "Share": "1%"}, # Part of Soma<br/>
        "Animale (Grupo Soma)": {"Ticker": "SOMA3.SA", "MarketCap": "8B", "Share": "1%"}, # Part of Soma<br/>
        "Le Lis Blanc (Restoque)": {"Ticker": "LLIS3.SA", "MarketCap": "0.5B", "Share": "0.5%"}, # Part of Restoque
    }

    st.subheader("Top 20 Marcas Internacionais de Moda")
    df_global_fashion = pd.DataFrame.from_dict(fashion_brands_global, orient='index')
    df_global_fashion.index.name = "Marca"
    st.dataframe(df_global_fashion.head(20))

    st.markdown("#### Gráficos de Ações (Internacionais)")
    tickers_to_plot_global = [info["Ticker"] for info in fashion_brands_global.values() if info["Ticker"]]
    cols_charts_global = st.columns(min(len(tickers_to_plot_global), 3))
    for i, ticker in enumerate(tickers_to_plot_global):<br/>
        with cols_charts[i % 3]:
            data = get_stock_data(ticker)
            if not data.empty:
                st.plotly_chart(plot_candlestick(data, f"{ticker} - Global"), use_container_width=True)
                support, resistance = calculate_support_resistance(data)
                if support and resistance:<br/>
                    st.markdown(f"**Suporte:** $ {support:.2f} | **Resistência:** $ {resistance:.2f}")<br/>
            else:
                st.warning(f"Dados não disponíveis para {ticker}")

    st.subheader("Top 20 Marcas Brasileiras de Moda")
    df_brazil_fashion = pd.DataFrame.from_dict(fashion_brands_brazil, orient='index')
    df_brazil_fashion.index.name = "Marca"
    st.dataframe(df_brazil_fashion.head(20))

    st.markdown("#### Gráficos de Ações (Brasil)")
    tickers_to_plot_brazil = [info["Ticker"] for info in fashion_brands_brazil.values() if info["Ticker"]]
    cols_charts_brazil = st.columns(min(len(tickers_to_plot_brazil), 3))
    for i, ticker in enumerate(tickers_to_plot_brazil):<br/>
        with cols_charts_brazil[i % 3]:
            data = get_stock_data(ticker)
            if not data.empty:
                st.plotly_chart(plot_candlestick(data, f"{ticker} - Brasil"), use_container_width=True)
                support, resistance = calculate_support_resistance(data)
                if support and resistance:<br/>
                    st.markdown(f"**Suporte:** R$ {support:.2f} | **Resistência:** R$ {resistance:.2f}")<br/>
            else:
                st.warning(f"Dados não disponíveis para {ticker}")

    st.subheader("Market Share Global de Marcas de Luxo (Simulado)")
    market_share_data = {name: float(info["Share"].replace('%', '')) for name, info in fashion_brands_global.items() if info["Share"]}
    market_share_df = pd.Series(market_share_data).sort_values(ascending=False)
    
    # Combine smaller shares into 'Outros' for better visualization
    if len(market_share_df) > 10:<br/>
        other_share = market_share_df.iloc[10:].sum()<br/>
        market_share_df = market_share_df.iloc[:10]
        market_share_df['Outros'] = other_share

    fig_pie = go.Figure(data=[go.Pie(labels=market_share_df.index, values=market_share_df.values, hole=.3)])
    fig_pie.update_layout(
        title='<span style="color:#d4af37">Market Share Global de Marcas de Luxo (Simulado)</span>',
        template="plotly_dark",
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font_color="#E0E0E0",
        legend_title="Marca",
        showlegend=True
    )
    st.plotly_chart(fig_pie, use_container_width=True)

elif selected_module == "SOBERANIA & AGRO":<br/>
    st.title("🌾 SOBERANIA & AGRO: Ativos Estratégicos e Minerais")
    st.markdown("Monitoramento de ativos agrícolas, minerais estratégicos e pedras preciosas, com dados de mercado e tendências.")

    st.subheader("Mercado AGRO (Brasil)")
    agro_tickers = {
        "Soja Futuros": "ZS=F", # Futuros de Soja<br/>
        "Milho Futuros": "ZC=F", # Futuros de Milho<br/>
        "Açúcar Futuros": "SB=F", # Futuros de Açúcar<br/>
        "Boi Gordo Futuros": "BGI=F", # Futuros de Boi Gordo (simulado, ticker pode variar)<br/>
        "SLC Agrícola": "SLCE3.SA",<br/>
        "BrasilAgro": "AGRO3.SA",
    }

    cols_agro = st.columns(3)
    for i, (name, ticker) in enumerate(agro_tickers.items()):<br/>
        with cols_agro[i % 3]:
            st.markdown(f"#### {name}")
            data = get_stock_data(ticker, period='6mo')
            if not data.empty:
                st.plotly_chart(plot_candlestick(data, name), use_container_width=True)
                support, resistance = calculate_support_resistance(data)
                if support and resistance:<br/>
                    st.markdown(f"**Suporte:** R$ {support:.2f} | **Resistência:** R$ {resistance:.2f}")<br/>
            else:
                st.warning(f"Dados não disponíveis para {name} ({ticker})")

    st.subheader("Minerais Estratégicos")
    mineral_data = {
        "Nióbio": {"Price": random.uniform(40, 60), "Unit": "USD/kg", "Change": random.uniform(-1, 1)},<br/>
        "Grafeno": {"Price": random.uniform(100, 500), "Unit": "USD/g", "Change": random.uniform(-5, 5)},<br/>
        "Prata": {"Price": yf.Ticker("SI=F").history(period='1d')['Close'].iloc[-1] if not yf.Ticker("SI=F").history(period='1d').empty else random.uniform(20, 30), "Unit": "USD/oz", "Change": random.uniform(-0.5, 0.5)},<br/>
        "Cobre": {"Price": yf.Ticker("HG=F").history(period='1d')['Close'].iloc[-1] if not yf.Ticker("HG=F").history(period='1d').empty else random.uniform(4, 5), "Unit": "USD/lb", "Change": random.uniform(-0.1, 0.1)},
    }

    df_minerals = pd.DataFrame.from_dict(mineral_data, orient='index')
    df_minerals['Change'] = df_minerals['Change'].apply(lambda x: f"{x:.2f}%" if x >= 0 else f"{x:.2f}%")<br/>
    st.dataframe(df_minerals.style.format({"Price": "{:.2f}"}))

    st.markdown("#### Gráficos de Variação de Minerais")
    cols_minerals = st.columns(2)
    for i, (mineral, data) in enumerate(mineral_data.items()):<br/>
        with cols_minerals[i % 2]:<br/>
            if mineral in ["Prata", "Cobre"]:
                ticker = "SI=F" if mineral == "Prata" else "HG=F"
                df_hist = get_stock_data(ticker, period='6mo')
                if not df_hist.empty:
                    st.plotly_chart(plot_candlestick(df_hist, mineral), use_container_width=True)
                    support, resistance = calculate_support_resistance(df_hist)
                    if support and resistance:<br/>
                        st.markdown(f"**Suporte:** $ {support:.2f} | **Resistência:** $ {resistance:.2f}")<br/>
                else:
                    st.warning(f"Dados históricos não disponíveis para {mineral}")
            else: # Nióbio, Grafeno (simulado)
                df_sim = generate_simulated_data(mineral, days=180)
                st.plotly_chart(plot_candlestick(df_sim, mineral + " (Simulado)"), use_container_width=True)
                support, resistance = calculate_support_resistance(df_sim)
                if support and resistance:<br/>
                    st.markdown(f"**Suporte:** $ {support:.2f} | **Resistência:** $ {resistance:.2f}")

    st.subheader("Pedras Preciosas")
    precious_stones = {
        "Diamante (1 quilate)": {"Price": random.uniform(5000, 15000), "Change": random.uniform(-0.5, 0.5)},<br/>
        "Esmeralda (1 quilate)": {"Price": random.uniform(1000, 8000), "Change": random.uniform(-0.3, 0.3)},<br/>
        "Rubi (1 quilate)": {"Price": random.uniform(2000, 10000), "Change": random.uniform(-0.4, 0.4)},<br/>
        "Safira (1 quilate)": {"Price": random.uniform(800, 6000), "Change": random.uniform(-0.2, 0.2)},<br/>
        "Alexandrita (1 quilate)": {"Price": random.uniform(10000, 25000), "Change": random.uniform(-0.8, 0.8)},
    }
    df_stones = pd.DataFrame.from_dict(precious_stones, orient='index')
    df_stones['Change'] = df_stones['Change'].apply(lambda x: f"{x:.2f}%" if x >= 0 else f"{x:.2f}%")<br/>
    st.dataframe(df_stones.style.format({"Price": "R$ {:.2f}"}))

elif selected_module == "IA QUÂNTICO TESLA":<br/>
    st.title("🧠 IA QUÂNTICO TESLA: Previsões de Loterias")
    st.markdown("Gerador de números para loterias com base em um algoritmo 'quântico-inspirado', utilizando frequências vórtex para máxima previsibilidade (simulada).")

    st.warning("⚠️ **Disclaimer:** Este gerador de números é para fins de entretenimento e exploração de conceitos. Loterias são jogos de azar e não há garantia de acerto. Jogue com responsabilidade.")

    # Frequências Vórtex (usadas como sementes ou modificadores)
    vortex_frequencies = [369, 432, 528, 963]

    def generate_quantum_numbers(count, min_num, max_num, frequencies):
        """Gera números 'quânticos' usando frequências vórtex como sementes/modificadores."""
        numbers = set()
        seed_modifier = sum(frequencies) % 1000 # Combina as frequências
        
        while len(numbers) < count:
            # Combina o tempo atual com as frequências e um fator aleatório
            current_time_seed = int(datetime.now().timestamp() * 1000) % 1000000
            random.seed(current_time_seed + seed_modifier + random.randint(1, 1000))
            
            num = random.randint(min_num, max_num)
            
            # Pequena "perturbação quântica" baseada nas frequências
            for freq in frequencies:<br/>
                if num % freq == 0:
                    num = (num + random.randint(-5, 5)) % (max_num - min_num + 1) + min_num
            
            numbers.add(num)
        return sorted(list(numbers))

    st.subheader("Mega-Sena (6 números de 1 a 60)")
    if st.button("Gerar Previsão Mega-Sena", key="mega_sena_btn"):
        mega_sena_numbers = generate_quantum_numbers(6, 1, 60, vortex_frequencies)
        st.success(f"**Números Quânticos Mega-Sena:** {', '.join(map(str, mega_sena_numbers))}")<br/>
        if "mega_sena_history" not in st.session_state:
            st.session_state.mega_sena_history = []
        st.session_state.mega_sena_history.append(f"{datetime.now().strftime('%H:%M:%S')}: {', '.join(map(str, mega_sena_numbers))}")

    if "mega_sena_history" in st.session_state and st.session_state.mega_sena_history:<br/>
        with st.expander("Histórico de Previsões Mega-Sena"):<br/>
            for entry in reversed(st.session_state.mega_sena_history):
                st.write(entry)

    st.subheader("Lotofácil (15 números de 1 a 25)")
    if st.button("Gerar Previsão Lotofácil", key="lotofacil_btn"):
        lotofacil_numbers = generate_quantum_numbers(15, 1, 25, vortex_frequencies)
        st.success(f"**Números Quânticos Lotofácil:** {', '.join(map(str, lotofacil_numbers))}")<br/>
        if "lotofacil_history" not in st.session_state:
            st.session_state.lotofacil_history = []
        st.session_state.lotofacil_history.append(f"{datetime.now().strftime('%H:%M:%S')}: {', '.join(map(str, lotofacil_numbers))}")

    if "lotofacil_history" in st.session_state and st.session_state.lotofacil_history:<br/>
        with st.expander("Histórico de Previsões Lotofácil"):<br/>
            for entry in reversed(st.session_state.lotofacil_history):
                st.write(entry)

    st.subheader("Lotomania (20 números de 0 a 99)")
    if st.button("Gerar Previsão Lotomania", key="lotomania_btn"):
        lotomania_numbers = generate_quantum_numbers(20, 0, 99, vortex_frequencies)
        st.success(f"**Números Quânticos Lotomania:** {', '.join(map(str, lotomania_numbers))}")<br/>
        if "lotomania_history" not in st.session_state:
            st.session_state.lotomania_history = []
        st.session_state.lotomania_history.append(f"{datetime.now().strftime('%H:%M:%S')}: {', '.join(map(str, lotomania_numbers))}")

    if "lotomania_history" in st.session_state and st.session_state.lotomania_history:<br/>
        with st.expander("Histórico de Previsões Lotomania"):<br/>
            for entry in reversed(st.session_state.lotomania_history):
                st.write(entry)

    st.markdown("---")
    st.markdown("#### Análise de Padrões Quânticos (Simulado)")
    st.info("O algoritmo utiliza uma combinação de sementes baseadas em tempo e frequências vórtex para gerar sequências que, embora aleatórias, buscam uma 'ressonância' com padrões energéticos. A 'previsibilidade' é uma interpretação da complexidade e interconexão dos eventos, não uma garantia matemática.")
    
    # Gráfico de distribuição de números gerados (simulado)
    if "all_generated_numbers" not in st.session_state:
        st.session_state.all_generated_numbers = []
    
    if st.session_state.mega_sena_history or st.session_state.lotofacil_history or st.session_state.lotomania_history:
        all_numbers = []
        for hist in [st.session_state.mega_sena_history, st.session_state.lotofacil_history, st.session_state.lotomania_history]:<br/>
            for entry in hist:<br/>
                nums_str = entry.split(': ')[1]
                all_numbers.extend([int(n) for n in nums_str.split(', ')])
        
        if all_numbers:
            fig_dist = go.Figure(data=[go.Histogram(x=all_numbers, marker_color='#d4af37')])
            fig_dist.update_layout(
                title='<span style="color:#d4af37">Distribuição dos Números Gerados (Simulado)</span>',
                template="plotly_dark",
                paper_bgcolor="#000000",
                plot_bgcolor="#000000",
                font_color="#E0E0E0",
                xaxis_title="Número",
                yaxis_title="Frequência",
                bargap=0.1
            )
            st.plotly_chart(fig_dist, use_container_width=True)

elif selected_module == "DEVOCIONAL COM DEUS":<br/>
    st.title("🙏 DEVOCIONAL COM DEUS: Reflexão e Inspiração")
    st.markdown("Um momento de pausa e conexão espiritual, com versículos bíblicos e explicações profundas que tocam a alma.")

    devotionals = [
        {
            "verse": "Filipenses 4:6-7",<br/>
            "text": "Não andeis ansiosos por coisa alguma; antes em tudo sejam os vossos pedidos conhecidos diante de Deus pela oração e súplica com ações de graças; e a paz de Deus, que excede todo o entendimento, guardará os vossos corações e os vossos sentimentos em Cristo Jesus.",<br/>
            "explanation": """<br/>
            Neste mundo de incertezas e desafios, a ansiedade pode ser um fardo pesado. Mas a Palavra de Deus nos convida a um caminho de **liberdade e paz**. Filipenses 4:6-7 não é apenas um conselho, é uma **promessa divina**.

            Imagine entregar cada preocupação, cada medo, cada anseio diretamente nas mãos do Criador do universo. Não é um ato de passividade, mas de **confiança radical**. É reconhecer que há um poder maior que cuida de você, que conhece suas necessidades antes mesmo de você as expressar.

            Quando oramos com gratidão, mudamos nossa perspectiva. Em vez de focar no que falta, lembramos do que já temos e do que Deus já fez. Essa atitude abre as portas para uma **paz que desafia a lógica humana**. Uma paz que não depende das circunstâncias externas, mas que reside no mais profundo do seu ser, guardada pelo próprio Espírito de Deus.

            Permita que essa paz inunde seu coração hoje. Deixe que ela acalme suas tempestades internas e traga clareza à sua mente. Você não está sozinho. Deus está com você, e Ele deseja que você viva em Sua perfeita paz.
            """,
            "context": "A carta de Paulo aos Filipenses é conhecida como a 'epístola da alegria', escrita enquanto ele estava preso. Mesmo em circunstâncias difíceis, Paulo exorta os crentes a encontrarem alegria e paz em Cristo, independentemente das adversidades.",<br/>
            "application": "Hoje, reserve um momento para listar suas preocupações e, em seguida, entregue-as a Deus em oração, agradecendo por Sua fidelidade. Observe como a paz começa a preencher o espaço da ansiedade."
        },
        {
            "verse": "Salmos 23:1",<br/>
            "text": "O Senhor é o meu pastor; nada me faltará.",<br/>
            "explanation": """
            Que declaração poderosa e reconfortante! "O Senhor é o meu pastor; nada me faltará." Em um mundo onde a escassez e a incerteza parecem dominar, esta verdade bíblica é um **oásis para a alma**.

            Pense na figura do pastor. Ele guia, protege, alimenta e cuida de suas ovelhas com uma dedicação inabalável. Ele conhece cada uma pelo nome, sabe de suas necessidades e as conduz a pastos verdejantes e águas tranquilas. Da mesma forma, Deus, o nosso Pastor, está ativamente envolvido em cada detalhe da nossa vida.

            Quando você se sente perdido, Ele é o seu guia. Quando a fome espiritual ou emocional aperta, Ele é o seu sustento. Quando o perigo se aproxima, Ele é o seu refúgio. A promessa "nada me faltará" não significa ausência de desafios, mas a **garantia da provisão divina** em meio a eles. Significa que, em Cristo, você tem tudo o que realmente precisa para viver uma vida plena e com propósito.

            Deixe que essa verdade penetre em seu coração hoje. Confie no seu Pastor. Ele é fiel, Ele é bom, e Ele nunca o abandonará.
            """,
            "context": "O Salmo 23 é um dos mais conhecidos e amados salmos, atribuído ao Rei Davi. Ele descreve a confiança inabalável do salmista na provisão e proteção de Deus, usando a metáfora do pastor e suas ovelhas.",<br/>
            "application": "Reflita sobre as áreas da sua vida onde você sente falta de algo. Entregue essas preocupações ao seu Pastor e confie que Ele suprirá todas as suas necessidades, conforme a Sua vontade."
        },
        {
            "verse": "João 14:27",<br/>
            "text": "Deixo-vos a paz, a minha paz vos dou; não vo-la dou como o mundo a dá. Não se turbe o vosso coração, nem se atemorize.",<br/>
            "explanation": """<br/>
            Em um mundo que busca a paz em conquistas, bens ou ausência de conflitos, Jesus nos oferece algo radicalmente diferente: **Sua própria paz**. A paz que o mundo oferece é superficial e passageira, dependente de circunstâncias favoráveis. Mas a paz de Cristo é **profunda, duradoura e inabalável**.

            Ele nos diz: "Não se turbe o vosso coração, nem se atemorize." Que convite à serenidade! Em meio às tempestades da vida, às incertezas do futuro, aos medos que tentam nos paralisar, a voz de Jesus ecoa, trazendo calma. Sua paz não é a ausência de problemas, mas a **presença de Deus** no meio deles. É a certeza de que, não importa o que aconteça, você está seguro em Suas mãos.

            Essa paz é um presente divino, um legado de amor. Ela nos capacita a enfrentar as adversidades com coragem, a perdoar com graça e a amar sem reservas. Ela nos liberta da escravidão da preocupação e nos convida a viver com uma confiança que transcende todo entendimento.

            Receba hoje a paz de Jesus. Deixe que ela acalme cada turbulência em seu coração e dissipe todo temor. Ele é a sua paz.
            """,
            "context": "Estas palavras foram ditas por Jesus aos seus discípulos durante a Última Ceia, pouco antes de sua crucificação. Ele estava preparando-os para a sua partida, mas lhes assegurava que não os deixaria desamparados, oferecendo-lhes a Sua paz e o Espírito Santo.",<br/>
            "application": "Quando sentir seu coração turbado ou atemorizado, feche os olhos e lembre-se das palavras de Jesus. Peça a Ele que inunde seu coração com a Sua paz, que excede todo o entendimento."
        }
    ]

    if "devotional_index" not in st.session_state:
        st.session_state.devotional_index = 0
    if "devotional_history" not in st.session_state:
        st.session_state.devotional_history = []

    current_devotional = devotionals[st.session_state.devotional_index % len(devotionals)]

    st.markdown(f"## <span style='color:#d4af37'>{current_devotional['verse']}</span>", unsafe_allow_html=True)
    st.markdown(f"### *\"{current_devotional['text']}\"*")
    st.markdown("---")

    st.markdown("#### ✨ Explicação Profunda")
    st.markdown(current_devotional['explanation'])

    st.markdown("---")
    st.markdown("#### 📖 Contexto Bíblico")
    st.info(current_devotional['context'])

    st.markdown("#### 💡 Aplicação Prática")
    st.success(current_devotional['application'])

    if st.button("Novo Versículo Inspirador", key="new_devotional_btn"):
        st.session_state.devotional_history.append(current_devotional['verse'])
        st.session_state.devotional_index += 1
        st.rerun()

    if st.session_state.devotional_history:<br/>
        with st.expander("Histórico de Versículos"):<br/>
            for verse in reversed(st.session_state.devotional_history):
                st.write(verse)

# 
# 6. FOOTER DO SISTEMA
# 
st.markdown("---")
st.markdown(
    f"""
    <div style="text-align: center; color: #555555; font-size: 0.8em;"><br/>
        Quantum Nexus Elite Terminal | Desenvolvido com 💖 e IA | Última Atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    """,
    unsafe_allow_html=True
)
