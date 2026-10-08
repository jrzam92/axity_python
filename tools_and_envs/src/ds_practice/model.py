from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def train_classifier(X, y):
    """Entrena un modelo de clasificación simple."""
    # Usamos un Random Forest clásico de scikit-learn
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model

def save_model(model, filepath: str):
    """Serializa el modelo usando joblib."""
    # Aseguramos que el directorio exista
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(model, filepath)