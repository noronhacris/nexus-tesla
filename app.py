
import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go
import time
import pandas as pd
from datetime import datetime

# =================================================================
# 1. CONFIGURAÇÃO DE ALTA PERFORMANCE
# =================================================================
st.set_page_config(page_title="Quantum Nexus Elite", layout="wide", initial_sidebar_state="expanded")

# =================================================================
# 2. ESTILO VISUAL (CSS INTEGRAL - SEM CORTES)
# =================================================================
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #050505; border-right: 2px solid #d4af37; }
    h1, h2, h3 { color: #d4af37; font-family: 'JetBrains Mono'; letter-spacing: 2px; }
    .stButton>button { 
        border-radius: 10px; border: 1px solid #d4af37; background: #1a1a1a; color: #d4af37;
        font-weight: bold; width: 100%; height: 50px;
    }
    .stButton>button:hover { background: #d4af37; color: #000; }
    .card-quantum { border-radius: 20px; background: #0f0f0f; padding: 30px; border: 1px solid #222; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# =================================================================
# 3. FUNÇÕES DE NÚCLEO (CORRIGIDAS)
# =================================================================

def render_corretora_chart(ticker, nome):
    try:
        # Download com período maior para garantir dados
        df = yf.download(ticker, period="1y", interval="1d", progress=False)
        if not df.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                increasing_line_color='#d4af37', decreasing_line_color='#ff4b4b'
            )])
            fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', height=500, title=f"MERCADO: {nome}")
            st.plotly_chart(fig, use_container_width=True)
            
            # Métricas Reais
            c1, c2, c3 = st.columns(3)
            ultimo_preco = float(df['Close'].iloc[-1])
            variacao = float(((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100)
            c1.metric("PREÇO ATUAL", f"{ultimo_preco:.2f}")
            c2.metric("VARIAÇÃO", f"{variacao:.2f}%")
            c3.metric("MÁXIMA ANO", f"{df['High'].max():.2f}")
        else:
            st.error("Dados não encontrados para este ativo.")
    except Exception as e:
        st.error(f"Erro na conexão: {e}")

def logic_astrolabio_tesla(max_n, qtd, modalidade):
    # CORREÇÃO DO ERRO DO PRINT: Garantindo que a amostra nunca seja maior que a população
    populacao_total = list(range(1, max_n + 1))
    vortex_base = [n for n in populacao_total if (n % 3 == 0 or n % 6 == 0 or n % 9 == 0)]
    
    # Se o filtro de Tesla for menor que o necessário (ex: Lotomania), usamos a população total
    if len(vortex_base) < qtd:
        pool = populacao_total
    else:
        pool = vortex_base
        
    selecionados = sorted(random.sample(pool, qtd))
    trevos = sorted(random.sample(range(1, 7), 2)) if modalidade == "Milionária" else None
    return selecionados, trevos

# =================================================================
# 4. MENU LATERAL
# =================================================================
with st.sidebar:
    st.markdown("<h1>⚡ NEXUS ELITE</h1>", unsafe_allow_html=True)
    menu = st.radio("COMANDOS:", [
        "💎 IA Quântico Tesla", "🐾 Pet Global Intelligence", "💹 Trade & Commodities", 
        "👗 Fashion High-Ticket", "🌍 Soberania & Reservas", "🙏 Devocional de Poder", "🤝 Conselho de Elite"
    ])
    st.write("---")
    st.write(f"Sync: {datetime.now().strftime('%H:%M:%S')}")

# =================================================================
# 5. MÓDULOS (CONTEÚDO COMPLETO)
# =================================================================

if menu == "💎 IA Quântico Tesla":
    st.title("💎 IA Quântico Tesla")
    jogo = st.selectbox("Escolha o Jogo:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    if st.button("GERAR CONFLUÊNCIA 3-6-9"):
        conf = {"Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5), "Lotomania": (100, 50), "Milionária": (50, 6)}
        n_max, n_qtd = conf[jogo]
        nums, trevos = logic_astrolabio_tesla(n_max, n_qtd, jogo)
        st.markdown(f"<div class='card-quantum'><h1 style='text-align:center;'>{nums}</h1></div>", unsafe_allow_html=True)
        if trevos: st.write(f"☘️ Trevos: {trevos}")

elif menu == "🐾 Pet Global Intelligence":
    st.title("🐾 Mercado Pet Specialization")
    ativo = st.selectbox("Ativo:", ["PETZ3.SA", "CHWY", "PAWZ"])
    render_corretora_chart(ativo, "Setor Pet")

elif menu == "💹 Trade & Commodities":
    st.title("💹 Trade & Finanças")
    ativo = st.selectbox("Ativo:", ["BTC-USD", "GC=F", "USDBRL=X"])
    render_corretora_chart(ativo, "Commodities/FX")

elif menu == "👗 Fashion High-Ticket":
    st.title("👗 Fashion High-Ticket & Luxury")
    render_corretora_chart("MC.PA", "LVMH Group")
    
    st.subheader("Market Share Luxo")
    col1, col2 = st.columns(2)
    marcas = ['LVMH', 'Hermès', 'Dior', 'Chanel', 'Richemont']
    valores = [450, 220, 160, 120, 90]
    with col1:
        st.plotly_chart(go.Figure(data=[go.Bar(x=marcas, y=valores, marker_color='#d4af37')], layout=dict(template='plotly_dark')), use_container_width=True)
    with col2:
        st.plotly_chart(go.Figure(data=[go.Pie(labels=marcas, values=valores, hole=.4)], layout=dict(template='plotly_dark')), use_container_width=True)

elif menu == "🌍 Soberania & Reservas":
    st.title("🌍 Reservas de Soberania")
    st.subheader("Reservas de Ouro (Toneladas)")
    paises = ['EUA', 'Alemanha', 'FMI', 'Itália', 'França', 'Rússia', 'China']
    ton = [8133, 3355, 2814, 2451, 2436, 2332, 2191]
    st.plotly_chart(go.Figure(data=[go.Bar(x=paises, y=ton, marker_color='#d4af37')], layout=dict(template='plotly_dark')), use_container_width=True)
    st.markdown("> **Nota:** O Brasil possui reservas estratégicas de Nióbio que superam 90% do mercado mundial.")

elif menu == "🙏 Devocional de Poder":
    st.title("🙏 Devocional de Poder")
    st.markdown("""
    <div class='card-quantum' style='border-left: 5px solid #d4af37;'>
        <h2>O FUNDAMENTO</h2>
        <p>"A soberania financeira sem soberania espiritual é castelo na areia."</p>
        <p><b>Princípio de Hoje:</b> A riqueza é uma ferramenta para o propósito, não o propósito em si.</p>
    </div>
    """, unsafe_allow_html=True)

elif menu == "🤝 Conselho de Elite":
    st.title("🤝 Conselho de Elite")
    st.checkbox("Checklist de Operação realizado?")
    st.checkbox("Gestão de Risco 2:1 aplicada?")
    st.metric("META DIÁRIA", "R$ 1.500,00", "+5%")
