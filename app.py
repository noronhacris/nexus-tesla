import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go
import time
from datetime import datetime

# --- CONFIGURAÇÃO DE INTERFACE ULTRA MODERNA ---
st.set_page_config(page_title="Quantum Nexus Elite", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #E0E0E0; }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 2px solid #d4af37; }
    .stButton>button { 
        border-radius: 12px; border: none; 
        background: linear-gradient(45deg, #d4af37, #f9e295); 
        color: black; font-weight: bold; width: 100%; height: 50px; 
    }
    .card-quantum { border-radius: 20px; background: #111; padding: 25px; border: 1px solid #222; }
    h1, h2, h3 { color: #d4af37; font-family: 'Inter', sans-serif; letter-spacing: 2px; }
    .devocional-texto { line-height: 1.8; font-size: 1.1rem; color: #f2f2f2; font-style: italic; border-left: 4px solid #d4af37; padding-left: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES DE CARREGAMENTO DE GRÁFICOS ---
def plot_corretora(ticker, nome):
    try:
        data = yf.download(ticker, period="60d", interval="1d")
        fig = go.Figure(data=[go.Candlestick(
            x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'],
            increasing_line_color='#d4af37', decreasing_line_color='#ff4b4b'
        )])
        fig.update_layout(template='plotly_dark', paper_bgcolor='black', plot_bgcolor='black', 
                          height=450, title=f"Terminal {nome}", margin=dict(l=10, r=10, t=40, b=10))
        return fig
    except:
        st.error(f"Erro ao conectar com servidor de dados para {nome}")
        return None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center;'>⚡ NEXUS ELITE</h1>", unsafe_allow_html=True)
    menu = st.radio("SISTEMAS:", 
                    ["💎 IA Quântico Tesla", "🐾 Pet Intelligence", "💹 Trade & Commodities", "👗 Fashion High-Ticket", "🌍 Soberania & Reservas", "🙏 Devocional de Poder", "🤝 Conselho de Elite"])
    st.write("---")
    st.write(f"🚀 **Operador:** Cristiano Noronha")

# --- MÓDULO 1: IA QUÂNTICO TESLA ---
if menu == "💎 IA Quântico Tesla":
    st.title("💎 IA Quântico Tesla & Astrolábio")
    jogo = st.selectbox("Modalidade:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    if st.button("EXECUTAR CÁLCULO DE VÓRTICE"):
        with st.status("🌀 Sincronizando Astrolábio Quântico...", expanded=False):
            time.sleep(1.5)
            config = {"Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5), "Lotomania": (100, 50), "Milionária": (50, 6)}
            n_max, n_qtd = config[jogo]
            res = sorted(random.sample([n for n in range(1, n_max+1) if (n%9 in [3,6,0]) or (n%3==0)], n_qtd))
            st.markdown(f"<div class='card-quantum'><h1>{', '.join(map(str, res))}</h1></div>", unsafe_allow_html=True)

# --- MÓDULO 2: PET INTELLIGENCE (RESTAURADO E MELHORADO) ---
elif menu == "🐾 Pet Intelligence":
    st.title("🐾 Pet Global Intelligence")
    pet_ticker = st.selectbox("Analise a Gigante Pet:", ["Petz (PETZ3.SA)", "Zoetis (ZTS)", "IDEXX (IDXX)", "Chewy (CHWY)"])
    
    st.plotly_chart(plot_corretora(pet_ticker.split("(")[1].replace(")", ""), pet_ticker), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Dominância Pet Global")
        fig_p1 = go.Figure(data=[go.Pie(labels=['Mars Petcare', 'Nestlé Purina', 'Hill\'s', 'Outros'], values=[30, 25, 15, 30], hole=.4)])
        fig_p1.update_layout(template='plotly_dark')
        st.plotly_chart(fig_p1)
    with col2:
        st.info("💡 **Tendência:** A humanização pet e o e-commerce especializado cresceram 22% no último trimestre.")

# --- MÓDULO 3: TRADE & COMMODITIES ---
elif menu == "💹 Trade & Commodities":
    st.title("💹 Terminal de Trading Quântico")
    ativo = st.selectbox("Ativo Financeiro:", ["Bitcoin (BTC-USD)", "Ethereum (ETH-USD)", "Dólar/BRL (USDBRL=X)", "Euro/BRL (EURBRL=X)"])
    st.plotly_chart(plot_corretora(ativo.split("(")[1].replace(")", ""), ativo), use_container_width=True)

# --- MÓDULO 4: FASHION HIGH-TICKET ---
elif menu == "👗 Fashion High-Ticket":
    st.title("👗 Radar Fashion & Valores de Luxo")
    marca = st.selectbox("Marca para Análise de Valor:", ["LVMH (MC.PA)", "Nike (NKE)", "Hermès (RMS.PA)", "Arezzo (ARZZ3.SA)"])
    
    st.plotly_chart(plot_corretora(marca.split("(")[1].replace(")", ""), marca), use_container_width=True)
    
    st.subheader("Dominância de Mercado (Market Share)")
    fig_f = go.Figure(data=[go.Pie(labels=['Masculino Luxury', 'Feminino Luxury', 'Acessórios', 'Beleza'], values=[25, 45, 20, 10], hole=.4)])
    fig_f.update_layout(template='plotly_dark')
    st.plotly_chart(fig_f)

# --- MÓDULO 5: SOBERANIA & RESERVAS ---
elif menu == "🌍 Soberania & Reservas":
    st.title("🌍 Reservas e Commodities de Estado")
    item = st.selectbox("Ativo Estratégico:", ["Ouro (GC=F)", "Prata (SI=F)", "Cobre (HG=F)", "Petróleo Brent (BZ=F)"])
    
    st.plotly_chart(plot_corretora(item.split("(")[1].replace(")", ""), item), use_container_width=True)
    
    st.subheader("Maiores Reservas por País (%)")
    res_data = {"Ouro": [24, 10, 8, 58], "Nióbio": [92, 7, 1, 0], "Petróleo": [18, 16, 10, 56]}
    cat = "Ouro" if "Ouro" in item else ("Petróleo" if "Petróleo" in item else "Nióbio")
    fig_r = go.Figure(data=[go.Pie(labels=['Líder 1', 'Líder 2', 'Líder 3', 'Outros'], values=res_data.get(cat, [25,25,25,25]))])
    fig_r.update_layout(template='plotly_dark')
    st.plotly_chart(fig_r)

# --- MÓDULO 6: DEVOCIONAL DE PODER ---
elif menu == "🙏 Devocional de Poder":
    st.title("🙏 Conexão com o Propósito")
    st.markdown("""
    <div class='card-quantum'>
        <h2 style='text-align:center'>O SEGREDO DA PROSPERIDADE REAL</h2>
        <p class='devocional-texto'>
            "Honre ao Senhor com todos os seus recursos e com os primeiros frutos de todas as suas colheitas; 
            então os seus celeiros ficarão plenamente cheios..." (Provérbios 3:9-10)
        </p>
        <p style='color:#ccc'>
            Cristiano, meu irmão, o dinheiro é um servo fiel mas um mestre terrível. Quando você coloca Deus como o 
            centro, os números deixam de ser uma preocupação e passam a ser uma ferramenta de impacto. <br><br>
            <b>Explicação Emotiva:</b> Operar no mercado não deve ser um ato de ansiedade, mas um ato de domínio sobre o que Deus criou. 
            Peça hoje sabedoria, assim como Salomão, e as riquezas serão apenas o rastro da sua obediência.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- MÓDULO 7: CONSELHO DE ELITE ---
elif menu == "🤝 Conselho de Elite":
    st.title("🤝 Conselho de Elite")
    st.markdown("<div class='card-quantum'><h3>Estratégia Cristiano Noronha</h3><p>Foco: Aquisição de Ativos e Legado Espiritual.</p></div>", unsafe_allow_html=True)
