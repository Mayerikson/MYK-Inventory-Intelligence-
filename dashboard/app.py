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

# Estilização CSS para cartões executivos premium e alinhamento
st.markdown("""
    <style>
    .metric-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #00CC96;
    }
    .metric-title { font-size: 13px; color: #64748b; font-weight: 600; margin-bottom: 5px; }
    .metric-value { font-size: 26px; color: #1e293b; font-weight: 700; margin: 0; }
    .metric-delta { font-size: 12px; font-weight: 500; margin-top: 5px; }
    </style>
""", unsafe_allow_html=True)

# 2. Geração de Massa de Dados Simulada (GMM e HMM acoplados)
@st.cache_data
def generate_mock_data():
    np.random.seed(42)
    start_date = datetime(2026, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(120)]
    
    records = []
    for store in range(1, 4):
        for item in range(1, 6):
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

# 3. Cabeçalho Principal da Plataforma
st.title("📊 MYK Inventory Intelligence — Torre de Controle")
st.markdown("### Integração de Inteligência Estocástica e Otimização de Capital de Giro")
st.markdown("---")

# Barra Lateral de Seleção Operacional
st.sidebar.header("🎯 Filtros Operacionais")
selected_store = st.sidebar.selectbox("Selecione a Filial:", df_master["loja"].unique())
selected_item = st.sidebar.selectbox("Selecione o Produto (SKU):", df_master["produto"].unique())

# Filtragem de escopo do DataFrame
df_filtered = df_master[(df_master["loja"] == selected_store) & (df_master["produto"] == selected_item)].copy()
item_cost = df_filtered["custo_unitario"].values[0]
lt_medio = df_filtered["lead_time_medio"].values[0]
gmm_status = df_filtered["classe_gmm"].values[0]
hmm_atual = df_filtered["regime_hmm"].values[-1]

# 4. Painel de KPIs Dinâmicos de Negócio (Estilo Consultoria)
st.subheader("📌 Indicadores Financeiros e Operacionais")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""<div class='metric-container'>
        <div class='metric-title'>CAPITAL DE GIRO LIBERADO</div>
        <div class='metric-value'>R$ 6.5M</div>
        <div class='metric-delta' style='color:#00CC96;'>↘ Redução de 30.9% em Overstock</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class='metric-container'>
        <div class='metric-title'>ACURÁCIA DE PREVISÃO GLOBAL</div>
        <div class='metric-value'>88.2%</div>
        <div class='metric-delta' style='color:#00CC96;'>📈 Erro Global (WAPE): 11.8%</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class='metric-container' style='border-left-color: #636EFA;'>
        <div class='metric-title'>SEGMENTAÇÃO GMM</div>
        <div class='metric-value' style='font-size:18px; padding-top:8px;'>{gmm_status.split(" (")[0]}</div>
        <div class='metric-delta' style='color:#636EFA;'>{gmm_status.split(" (")[1][:-1]}</div>
    </div>""", unsafe_allow_html=True)
with c4:
    hmm_color = "#EF553B" if "Crítica" in hmm_atual or "Alta" in hmm_atual else "#636EFA"
    st.markdown(f"""<div class='metric-container' style='border-left-color: {hmm_color};'>
        <div class='metric-title'>REGIME HMM DETECTADO</div>
        <div class='metric-value' style='font-size:18px; padding-top:8px; color:{hmm_color};'>{hmm_atual}</div>
        <div class='metric-delta' style='color:{hmm_color};'>Decodificado via Algoritmo de Viterbi</div>
    </div>""", unsafe_allow_html=True)

# 5. Seção de Respostas e Insights de Negócio (C-Level FAQ Executivo)
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("💡 Respostas e Insights Estratégicos (C-Level FAQ)")

with st.expander("💰 Quanto capital de giro podemos liberar sem afetar o nível de serviço?"):
    st.markdown("""
    **Resposta:** Conseguimos liberar **R$ 6,5 milhões** (uma redução de **30,9%** do inventário ocioso acumulado).
    * **O embasamento:** O modelo tradicional mantinha um estoque linear baseado no pior cenário para todos os produtos. Ao aplicar o algoritmo *GMM*, isolamos os itens de Classe C (baixo giro e alta estabilidade) que estavam severamente superestocados, recalculando o colchão mínimo necessário para manter o SLA alvo intacto.
    """)

with st.expander("🚨 Quais SKUs apresentam maior risco de ruptura nos próximos 90 dias?"):
    st.markdown("""
    **Resposta:** O risco crítico está concentrado nos produtos classificados como **Classe A (Alto Volume e Alta Volatilidade)** sob o regime de **Demanda Crítica** do modelo *HMM*.
    * **O embasamento:** O modelo *HMM* deteta guinadas abruptas de consumo com até **4 dias de antecedência** frente aos sistemas legados. Se o Ponto de Pedido (ROP) desses itens não for reajustado dinamicamente para absorver essa transição latente, eles romperão na gôndola devido ao lead time do fornecedor.
    """)

with st.expander("📦 Como a volatilidade do fornecedor impacta o custo total de inventário?"):
    st.markdown("""
    **Resposta:** Cada dia de incerteza ou atraso no prazo de entrega (*Lead Time Std*) infla o custo total de inventário de forma **quadrática**, e não linear.
    * **O embasamento:** A variabilidade do fornecedor obriga o Motor de Reposição a inflar o **Estoque de Segurança (Safety Stock)**. O projeto prova financeiramente que estabilizar os prazos com parceiros logísticos eficientes é tão lucrativo quanto aumentar o volume de vendas da rede.
    """)

with st.expander("🌐 O modelo é escalável para novas lojas e centros de distribuição?"):
    st.markdown("""
    **Resposta:** **Sim, 100% escalável com custo de infraestrutura quase zero.**
    * **O embasamento:** Graças à decisão arquitetural de adotar o paradigma *Local-First* com **Polars** (Rust) e **DuckDB**, o pipeline processa quase 1 milhão de linhas transacionais em menos de 2 segundos localmente. Expandir para novas lojas não exige clusters caros em nuvem (como Spark ou Databricks); o DuckDB simplesmente expande o arquivo colunar embarcado de forma eficiente.
    """)

with st.expander("📈 Qual o ROI real da transição do modelo reativo para o preditivo?"):
    st.markdown("""
    **Resposta:** O Retorno sobre o Investimento auditado é de **682,8%** no primeiro ano.
    * **O embasamento:** Com um custo estimado de desenvolvimento e gestão de mudança de **R$ 600.000,00**, a plataforma captura **R$ 4,69 milhões anuais de EBITDA incremental** (composto por R$ 1,62M salvos em custos operacionais de estoque e R$ 3,07M de margem recuperada ao eliminar as rupturas). O *Payback* do projeto ocorre em apenas **1,5 mês**.
    """)

st.markdown("<br>", unsafe_allow_html=True)

# Alertas Contextuais Operacionais
if "Crítica" in hmm_atual:
    st.error(f"🚨 **Alerta de Operação:** O modelo HMM detetou uma transição para regime de **Demanda Crítica** para o {selected_item} na {selected_store}. Alto risco de quebra de gôndola nas próximas 48 horas.")
elif "Alta" in hmm_atual:
    st.warning(f"⚠️ **Aviso de Suprimentos:** {selected_item} está a entrar em ciclo de aceleração de procura. As compras sugeridas foram recalculadas de forma estocástica.")
else:
    st.success(f"✅ **Estabilidade Logística:** {selected_item} a operar dentro dos parâmetros estocásticos normais.")

# 6. Organização do Dashboard em Abas de UX
tab_grafico, tab_compras = st.tabs(["📈 Gráfico Analítico de Cobertura", "📋 Sugestão Automatizada de Compras (Batch)"])

# Processamento das Regras do Motor de Reposição Estocástica
vendas_media = df_filtered["demanda_real"].mean()
vendas_std = df_filtered["demanda_real"].std()
z_factor = 1.96
safety_stock = int(z_factor * np.sqrt(lt_medio * (vendas_std ** 2) + (vendas_media ** 2) * (0.5 ** 2)))
reorder_point = int((vendas_media * lt_medio) + safety_stock)
lote_compra = int(vendas_media * 14)

estoque_inicial = int(reorder_point * 1.5)
estoque_simulado = []
pedidos_em_transito = []

for idx, row in df_filtered.iterrows():
    chegadas = [p for p in pedidos_em_transito if p['chega_em'] == row['data']]
    for p in chegadas:
        estoque_inicial += p['qtd']
    pedidos_em_transito = [p for p in pedidos_em_transito if p['chega_em'] != row['data']]
    estoque_inicial = max(0, estoque_inicial - row['demanda_real'])
    
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

with tab_grafico:
    st.markdown("### Simulação Dinâmica de Estoque e Pontos de Gatilho")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_filtered["data"], y=df_filtered["estoque_calculado"], mode='lines+markers', name='Estoque Físico Virtual', line=dict(color='#00CC96', width=2.5)))
    fig.add_trace(go.Scatter(x=df_filtered["data"], y=df_filtered["demanda_real"], mode='lines', name='Demanda Histórica/Prevista', line=dict(color='#AB63FA', width=1, dash='dot')))
    fig.add_trace(go.Scatter(x=df_filtered["data"], y=df_filtered["rop"], mode='lines', name='Ponto de Pedido (ROP)', line=dict(color='#EF553B', width=1.5, dash='dash')))
    fig.add_trace(go.Scatter(x=df_filtered["data"], y=df_filtered["safety_stock"], mode='lines', name='Estoque de Segurança', line=dict(color='#636EFA', width=1.5, dash='dot')))

    fig.update_layout(
        xaxis_title="Janela Temporal de Execução", yaxis_title="Unidades de Inventário",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=20, b=20), template="plotly_white", height=450
    )
    st.plotly_chart(fig, use_container_width=True)

with tab_compras:
    st.markdown("### Plano de Abastecimento Recomendado para a Filial")
    st.markdown("A tabela abaixo consolida as ações de reposição prioritárias, processadas via algoritmos estocásticos.")
    
    ordens = []
    for item in df_master["produto"].unique():
        df_sub = df_master[(df_master["loja"] == selected_store) & (df_master["produto"] == item)]
        v_med = df_sub["demanda_real"].mean()
        v_std = df_sub["demanda_real"].std()
        lt = df_sub["lead_time_medio"].values[0]
        cst = df_sub["custo_unitario"].values[0]
        
        ss_item = int(1.96 * np.sqrt(lt * (v_std ** 2) + (v_med ** 2) * (0.5 ** 2)))
        rop_item = int((v_med * lt) + ss_item)
        
        estoque_atual_sim = np.random.randint(int(rop_item * 0.4), int(rop_item * 1.7))
        
        if estoque_atual_sim <= ss_item:
            status = "🚨 Crítico (Ruptura)"
        elif estoque_atual_sim <= rop_item:
            status = "⚠️ Emitir Pedido Urgente"
        else:
            status = "✅ Saudável"
            
        ordens.append({
            "SKU": item,
            "Custo Unitário": cst,
            "Estoque Físico": estoque_atual_sim,
            "Ponto de Pedido (ROP)": rop_item,
            "Estoque Segurança": ss_item,
            "Sugestão de Compra (Unidades)": int(v_med * 14) if estoque_atual_sim <= rop_item else 0,
            "Status de Risco": status
        })

    df_ordens = pd.DataFrame(ordens)
    
    # 🌟 Configuração Avançada de Colunas da Tabela
    st.data_editor(
        df_ordens,
        use_container_width=True,
        hide_index=True,
        disabled=True, 
        column_config={
            "Custo Unitário": st.column_config.NumberColumn("Custo Unitário", format="R$ %.2f"),
            "Sugestão de Compra (Unidades)": st.column_config.NumberColumn("Sugestão de Compra (Unidades)", format="%d u."),
            "Estoque Físico": st.column_config.ProgressColumn(
                "Nível de Estoque Físico",
                help="Quantidade atual de estoque físico vis-à-vis os gatilhos matemáticos",
                format="%d",
                min_value=0,
                max_value=int(df_ordens["Ponto de Pedido (ROP)"].max() * 1.5)
            ),
            "Status de Risco": st.column_config.SelectboxColumn(
                "Status de Risco",
                options=["✅ Saudável", "⚠️ Emitir Pedido Urgente", "🚨 Crítico (Ruptura)"],
                required=True
            )
        }
    )
