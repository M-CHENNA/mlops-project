FROM python:3.9

WORKDIR /app

# L code de l'API dans le répertoire de travail
COPY ml_app/api/ /app/

# Le modèle entraîné
COPY ml_app/model/model.pkl /app/

# Installation des dépendances nécessaires
RUN pip install Flask joblib scikit-learn prometheus-flask-exporter

# Exposition du port 5003 pour l'API Flask
EXPOSE 5003

# Commande pour lancer l'API
CMD ["python", "main.py"]
