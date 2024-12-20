import streamlit as st
import requests

st.title("Prédiction avec l'API ML")

features = st.text_input("Entrez les caractéristiques (ex: 5.1, 3.5, 1.4, 0.2)")

if st.button("Prédire"):
    data = {"features": [float(x) for x in features.split(",")]}
    response = requests.post("http://localhost:5003/predict", json=data)
    if response.status_code == 200:
        st.write("Prédiction :", response.json()['prediction'])
    else:
        st.write("Erreur :", response.status_code)
