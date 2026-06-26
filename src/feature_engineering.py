import numpy as np
import pandas as pd

def build_time_features(df_input: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """
    Gera recursos sazonais e temporais clássicos para o LightGBM.
    Convertido para compatibilidade de engenharia.
    """
    df = df_input.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    
    df["month"] = df[date_col].dt.month
    df["day_of_week"] = df[date_col].dt.dayofweek
    df["day_of_year"] = df[date_col].dt.dayofyear
    
    # Termos de Fourier para Sazonalidade Cíclica Anual
    pi_factor = 2 * np.pi / 365.25
    df["fourier_sin_year"] = np.sin(df["day_of_year"] * pi_factor)
    df["fourier_cos_year"] = np.cos(df["day_of_year"] * pi_factor)
    
    return df

def build_lag_features(df_input: pd.DataFrame, target_col: str, group_cols: list) -> pd.DataFrame:
    """
    Cria variáveis de atraso (lags) e estatísticas móveis sem data leakage.
    """
    df = df_input.sort_values(by=group_cols + ["date"]).copy()
    
    # Defasagens de segurança para horizontes longos
    df["lag_7"] = df.groupby(group_cols)[target_col].shift(7)
    df["lag_14"] = df.groupby(group_cols)[target_col].shift(14)
    
    # Médias móveis baseadas no primeiro lag estável
    df["rolling_mean_7"] = df.groupby(group_cols)["lag_7"].transform(lambda x: x.rolling(7).mean())
    df["rolling_mean_30"] = df.groupby(group_cols)["lag_7"].transform(lambda x: x.rolling(30).mean())
    
    return df.dropna()
