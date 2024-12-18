import requests

url = "http://localhost:5003/predict"
data = {"features": [1.5, 2.3, 3.7, 0.8]}  # Exemple avec 4 valeurs

response = requests.post(url, json=data)

print("Statut:", response.status_code)
print("Réponse:", response.json())
