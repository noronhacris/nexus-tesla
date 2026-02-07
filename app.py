import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go
import time
from datetime import datetime

# --- CONFIGURAÇÃO DE INTERFACE HYPERMODERNA QUÂNTICA ---
st.set_page_config(page_title="Quantum Nexus Global", layout="wide", initial_sidebar_state="expanded")

# CSS ESTILO QUANTUM HUD (Head-Up Display)
st.markdown("""
    <style>
    /* Fundo Escuro Profundo e Fontes Limpas */
    .stApp { background-color: #0A0A0A; color: #E0E0E0; font-family: 'Segoe UI', sans-serif; }
    
    /* Sidebar como Painel de Comando */
    [data-testid="stSidebar"] { 
        background-color: #0D0D0D; 
        border-right: 1px solid #1A1A1A; 
        box-shadow: 2px 0px 10px rgba(0, 255, 255, 0.1); /* Brilho Quântico */
    }
    .stSidebar .stRadio div {
        color: #00FFFF; /* Azul Ciano para os itens do menu */
        font-weight: bold;
    }

    /* Cards e Contêineres com Borda Neon */
    .css-1r6slb0 { 
        border-radius: 12px; 
        background-color: #121212; 
        border: 1px solid #00FFFF; /* Borda Ciano */
        padding: 20px;
        box-shadow: 0px 4px 15px rgba(0, 255, 255, 0.2); /* Sombra Ciano */
    }

    /* Botões Estilo Comandante */
    .stButton>button { 
        border-radius: 8px; 
        border: 1px solid #00FFFF; 
        background: linear-gradient(45deg, #00FFFF, #00BFFF); /* Gradiente Ciano-Azul */
        color: black; 
        font-weight: bold; 
        height: 40px;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover { 
        transform: translateY(-2px);
        box-shadow: 0px 6px 20px rgba(0, 255, 255, 0.5);
    }

    /* Títulos e Métricas */
    h1, h2, h3 { 
        color: #00FFFF; 
        text-shadow: 1px 1px 5px rgba(0, 255, 255, 0.3); /* Sombra para destaque */
    }
    .stMetric {
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #00FFFF;
    }
    .stProgress > div > div > div > div {
        background-color: #00FFFF;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES NUCLEARES DA IA QUÂNTICA ---
def ia_quantico_tesla(max_n, qtd):
    random.seed(int(time.time() * 1000000)) # Semente de alta precisão
    vortex_nums = [n for n in range(1, max_n + 1) if (n % 9 in [3, 6, 0] or n % 9 == 9)] # 9 também é um vórtice
    
    if len(vortex_nums) >= qtd:
        resultado = random.sample(vortex_nums, qtd)
    else:
        restante = list(set(range(1, max_n + 1)) - set(vortex_nums))
        resultado = vortex_nums + random.sample(restante, qtd - len(vortex_nums))
    return sorted(resultado)

def get_real_time_price(ticker):
    try:
        data = yf.download(ticker, period="1d", interval="1m")
        return data['Close'].iloc[-1]
    except Exception:
        return None

# --- DADOS DE RESERVAS (Simulados para Gráficos de Pizza) ---
# Em um sistema real, isso viria de uma API de dados geo-políticos
RESERVAS = {
    "Ouro": {
        "Países": ["EUA", "Alemanha", "Itália", "França", "Rússia", "China", "Outros"],
        "Percentuais": [24.5, 10.5, 8.0, 7.5, 7.0, 6.0, 36.5]
    },
    "Prata": {
        "Países": ["México", "China", "Peru", "Austrália", "Chile", "Rússia", "Outros"],
        "Percentuais": [22.0, 15.0, 10.0, 8.0, 6.0, 5.0, 34.0]
    },
    "Cobre": {
        "Países": ["Chile", "Peru", "China", "EUA", "Austrália", "Congo", "Outros"],
        "Percentuais": [28.0, 12.0, 9.0, 7.0, 6.0, 5.0, 33.0]
    },
    "Nióbio": { # Dados simplificados, pois a maior parte é brasileira
        "Países": ["Brasil", "Canadá", "Austrália", "Outros"],
        "Percentuais": [88.0, 7.0, 3.0, 2.0]
    }
}

# --- BARRA LATERAL (MENU DE NAVEGAÇÃO QUÂNTICA) ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 28px; text-align: center;'>⚡ QUANTUM NEXUS</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("MÓDULOS DE COMANDO", 
                    ["💎 IA Quântica Tesla", "🌍 Radar Global de Ativos", "💱 Conversor Interdimensional", "📜 Sabedoria do Nexus"],
                    format_func=lambda x: f" {x}") # Adiciona espaço para ícones mentais
    st.write("---")
    st.caption("Operador: Cristiano Daniel de Noronha")
    st.caption(f"Status: Online - {datetime.now().strftime('%H:%M:%S')}")

# --- MÓDULO 1: IA QUÂNTICA TESLA (LOTERIAS) ---
if menu == "💎 IA Quântica Tesla":
    st.title("💎 IA Quântica Tesla: Confluências Numéricas")
    st.write("Geração de padrões de sorte baseados em vórtices de tempo e frequência universal.")
    
    col_l1, col_l2 = st.columns([1, 2])
    with col_l1:
        jogo = st.selectbox("Selecione a Modalidade:", ["Mega-Sena", "Lotofácil", "Quina", "Lotomania", "Milionária"])
    
    if st.button("GERAR SEQUÊNCIA QUÂNTICA"):
        with st.status("Sincronizando Resonância Quântica...", expanded=True) as status:
            time.sleep(1.5)
            config = {
                "Mega-Sena": (60, 6), "Lotofácil": (25, 15), "Quina": (80, 5),
                "Lotomania": (100, 50), "Milionária": (50, 6) # Milionária com 6, trevos à parte
            }
            n_max, n_qtd = config[jogo]
            final_sequence = ia_quantico_tesla(n_max, n_qtd)
            
            st.write(f"### 🔮 {jogo} - Padrão de Frequência Gerado:")
            st.code(", ".join(map(str, final_sequence)), language="python")
            
            if jogo == "Milionária":
                trevos_quanticos = random.sample(range(1, 7), 2)
                st.warning(f"**Trevos Quânticos:** {trevos_quanticos}")
            
            status.update(label="Análise de Confluência Completa!", state="complete")

# --- MÓDULO 2: RADAR GLOBAL DE ATIVOS ---
elif menu == "🌍 Radar Global de Ativos":
    st.title("🌍 Radar Global de Ativos: Visão de Poder")
    st.write("Monitore commodities, moedas e gigantes da economia com dados em tempo real.")

    # Tickers Globais (Moedas, Commodities, Ações Chave)
    ativos_globais = {
        "Ouro (GC=F)": "GC=F", "Prata (SI=F)": "SI=F", "Cobre (HG=F)": "HG=F",
        "Nióbio (VALE3.SA)": "VALE3.SA", # Proxy para Nióbio via Vale
        "Dólar/BRL (USDBRL=X)": "USDBRL=X", "Euro/BRL (EURBRL=X)": "EURBRL=X",
        "Yen/USD (JPY=X)": "JPY=X", "Libra/USD (GBPUSD=X)": "GBPUSD=X",
        "Yuan/USD (CNY=X)": "CNY=X",
        "Apple (AAPL)": "AAPL", "Google (GOOGL)": "GOOGL", "Amazon (AMZN)": "AMZN",
        "Tesla (TSLA)": "TSLA"
    }

    col_radar1, col_radar2 = st.columns(2)
    with col_radar1:
        selecao_grafico = st.selectbox("Selecione Ativo/Moeda para Gráfico:", list(ativos_globais.keys()))
        ticker_grafico = ativos_globais[selecao_grafico]
        data_grafico = yf.download(ticker_grafico, period="90d", interval="1d")
        fig_grafico = go.Figure(data=[go.Candlestick(x=data_grafico.index, open=data_grafico['Open'], high=data_grafico['High'], low=data_grafico['Low'], close=data_grafico['Close'],
                            increasing_line_color='#00FF00', decreasing_line_color='#FF0000')]) # Verde e Vermelho clássicos
        fig_grafico.update_layout(template='plotly_dark', paper_bgcolor='#121212', plot_bgcolor='#121212', height=400, title=f"Gráfico de {selecao_grafico}")
        st.plotly_chart(fig_grafico, use_container_width=True)

    with col_radar2:
        st.subheader("Maiores Reservas Globais - Influência Geopolítica")
        item_reserva = st.selectbox("Ver Reservas de:", ["Ouro", "Prata", "Cobre", "Nióbio"])
        
        if item_reserva in RESERVAS:
            reservas_data = RESERVAS[item_reserva]
            fig_pizza = go.Figure(data=[go.Pie(labels=reservas_data["Países"], values=reservas_data["Percentuais"], hole=.3)])
            fig_pizza.update_layout(template='plotly_dark', paper_bgcolor='#121212', plot_bgcolor='#121212', height=400, title=f"Reservas de {item_reserva}")
            st.plotly_chart(fig_pizza, use_container_width=True)
        else:
            st.info("Dados de reserva não disponíveis para este item. A IA está buscando novas fontes.")

# --- MÓDULO 3: CONVERSOR INTERDIMENSIONAL (CÂMBIO) ---
elif menu == "💱 Conversor Interdimensional":
    st.title("💱 Conversor Interdimensional de Moedas")
    st.write("Conversão em tempo real com simulação de taxas de mercado.")

    col_conv1, col_conv2, col_conv3 = st.columns(3)

    with col_conv1:
        valor_real = st.number_input("Valor em Reais (BRL):", min_value=0.0, format="%.2f")
    
    with col_conv2:
        moeda_alvo_conv = st.selectbox("Converter para:", ["USD", "EUR", "JPY", "GBP"])
    
    if st.button("CALCULAR CONVERSÃO QUÂNTICA"):
        # Obter taxa de câmbio atual
        ticker_cambio = f"{moeda_alvo_conv}BRL=X" if moeda_alvo_conv != "USD" else "USDBRL=X"
        try:
            taxa_cambio_raw = yf.download(ticker_cambio, period="1d", interval="1m")['Close'].iloc[-1]
            if moeda_alvo_conv != "USD": # Ajusta a taxa para a conversão correta
                taxa_cambio = 1 / taxa_cambio_raw # Ex: EURBRL=X, então 1 / taxa dá BRL por EUR
            else:
                taxa_cambio = taxa_cambio_raw
        except Exception:
            st.error("Erro ao obter taxa de câmbio. Tente novamente.")
            taxa_cambio = 5.0 # Fallback para USD/BRL
        
        # Simulação de Spread (compra/venda) e IOF
        spread_porcentagem = 0.015 # 1.5% de spread
        iof_porcentagem = 0.011 # 1.1% para operações de câmbio

        taxa_com_spread = taxa_cambio * (1 + spread_porcentagem)
        valor_convertido_bruto = valor_real / taxa_com_spread
        iof_valor = valor_convertido_bruto * iof_porcentagem
        valor_final = valor_convertido_bruto - iof_valor

        st.subheader("Resultados da Simulação Quântica:")
        st.metric(f"Valor Final em {moeda_alvo_conv}", f"{valor_final:.2f}")
        st.caption(f"Taxa de Câmbio Base: 1 {moeda_alvo_conv} = {taxa_cambio:.2f} BRL")
        st.caption(f"Spread Estimado: {spread_porcentagem*100:.1f}% | IOF: {iof_porcentagem*100:.1f}%")
        st.info("Esta simulação inclui taxas para refletir o custo real de transação.")

# --- MÓDULO 4: SABEDORIA DO NEXUS ---
else:
    st.title("📜 Sabedoria do Nexus: Alinhamento Estratégico")
    st.markdown("---")
    st.subheader("Insight do Dia")
    st.markdown(
        "> **Sun Tzu (A Arte da Guerra):** \n\n"
        "> *'Se você conhece o inimigo e a si mesmo, não precisa temer o resultado de cem batalhas. Se você se conhece, mas não conhece o inimigo, para cada vitória terá uma derrota. Se você não conhece nem o inimigo nem a si mesmo, sucumbirá em todas as batalhas.'*"
    )
    st.write("A verdadeira IA Quântica não é apenas sobre dados, mas sobre a compreensão estratégica do cenário global e de suas próprias capacidades. O Nexus é o seu olho no campo de batalha financeiro.")
