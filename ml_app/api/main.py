from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
import joblib
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)  

# Chargement du modèle
model_path = os.path.join(os.path.dirname(__file__), '../model/model.pkl')
model = joblib.load(model_path)
# Route pour l'URL racine
@app.route('/')
def home():
    return "Bienvenue sur l'API ML!"

# Route pour les prédictions
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    prediction = model.predict([data['features']])
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
