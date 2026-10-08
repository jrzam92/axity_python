import joblib
import pandas as pd

def load_model(filepath: str):
    """Carga un modelo previamente guardado."""
    return joblib.load(filepath)

def predict(model, input_data: pd.DataFrame) -> list:
    """Realiza predicciones usando el modelo cargado."""
    return model.predict(input_data).tolist()