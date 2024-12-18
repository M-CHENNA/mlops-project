import subprocess

def train_model():
    subprocess.run(["python", "../model/train.py"])

def deploy_model():
    subprocess.run(["docker", "build", "-t", "ml_api", "../../docker"])
    subprocess.run(["docker", "run", "-d", "-p", "5000:5000", "ml_api"])

if __name__ == "__main__":
    train_model()
    deploy_model()
