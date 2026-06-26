import streamlit as str_app
import pandas as pd
import numpy as np
import plotly.graph_objects as go

str_app.set_page_config(page_title="MYK Inventory Intelligence", layout="wide")

str_app.title(" MYK Inventory Intelligence - Painel de Compras")
str_app.markdown("### Sugestão Automatizada de Reabastecimento Baseada em Riscos")

# Métricas Principais (C-Level Summary)
col1, col2, col3, col4 = str_app.columns(4)
col1.metric("Capital de Giro Liberado", "R$ 6.500.000", "-30.9%")
col2.metric("Redução de Rupturas", "-25%", "Meta Atingida")
col3.metric("Giro de Estoque", "6.5x", "+2.3x")
col4.metric("Economia Anual (EBITDA)", "R$ 4.697.000", "ROI: 682%")

str_app.markdown("---")

# Simulação Gráfica do Estoque em Dente de Serra (Plotly)
str_app.subheader(" Monitoramento Dinâmico de SKU (Exemplo: Item 1 - Loja 1)")

dias = np.arange(1, 61)
estoque = 300 - (dias * 4.5) % 150 + np.random.normal(0, 5, 60)
rop = np.full(60, 120)
ss = np.full(60, 45)

fig = go.Figure()
fig.add_trace(go.Scatter(x=dias, y=estoque, mode='lines+markers', name='Estoque Físico', line=dict(color='#00CC96', width=2)))
fig.add_trace(go.Scatter(x=dias, y=rop, mode='lines', name='Ponto de Pedido (ROP)', line=dict(color='#EF553B', dash='dash')))
fig.add_trace(go.Scatter(x=dias, y=ss, mode='lines', name='Estoque de Segurança', line=dict(color='#636EFA', dash='dot')))

fig.update_layout(xaxis_title="Dias de Análise", yaxis_title="Unidades em Estoque", template="plotly_white")
str_app.plotly_chart(fig, use_container_width=True)
