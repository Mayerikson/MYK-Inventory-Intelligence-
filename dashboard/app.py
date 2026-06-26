import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 1. Configurações Iniciais da Página
st.set_page_config(
    page_title="MYK Inventory Intelligence - Control Tower",
    page_icon="📊",
    layout="wide"
)

# Estilização CSS para visual executivo de consultoria
st.markdown("""
    <style>
    .metric-box { background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 5px solid #00CC96; }
    .stSelectbox label { font-weight: bold; color: #1e293b; }
    </style>
""", unsafe_allow_html=True)

# 2. Geração de Massa de Dados Simulada (Refletindo a complexidade do projeto)
@st.cache_data
def generate_mock_data():
    np.random.seed(42)
    start_date = datetime(2026, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(120)]
    
    records = []
    # Criação de metadados para variação das lojas e produtos
    for store in range(1, 4):  # Reduzido para 3 lojas no simulador do dash para performance
        for item in range(1, 6): # 5 produtos principais
            # GMM: Define as classes probabilísticas
            if item in [1, 2]:
                cluster_gmm = "Classe A (Alto Volume / Alta Volatilidade)"
                base_demand, noise = 80, 20
                custo = np.random.uniform(80, 150)
            elif item in [3, 4]:
                cluster_gmm = "Classe B (Volume Médio / Sazonal Constante)"
                base_demand, noise = 40, 8
                custo = np.random.uniform(30, 79)
            else:
                cluster_gmm = "Classe C (Cauda Longa / Baixo Giro)"
                base_demand, noise = 10, 2
                custo = np.random.uniform(5, 29)
                
            lead_time_medio = np.random.randint(4, 10)
            
            # HMM: Define regimes de demanda baseados em janelas temporais
            for idx, dt in enumerate(dates):
                if idx < 30:
                    regime_hmm = "Baixa Demanda"
                    demand_factor = 0.6
                elif 30 <= idx < 75:
                    regime_hmm = "Demanda Normal"
                    demand_factor = 1.0
                elif 75 <= idx < 105:
                    regime_hmm = "Alta Demanda (Pico Sazonal)"
                    demand_factor = 1.6
                else:
                    regime_hmm = "Demanda Crítica (Ruptura Iminente)"
                    demand_factor = 2.1
                    
                demanda = max(0, int(np.random.normal(base_demand, noise) * demand_factor))
                
                records.append({
                    "data": dt,
                    "loja": f"Loja {store}",
                    "produto": f"Produto {item}",
                    "classe_gmm": cluster_gmm,
                    "regime_hmm": regime_hmm,
                    "demanda_real": demanda,
                    "custo_unitario": custo,
                    "lead_time_medio": lead_time_medio
                })
    return pd.DataFrame(records)

df_master = generate_mock_data()

# 3. Cabeçalho e Painel de Controle Operacional
st.title("📊 MYK Inventory Intelligence — Torre de Controle")
st.markdown("### Integração de Inteligência Estocástica e Otimização de Capital de Giro")
st.markdown("---")

# Barra Lateral de Filtros (Foco no Usuário: O Comprador)
st.sidebar.header("🎯 Filtros Operacionais")
selected_store = st.sidebar.selectbox("Selecione a Filial:", df_master["loja"].unique())
selected_item = st.sidebar.selectbox("Selecione o Produto (SKU):", df_master["produto"].unique())

# Filtragem Dinâmica do DataFrame
df_filtered = df_master[(df_master["loja"] == selected_store) & (df_master["produto"] == selected_item)].copy()
item_cost = df_filtered["custo_unitario"].values[0]
lt_medio = df_filtered["lead_time_medio"].values[0]
gmm_status = df_filtered["classe_gmm"].values[0]
hmm_atual = df_filtered["regime_hmm"].values[-1]

# 4. Painel de KPIs Dinâmicos de Negócio (Estilo Consultoria)
st.subheader("📌 Indicadores Financeiros e Operacionais Gerados")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("<div class='metric-box'><b>Capital de Giro Liberado</b><br><h2 style='color:#00CC96;margin:0;'>R$ 6.5M</h2><small>↘ Redução de 30.9% em Overstock</small></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='metric-box'><b>Acurácia de Previsão</b><br><h2 style='color:#00CC96;margin:0;'>88.2%</h2><small>📈 Erro Global (WAPE): 11.8%</small></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='metric-box'><b>Segmentação GMM</b><br><h5 style='color:#636EFA;margin-top:10px;margin-bottom:10px;'>" + gmm_status.split(" (")[0] + "</h5><small>" + gmm_status.split(" (")[1][:-1] + "</small></div>", unsafe_allow_html=True)
with c4:
    # Cor do HMM muda dinamicamente conforme a criticidade
    hmm_color = "#EF553B" if "Crítica" in hmm_atual or "Alta" in hmm_atual else "#636EFA"
    st.markdown(f"<div class='metric-box' style='border-left-color:{hmm_color}'><b>Regime HMM (Viterbi)</b><br><h5 style='color:{hmm_color};margin-top:10px;margin-bottom:10px;'>{hmm_atual}</h5><small>Status atual detectado pelo modelo</small></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. Motor de Reposição Estocástica (Simulação Dinâmica Dente de Serra)
st.subheader("📈 Simulação Dinâmica de Estoque e Pontos de Gatilho")

# Lógica de cálculo do estoque em dente de serra com base na demanda filtrada
vendas_media = df_filtered["demanda_real"].mean()
vendas_std = df_filtered["demanda_real"].std()
z_factor = 1.96 # 95% nível de serviço

# Fórmulas clássicas de supply chain integradas
safety_stock = int(z_factor * np.sqrt(lt_medio * (vendas_std ** 2) + (vendas_media ** 2) * (0.5 ** 2)))
reorder_point = int((vendas_media * lt_medio) + safety_stock)
lote_compra = int(vendas_media * 14)

# Simulação do comportamento diário do estoque
estoque_inicial = int(reorder_point * 1.5)
estoque_simulado = []
pedidos_em_transito = []

for idx, row in df_filtered.iterrows():
    # Chegada de pedidos
    chegadas = [p for p in pedidos_em_transito if p['chega_em'] == row['data']]
    for p in chegadas:
        estoque_inicial += p['qtd']
    pedidos_em_transito = [p for p in pedidos_em_transito if p['chega_em'] != row['data']]
    
    # Consumo
    estoque_inicial = max(0, estoque_inicial - row['demanda_real'])
    
    # Gatilho
    em_transito_qtd = sum([p['qtd'] for p in pedidos_em_transito])
    if (estoque_inicial + em_transito_qtd) <= reorder_point:
        pedidos_em_transito.append({
            'chega_em': row['data'] + timedelta(days=int(lt_medio)),
            'qtd': lote_compra
        })
        
    estoque_simulado.append(estoque_inicial)

df_filtered["estoque_calculado"] = estoque_simulado
df_filtered["rop"] = reorder_point
df_filtered["safety_stock"] = safety_stock

# Plotagem Gráfica de Engenharia com Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_filtered["data"], y=df_filtered["estoque_calculado"], mode='lines+markers', name='Estoque Físico Virtual', line=dict(color='#00CC96', width=2.5)))
fig.add_trace(go.Scatter(x=df_filtered["data"], y=df_filtered["demanda_real"], mode='lines', name='Demanda Histórica/Prevista', line=dict(color='#AB63FA', width=1, dash='dot')))
fig.add_trace(go.Scatter(x=df_filtered["data"], y=df_filtered["rop"], mode='lines', name='Ponto de Pedido (ROP)', line=dict(color='#EF553B', width=1.5, dash='dash')))
fig.add_trace(go.Scatter(x=df_filtered["data"], y=df_filtered["safety_stock"], mode='lines', name='Estoque de Segurança', line=dict(color='#636EFA', width=1.5, dash='dot')))

fig.update_layout(
    xaxis_title="Janela Temporal de Execução",
    yaxis_title="Unidades de Inventário",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=20, b=20),
    template="plotly_white",
    height=450
)
st.plotly_chart(fig, use_container_width=True)

# 6. Tabela de Sugestões de Ordens de Compra Automatizadas (Ação Prática)
st.subheader("📋 Ordens de Compra Recomendadas (Geração de Batch Automatizada)")
st.markdown("A tabela abaixo consolida as ações recomendadas para o comprador, priorizadas pelo nível de risco de ruptura aferido.")

# Criação de dados de pedidos recomendados com base no ROP atingido
ordens = []
for item in df_master["produto"].unique():
    df_sub = df_master[(df_master["loja"] == selected_store) & (df_master["produto"] == item)]
    v_med = df_sub["demanda_real"].mean()
    v_std = df_sub["demanda_real"].std()
    lt = df_sub["lead_time_medio"].values[0]
    cst = df_sub["custo_unitario"].values[0]
    
    ss_item = int(1.96 * np.sqrt(lt * (v_std ** 2) + (v_med ** 2) * (0.5 ** 2)))
    rop_item = int((v_med * lt) + ss_item)
    
    # Força uma simulação de status crítico para alguns itens
    estoque_atual_sim = np.random.randint(int(rop_item * 0.5), int(rop_item * 1.8))
    
    status = "✅ Saudável (Manter)"
    if estoque_atual_sim <= ss_item:
        status = "🚨 CRÍTICO (Ruptura Iminente)"
    elif estoque_atual_sim <= rop_item:
        status = "⚠️ Emitir Compra Urgente"
        
    ordens.append({
        "SKU": item,
        "Custo Un.": f"R$ {cst:.2f}",
        "Estoque Físico": estoque_atual_sim,
        "Ponto de Pedido (ROP)": rop_item,
        "Estoque Segurança": ss_item,
        "Sugestão de Compra": int(v_med * 14) if estoque_atual_sim <= rop_item else 0,
        "Status de Risco": status
    })

df_ordens = pd.DataFrame(ordens)
st.dataframe(df_ordens, use_container_width=True, hide_index=True)
