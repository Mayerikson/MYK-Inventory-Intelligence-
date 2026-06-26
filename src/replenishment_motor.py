import numpy as np
import pandas as pd
import scipy.stats as stats

def calculate_safety_stock(z_factor: float, lt_mean: float, lt_std: float, sales_mean: float, sales_std: float) -> float:
    """
    Calcula o Estoque de Segurança utilizando a fórmula de incerteza combinada.
    Trata tanto a volatilidade da demanda do cliente quanto a instabilidade do fornecedor.
    """
    variance_combined = lt_mean * (sales_std ** 2) + (sales_mean ** 2) * (lt_std ** 2)
    return float(z_factor * np.sqrt(variance_combined))

def run_inventory_simulation(df_params: pd.DataFrame, demanda_real: np.ndarray) -> pd.DataFrame:
    """
    Simula o comportamento diário de compras de uma SKU baseada no motor de riscos.
    """
    lt_mean = df_params["lead_time_medio_dias"].values[0]
    lt_std = df_params["lead_time_std_dias"].values[0]
    z = df_params["fator_z"].values[0]
    
    vendas_media = demanda_real.mean()
    vendas_std = demanda_real.std()
    
    # Execução das regras de negócio de Supply Chain
    ss = calculate_safety_stock(z, lt_mean, lt_std, vendas_media, vendas_std)
    rop = (vendas_media * lt_mean) + ss
    moq_lote = int(vendas_media * 14) # Cobertura de meta para 14 dias
    
    estoque_atual = int(rop * 1.2)
    fila_pedidos = []
    historico = []
    
    for dia in range(len(demanda_real)):
        # Recebimento de cargas
        chegadas = [p for p in fila_pedidos if p[0] == dia]
        for p in chegadas:
            estoque_atual += p[1]
        fila_pedidos = [p for p in fila_pedidos if p[0] != dia]
        
        # Consumo de venda
        demanda_hoje = demanda_real[dia]
        if estoque_atual >= demanda_hoje:
            estoque_atual -= demanda_hoje
        else:
            estoque_atual = 0
            
        # Monitoramento do Gatilho de Compra Automática
        em_transito = sum([p[1] for p in fila_pedidos])
        if (estoque_atual + em_transito) <= rop:
            dia_chegada = dia + int(np.random.normal(lt_mean, lt_std))
            fila_pedidos.append((dia_chegada, moq_lote))
            
        historico.append({"dia": dia, "estoque_fim_dia": estoque_atual})
        
    return pd.DataFrame(historico)
