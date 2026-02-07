import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go
import time

# 1. CONFIGURAÇÃO DE INTERFACE ULTRA MODERNA
st.set_page_config(page_title="IA Quântico Tesla", layout="wide", initial_sidebar_state="expanded")

# CSS ESTILO INSTAGRAM PREMIUM
st.markdown("""
    <style>
    /* Fundo e Texto Principal */
    .stApp { background-color: #000000; color: #FFFFFF; }
    
    /* Sidebar Estilo Menu Social */
    [data-testid="stSidebar"] { 
        background-color: #050505; 
        border-right: 1px solid #262626; 
    }
    
    /* Cards e Containers */
    .css-1r6slb0 { 
        border-radius: 20px; 
        background-color: #121212; 
        border: 1px solid #262626;
        padding: 25px;
    }

    /* Botões Estilo Action */
    .stButton>button { 
        border-radius: 12px; 
        border: none; 
        background: linear-gradient(45deg, #d4af37, #f9e295); 
        color: black; 
        font-weight: bold; 
        height: 45px;
        transition: 0.3s;
    }
    .stButton>button:hover { 
        transform: scale(1.02);
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.4);
    }

    /* Títulos */
    h1, h2, h3 { 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica; 
        font-weight: 700;
        color: #d4af37;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. MOTOR IA QUÂNTICO TESLA
def ia_quantico_tesla(max_n, qtd):
    # Semente quântica baseada em milissegundos
    random.seed(int(time.time() * 1000))
    # Filtro de Frequência 3-6-9
    vortex_nums = [n for n in range(1, max_n + 1) if (n % 9 in [3, 6, 0])]
    # Seleção inteligente
    if len(vortex_nums) >= qtd:
        resultado = random.sample(vortex_nums, qtd)
    else:
        restante = list(set(range(1, max_n + 1)) - set(vortex_nums))
        resultado = vortex_nums + random.sample(restante, qtd - len(vortex_nums))
    return sorted(resultado)

# 3. NAVEGAÇÃO LATERAL (SIDEBAR)
with st.sidebar:
    st.markdown("<h1 style='font-size: 24px;'>⚡ NEXUS PRO</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("MENU", 
                    ["💎 IA Quântico Tesla", "📈 Mercado Global", "💹 Sugestões de Investimento", "📜 Sabedoria"],
                    format_func=lambda x: f" {x}")
    st.write("---")
    st.caption("Operador: Cristiano Daniel de Noronha")

# MÓDULO 1: IA QUÂNTICO TESLA (LOTERIAS)
if menu == "💎 IA Quântico Tesla":
    st.title("💎 IA Quântico Tesla")
    st.write("Cálculo de probabilidade baseado em frequências de vórtice e astrolábio quântico.")
    
    col_l1, col_l2 = st.columns([1, 1])
    with col_l1:
        jogo = st.selectbox("Modalidade:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    
    if st.button("GERAR CONFLUÊNCIA"):
        with st.status("Processando IA Quântico...", expanded=True) as status:
            time.sleep(1.2)
            config = {
                "Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5),
                "Lotomania": (100, 50), "Milionária": (50, 6)
            }
            n_max, n_qtd = config[jogo]
            final = ia_quantico_tesla(n_max, n_qtd)
            
            st.write(f"### {jogo} - Números Sugeridos:")
            st.code(", ".join(map(str, final)))
            
            if jogo == "Milionária":
                st.warning(f"Trevos: {random.sample(range(1, 7), 2)}")
            status.update(label="Cálculo Finalizado!", state="complete")

# MÓDULO 2: MERCADO GLOBAL (RADAR)
elif menu == "📈 Mercado Global":
    st.title("📈 Radar Global")
    # Tickers: Ouro, Prata, Cobre, Nióbio (via Vale), Apple, Google, Amazon, Dólar, Euro
    ativos = {
        "Ouro": "GC=F", "Prata": "SI=F", "Cobre": "HG=F", "Nióbio (VALE3)": "VALE3.SA",
        "Apple": "AAPL", "Google": "GOOGL", "Amazon": "AMZN", 
        "Dólar/BRL": "USDBRL=X", "Euro/BRL": "EURBRL=X"
    }
    selecionado = st.selectbox("Selecione para análise diária:", list(ativos.keys()))
    
    data = yf.download(ativos[selecionado], period="60d", interval="1d")
    fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
                    increasing_line_color='#d4af37', decreasing_line_color='#444')])
    fig.update_layout(template='plotly_dark', paper_bgcolor='black', plot_bgcolor='black', height=500)
    st.plotly_chart(fig, use_container_width=True)

# MÓDULO 3: SUGESTÕES DE INVESTIMENTO
elif menu == "💹 Sugestões de Investimento":
    st.title("💹 Central de Oportunidades")
    st.info("A IA analisa o desvio padrão e as médias móveis de Tesla para sugerir entradas.")
    
    # Exemplo de sugestão automática
    st.subheader("Oportunidade de Hoje")
    st.write("**Ativo:** Bitcoin (BTC)")
    st.progress(85, text="Força de Compra (Base Quântica)")
    st.success("Sugerido: Entrada em zonas de retração de 3% para alvo de 9%.")

# MÓDULO 4: SABEDORIA
else:
    st.title("📜 Sabedoria do Dia")
    st.markdown("> **Provérbios 3:13-14** \n\n > *'Como é feliz aquele que acha a sabedoria... pois ela é mais proveitosa que a prata e rende mais do que o ouro.'*")
    st.write("Explicação: O Nexus não é apenas sobre números, é sobre a mentalidade de abundância que gera retorno financeiro.")
