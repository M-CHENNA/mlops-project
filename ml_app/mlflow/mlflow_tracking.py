import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Charger les données
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)

# Démarrer une expérience MLflow
mlflow.set_experiment("iris_classification")

with mlflow.start_run():
    # Entraîner le modèle
    model = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=42)
    model.fit(X_train, y_train)
    
    # Faire des prédictions
    predictions = model.predict(X_test)
    
    # Évaluer le modèle
    acc = accuracy_score(y_test, predictions)
    
    # Enregistrer les paramètres et métriques
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 3)
    mlflow.log_metric("accuracy", acc)
    
    # Enregistrer le modèle
    mlflow.sklearn.log_model(model, "random_forest_model")

    print(f"Modèle enregistré avec une précision de : {acc}")
