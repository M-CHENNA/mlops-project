import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Définir le serveur MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("iris_classification")

# Charger les données
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2)

with mlflow.start_run():
    # Entraîner le modèle
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # Logger le modèle
    mlflow.sklearn.log_model(model, "model")
    print("Modèle loggé avec succès.")

    # Logger des paramètres
    mlflow.log_param("n_estimators", 100)
    print("Paramètres loggés avec succès.")

    # Logger des métriques
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    print(f"Modèle enregistré avec une précision de {accuracy:.2f}")

print("Fin de l'exécution du script.")
