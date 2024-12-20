# Projet de Machine Learning : Infrastructure, Application ML, Pipeline CI/CD et Monitoring

## Étape 1 : Infrastructure

### 1.1 Installation de Terraform et Ansible

#### Installer Terraform sur Ubuntu

```bash
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt-get update && sudo apt-get install terraform
```

**Vérification :**

```bash
terraform -v
```

#### Installer Ansible sur Ubuntu

```bash
sudo apt-get update
sudo apt-get install -y ansible
```

**Vérification :**

```bash
ansible --version
```

### 1.2 Configuration Terraform

#### `main.tf`

```hcl
resource "google_compute_instance" "ubuntu_vm" {
  name         = "ubuntu-vm2"
  machine_type = "e2-medium"
  zone         = "europe-west9-b"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  tags = ["http-server", "https-server"]
}
```

#### `providers.tf`

```hcl
provider "google" {
  credentials = file("C:/Users/Manel CHENNA/Desktop/MLops/credentials/terraform-key.json")
  project     = "plucky-sound-444819-n5"
  region      = "europe-west9"
}
```

### 1.3 Commandes Terraform

1. **Initialiser Terraform :**

   ```bash
   terraform init
   ```

2. **Planifier le déploiement :**

   ```bash
   terraform plan
   ```

3. **Appliquer le déploiement :**

   ```bash
   terraform apply
   ```

---

## Étape 2 : Application ML

On a développé une application Flask permettant de faire des prédictions à partir d'un modèle de Machine Learning.

### 2.1 API Flask

- **Fichier `main.py`** :

```python
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)
model = joblib.load("model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    prediction = model.predict([data['features']])
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
```

**Instructions pour exécuter l'API :**
```bash
python ml_app/api/main.py
```

Accéder à l'API :
```bash
http://localhost:5003
```

#### **Requête pour tester l'API :**
```bash
curl -X POST http://localhost:5003/predict -H "Content-Type: application/json" -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

### 2.2 Entraînement du Modèle

- **Fichier `train.py`** :

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import mlflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("iris_classification")

data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2)

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    mlflow.sklearn.log_model(model, "model")
    mlflow.log_param("n_estimators", 100)
    accuracy = model.score(X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    print(f"Modèle enregistré avec une précision de {accuracy:.2f}")
```

**Instructions pour entraîner le modèle :**
```bash
python ml_app/model/train.py
```

Lancer l'interface MLflow :
```bash
mlflow ui --port 5000
```

Accéder à l'interface :
```bash
http://127.0.0.1:5000
```

---

## Étape 3 : Pipeline CI/CD

On a mis en place un pipeline CI/CD avec GitHub Actions pour automatiser le déploiement de l'application.

### Fichier `.github/workflows/ci-cd.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Build Docker image
        run: docker build -t ml-app:latest .

      - name: Run tests
        run: pytest tests/
```

---

## Étape 4 : Monitoring

On a configuré le monitoring de l'application avec Prometheus et Grafana.

### Fichier `prometheus.yml`

```yaml
scrape_configs:
  - job_name: 'ml-app'
    static_configs:
      - targets: ['ml-app-container:5003']
```

### Lancement du Monitoring

Démarrez Prometheus et Grafana avec Docker Compose :
```bash
docker-compose up --build
```

Accès aux services :
- **Prometheus** : http://localhost:9090
- **Grafana** : http://localhost:3000 (utilisateur : `admin`, mot de passe : `admin`)

---

## Explication des Fichiers et Dossiers

### Racine du Projet
- **.github/workflows/ci-cd.yml** : Pipeline CI/CD pour automatiser le déploiement avec GitHub Actions.
- **ansible/** : Fichiers Ansible pour l'automatisation du provisionnement.
- **backups/** : Sauvegardes des modèles ou configurations importantes.

### Docker
- **docker-compose.yml** : Configuration pour lancer les services Docker.
- **Dockerfile** : Image Docker pour l'application.
- **prometheus.yml** : Configuration de Prometheus pour la surveillance.

### ml_app
- **api/** : Code de l'API pour servir le modèle.
  - **main.py** : Fichier principal de l'API.
  - **requirements.txt** : Dépendances Python.
- **model/** : Code et fichiers du modèle ML.
  - **train.py** : Script pour entraîner le modèle.
  - **model.pkl** : Modèle pré-entraîné.

### mlartifacts
- Contient les fichiers MLflow pour les expériences et artefacts des modèles.
