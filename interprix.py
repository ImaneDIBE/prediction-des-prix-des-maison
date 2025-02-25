import streamlit as st
import sys
sys.path.append("D:\\Lib\\site-packages")

import joblib
import numpy as np
import base64


# Charger le modèle XGBoost
model = joblib.load("model_xgboost.pkl")

# --- FONCTION POUR AJOUTER UNE IMAGE EN ARRIÈRE-PLAN ---
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode()
        page_bg_img = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: 100% 100%;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        .transparent-box {{
            background: rgba(255, 255, 255, 0.3);
            padding: 2rem;
            border-radius: 10px;
            width: 50%;
            margin: auto;
            text-align: center;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.2);
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("L'image d'arrière-plan est introuvable. Vérifiez le fichier 'nyk.jpg'.")

# --- APPLIQUER L'IMAGE EN ARRIÈRE-PLAN ---
add_bg_from_local("nyk.jpg")

# --- TITRE ---
st.markdown("<h1 style='text-align: center; color: white;'>Prédiction des Prix des Maisons 🏡</h1>", unsafe_allow_html=True)

# --- INTRODUCTION ---
st.markdown("""
<div class="header-box">
    <p style="color: white;">Cette interface permet de prédire les prix des maisons à New York en fonction de plusieurs critères.</p>
    <p style="color: white;">Pour mieux comprendre notre approche, vous pouvez consulter notre rapport ci-dessous.</p>
</div>
""", unsafe_allow_html=True)

# --- BOUTON DE TÉLÉCHARGEMENT ---
if st.button("📥 Télécharger le Rapport"):
    with open("rapport_predictin_des_prix_des_maisons.pdf", "rb") as file:
        st.download_button(label="📥 Télécharger le Rapport", data=file, file_name="rapport_predictin_des_prix_des_maisons.pdf", mime="application/pdf")

# Champs de saisie pour l'utilisateur
area = st.number_input("Surface en m²", min_value=10, max_value=1000, step=1)
bathrooms = st.selectbox("Nombre de salles de bain", [1, 2, 3, 4])
stories = st.selectbox("Nombre d'étages", [1, 2, 3, 4])
bedrooms = st.selectbox("Nombre de chambres", [1, 2, 3, 4, 5, 6])
parking = st.selectbox("Nombre de places de parking", [0, 1, 2, 3])
furnishingstatus = st.selectbox("État du mobilier", ["semi-furnished", "unfurnished", "furnished"])

# Variables catégoriques (Oui/Non)
airconditioning = st.radio("Climatisation", ["yes", "no"])
prefarea = st.radio("Quartier résidentiel privilégié ?", ["yes", "no"])
mainroad = st.radio("Proximité de la route principale", ["yes", "no"])
guestroom = st.radio("Présence d'une chambre d'amis", ["yes", "no"])


# Encodage des variables catégoriques
airconditioning = 1 if airconditioning == "yes" else 0
prefarea = 1 if prefarea == "yes" else 0
mainroad = 1 if mainroad == "yes" else 0
guestroom = 1 if guestroom == "yes" else 0
furnishing_map = {"semi-furnished": 1, "unfurnished": 2, "furnished": 0}
furnishingstatus = furnishing_map[furnishingstatus]

# Prédiction
if st.button("Prédire le prix"):
    input_data = np.array([[area, bathrooms, stories, airconditioning, parking, bedrooms, furnishingstatus, prefarea, mainroad, guestroom]])
    predicted_price = model.predict(input_data)[0]
    
    st.info(f"Prix estimé : {predicted_price:,.2f} $")
