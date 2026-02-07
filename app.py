import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import random
import time

# --- CONFIGURAÇÃO DE INTERFACE ELITE ---
st.set_page_config(page_title="Tesla Quantum Nexus", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #d4af37; }
    [data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #d4af37; }
    .stButton>button { 
        border-radius: 10px; border: 1px solid #d4af37; background: #d4af37; color: black; 
        font-weight: bold; width: 100%; height: 45px; transition: 0.3s;
    }
    .stButton>button:hover { background: #f9e295; box-shadow: 0px 0px 15px #d4af37; }
    .card { border-radius: 15px; background: #111; padding: 20px; border: 1px solid #222; margin-bottom: 15px; }
    h1, h2, h3 { color: #d4af37; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE GRÁFICO PROFISSIONAL ---
def render_terminal(ticker, label):
    try:
        data = yf.download(ticker, period="60d", interval="1d", progress=False)
        if not data.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
                increasing_line_color='#d4af37', decreasing_line_color='#ff4b4b'
            )])
            fig.update_layout(template='plotly_dark', paper_bgcolor='black', plot_bgcolor='black', height=400, margin=dict(l=0,r=0,t=30,b=0))
            st.plotly_chart(fig, use_container_width=True)
        else: st.warning(f"Dados de {label} indisponíveis no momento.")
    except: st.error(f"Erro ao conectar com a Bolsa para {label}")

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚡ NEXUS TERMINAL")
    menu = st.radio("SELECIONE O SISTEMA:", 
                    ["Loterias Tesla", "Mercado Pet", "Trade & Cripto", "Fashion Luxo", "Soberania & Reservas", "Devocional"])
    st.write("---")
    st.write("Operador: Cristiano Noronha")

# --- MÓDULO 1: LOTERIAS ---
if menu == "Loterias Tesla":
    st.title("💎 IA Quântico Tesla")
    jogo = st.selectbox("Modalidade:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    if st.button("GERAR CONFLUÊNCIA 3-6-9"):
        with st.status("Calculando Vórtice..."):
            time.sleep(1)
            config = {"Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5), "Lotomania": (100, 50), "Milionária": (50, 6)}
            n_max, n_qtd = config[jogo]
            res = sorted(random.sample([n for n in range(1, n_max+1) if n%3==0 or n%9==0], n_qtd))
            st.markdown(f"<div class='card'><h1>{', '.join(map(str, res))}</h1></div>", unsafe_allow_html=True)

# --- MÓDULO 2: MERCADO PET ---
elif menu == "Mercado Pet":
    st.title("🐾 Pet Intelligence Global")
    pet_t = st.selectbox("Ativo Pet:", ["PETZ3.SA (Petz)", "ZTS (Zoetis)", "CHWY (Chewy)"])
    render_terminal(pet_t.split(" (")[1].replace(")", ""), pet_t)
    
    st.subheader("Dominância de Mercado (Market Share)")
    fig_pet = go.Figure(data=[go.Pie(labels=['Mars', 'Purina', 'Zoetis', 'Outros'], values=[35, 25, 15, 25], hole=.4)])
    fig_pet.update_layout(template='plotly_dark')
    st.plotly_chart(fig_pet)

# --- MÓDULO 3: TRADE ---
elif menu == "Trade & Cripto":
    st.title("💹 Terminal de Trading")
    t_choice = st.selectbox("Ativo:", ["BTC-USD", "ETH-USD", "USDBRL=X"])
    render_terminal(t_choice, t_choice)

# --- MÓDULO 4: FASHION ---
elif menu == "Fashion Luxo":
    st.title("👗 Radar Fashion High-Ticket")
    f_choice = st.selectbox("Marca:", ["MC.PA (LVMH)", "RMS.PA (Hermès)", "NKE (Nike)", "ARZZ3.SA (Arezzo)"])
    render_terminal(f_choice.split(" (")[1].replace(")", ""), f_choice)
    
    st.subheader("Consumo por Categoria (%)")
    fig_f = go.Figure(data=[go.Pie(labels=['Feminino', 'Masculino', 'Acessórios'], values=[50, 30, 20], hole=.4)])
    fig_f.update_layout(template='plotly_dark')
    st.plotly_chart(fig_f)

# --- MÓDULO 5: RESERVAS ---
elif menu == "Soberania & Reservas":
    st.title("🌍 Soberania e Reservas de Estado")
    r_choice = st.selectbox("Commodity:", ["GC=F (Ouro)", "SI=F (Prata)", "BZ=F (Petróleo)", "VALE (Nióbio)"])
    render_terminal(r_choice.split(" (")[1].replace(")", ""), r_choice)
    
    st.subheader("Maiores Reservas por País (%)")
    fig_r = go.Figure(data=[go.Pie(labels=['Brasil', 'EUA', 'China', 'Rússia', 'Outros'], values=[40, 20, 15, 10, 15], hole=.4)])
    fig_r.update_layout(template='plotly_dark')
    st.plotly_chart(fig_r)

# --- MÓDULO 6: DEVOCIONAL ---
elif menu == "Devocional":
    st.title("🙏 Sabedoria e Propósito")
    st.markdown("""
    <div class='card'>
        <p align='center'><i>"Honre ao Senhor com todos os seus recursos..." (Provérbios 3:9)</i></p>
        <hr>
        <p>Cristiano, a verdadeira riqueza é aquela que edifica. Use a inteligência que Deus lhe deu para dominar o mercado, 
        mas mantenha o coração Nele. Que sua jornada seja guiada pela paz e pela clareza.</p>
    </div>
    """, unsafe_allow_html=True)
