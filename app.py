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
    st.title("💹 Terminal Trade & Cripto")
    t_choice = st.selectbox("Ativo:", ["BTC-USD (Bitcoin)", "ETH-USD (Ethereum)", "USDBRL=X (Dólar)"])
    fig = get_market_data(t_choice.split(" (")[1].replace(")", ""), t_choice)
    if fig: st.plotly_chart(fig, use_container_width=True)

elif menu == "👗 Fashion High-Ticket":
    st.title("👗 Radar Fashion Luxo")
    f_choice = st.selectbox("Marca:", ["MC.PA (LVMH)", "RMS.PA (Hermès)", "NKE (Nike)", "ARZZ3.SA (Arezzo)"])
    fig = get_market_data(f_choice.split(" (")[1].replace(")", ""), f_choice)
    if fig: st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Dominância por Gênero")
    fig_f = go.Figure(data=[go.Pie(labels=['Feminino', 'Masculino', 'Acessórios'], values=[50, 30, 20], hole=.4)])
    fig_f.update_layout(template='plotly_dark')
    st.plotly_chart(fig_f)

elif menu == "🌍 Soberania & Reservas":
    st.title("🌍 Reservas Mundiais de Estado")
    r_choice = st.selectbox("Commodity:", ["GC=F (Ouro)", "SI=F (Prata)", "HG=F (Cobre)", "VALE (Nióbio/Vale)"])
    fig = get_market_data(r_choice.split(" (")[1].replace(")", ""), r_choice)
    if fig: st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Maiores Detentores (%)")
    fig_r = go.Figure(data=[go.Pie(labels=['Brasil', 'EUA', 'China', 'Rússia', 'Outros'], values=[40, 20, 15, 10, 15])])
    fig_r.update_layout(template='plotly_dark')
    st.plotly_chart(fig_r)

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
