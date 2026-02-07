import streamlit as st
import random
import yfinance as yf
import plotly.graph_objects as go

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Tesla Quantum Nexus", layout="wide")

# ESTILO TESLA (PRETO E DOURADO)
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #d4af37; }
    .stButton>button { background-color: #d4af37; color: black; border-radius: 10px; width: 100%; }
    h1, h2, h3 { color: #d4af37; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ TESLA QUANTUM NEXUS")
st.write("<p style='text-align: center;'>Operador: Cristiano Daniel de Noronha</p>", unsafe_allow_html=True)

# FUNÇÃO MATEMÁTICA DE TESLA
def reduzir_tesla(n):
    n_limpo = ''.join(filter(str.isdigit, str(n)))
    if not n_limpo: return 0
    soma = int(n_limpo)
    while soma > 9:
        soma = sum(int(d) for d in str(soma))
    return soma

# ABAS DO SISTEMA
tab1, tab2, tab3, tab4 = st.tabs(["🎰 Loteria", "📜 Bíblia", "₿ Cripto", "📊 Mercado Pet"])

with tab1:
    st.header("Frequência de Sorte (Vórtice)")
    if st.button("GERAR NÚMEROS 3-6-9"):
        nums = [n for n in range(1, 61) if reduzir_tesla(n) in [3, 6, 9]]
        sorteio = random.sample(nums, 6)
        st.success(f"Números Identificados: {sorted(sorteio)}")

with tab2:
    st.header("Decifrador de Frequência Bíblica")
    texto = st.text_input("Digite o nome ou versículo:")
    if texto:
        res = reduzir_tesla(sum(ord(c) for c in texto))
        st.metric("Vibração Numérica", res)
        if res == 9: st.warning("ALERTA: Confluência Ponto Zero Detectada!")

with tab3:
    st.header("Monitoramento de Vórtice Cripto")
    moeda = st.selectbox("Escolha a Moeda:", ["BTC-USD", "ETH-USD", "SOL-USD"])
    data = yf.download(moeda, period="7d", interval="1h")
    
    # Cálculo da Linha de Equilíbrio Tesla (Média de 9 períodos)
    data['Tesla_9'] = data['Close'].rolling(window=9).mean()
    
    fig = go.Figure()
    # Velas de Preço
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], 
                                 low=data['Low'], close=data['Close'], name='Mercado'))
    # Linha de Vórtice (Dourada)
    fig.add_trace(go.Scatter(x=data.index, y=data['Tesla_9'], name='Frequência 9',
                             line=dict(color='#d4af37', width=2)))
    
    fig.update_layout(template='plotly_dark', paper_bgcolor='black', plot_bgcolor='black', height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("💡 **Dica do Operador:** Quando o preço toca a linha dourada (Frequência 9), o mercado busca o equilíbrio do Ponto Zero.")

with tab4:
    st.header("🌍 Radar de Riqueza Global")
    ativo_global = st.selectbox("Monitorar Ativo de Refúgio:", ["Gold (Ouro)", "S&P 500 (EUA)", "EUR/USD"])
    
    dict_ativos = {"Gold (Ouro)": "GC=F", "S&P 500 (EUA)": "^GSPC", "EUR/USD": "EURUSD=X"}
    ticker_global = dict_ativos[ativo_global]
    
    # Análise de Volume e Vórtice
    data_g = yf.download(ticker_global, period="30d", interval="1d")
    st.line_chart(data_g['Close'])
    
    st.subheader("💡 Estratégia de Retorno Financeiro")
    st.write("""
    * **Arbitragem Global:** Identificar produtos eletrônicos ou de luxo com alta demanda na Europa/EUA e revenda estratégica.
    * **Investimento em Valor:** Utilizar a Frequência 9 para identificar fundos de índice (ETFs) em pontos de exaustão.
    * **Escalabilidade:** Focar em produtos de consumo que resolvem dores de 'Status' e 'Segurança'.
    """)
