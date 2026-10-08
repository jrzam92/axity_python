import pandas as pd

def load_and_clean_csv(filepath: str) -> pd.DataFrame:
    """Carga un CSV y realiza una limpieza básica."""
    df = pd.read_csv(filepath)
    
    # Limpieza de ejemplo: eliminar filas con valores nulos
    df = df.dropna()
    return df

def get_features_and_target(df: pd.DataFrame, target_col: str):
    """Separa el DataFrame en variables predictoras (X) y objetivo (y)."""
    X = df.drop(columns=[target_col])
    y = df[target_col]
    return X, y