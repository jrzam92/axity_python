import pandas as pd
import pytest
from ds_practice.data import load_and_clean_csv, get_features_and_target
from ds_practice.model import train_classifier, save_model
from ds_practice.inference import load_model, predict

@pytest.fixture
def dummy_dataset(tmp_path):
    """Crea un CSV temporal para las pruebas."""
    df = pd.DataFrame({
        'edad': [25, 30, 45, 22, 50],
        'salario': [30000, 40000, 80000, 25000, 90000],
        'compra': [0, 0, 1, 0, 1]  # Target (0 = No, 1 = Sí)
    })
    # Guardamos en una ruta temporal
    file_path = tmp_path / "dataset.csv"
    df.to_csv(file_path, index=False)
    return file_path

def test_full_ml_pipeline(dummy_dataset, tmp_path):
    # 1. Laboratorio: Cargar y limpiar
    df = load_and_clean_csv(dummy_dataset)
    assert len(df) == 5
    
    X, y = get_features_and_target(df, target_col='compra')
    
    # 2. Laboratorio: Entrenar clasificador
    model = train_classifier(X, y)
    assert model is not None
    
    # 3. Laboratorio: Guardar con joblib
    model_path = tmp_path / "modelo_prueba.joblib"
    save_model(model, model_path)
    assert model_path.exists()
    
    # 4. Laboratorio: Probar inferencia
    loaded_model = load_model(model_path)
    
    # Hacemos una predicción con los mismos datos de X (solo para probar que funciona)
    predictions = predict(loaded_model, X)
    
    assert len(predictions) == 5
    assert all(p in [0, 1] for p in predictions) # Las predicciones deben ser 0 o 1