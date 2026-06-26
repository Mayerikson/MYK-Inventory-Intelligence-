import numpy as np
import pytest
from src.replenishment_motor import calculate_safety_stock

def test_calculate_safety_stock_zero_variance():
    """Garante que se não houver volatilidade na demanda ou no fornecedor, o estoque de segurança é zero."""
    z_factor = 1.96  # 95% de Nível de Serviço
    lt_mean = 5.0
    lt_std = 0.0
    sales_mean = 50.0
    sales_std = 0.0
    
    ss = calculate_safety_stock(z_factor, lt_mean, lt_std, sales_mean, sales_std)
    assert ss == 0.0

def test_safety_stock_increases_with_volatility():
    """Valida se o modelo aumenta o colchão de segurança à medida que o fornecedor se torna instável."""
    z_factor = 1.96
    vendas_media = 50.0
    vendas_std = 5.0
    lt_mean = 7.0
    
    # Fornecedor estável (desvio padrão de prazos = 0.1)
    ss_estavel = calculate_safety_stock(z_factor, lt_mean, 0.1, vendas_media, vendas_std)
    
    # Fornecedor instável/atrasado (desvio padrão de prazos = 3.0)
    ss_instavel = calculate_safety_stock(z_factor, lt_mean, 3.0, vendas_media, vendas_std)
    
    assert ss_instavel > ss_estavel
