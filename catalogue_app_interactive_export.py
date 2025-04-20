
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Catalogue interactif", layout="centered")

@st.cache_data
def charger_catalogue(path):
    try:
        return pd.read_excel(path)
    except Exception as e:
        st.error(f"Erreur de chargement du fichier Excel : {e}")
        return pd.DataFrame()

df = charger_catalogue("catalogue_articles_final.xlsx")

st.markdown("<h2 style='text-align:center;'>Catalogue Magasin</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Filtrez les produits par nom, capacité ou prix maximum</p>", unsafe_allow_html=True)

# Filtres utilisateur
col1, col2 = st.columns(2)
with col1:
    recherche_nom = st.text_input("Recherche par nom d'article", placeholder="ex: Galaxy, Watch...")
with col2:
    capacites = sorted(df["Capacité"].dropna().unique())
    filtre_capacite = st.selectbox("Filtrer par capacité", options=["-- Toutes --"] + capacites)

filtre_prix = st.number_input("Prix maximum", min_value=0, step=1000, format="%d")

# Application des filtres
resultats = df.copy()
if recherche_nom:
    resultats = resultats[resultats["Nom d'article"].str.contains(recherche_nom, case=False, na=False)]
if filtre_capacite != "-- Toutes --":
    resultats = resultats[resultats["Capacité"] == filtre_capacite]
if filtre_prix > 0:
    resultats = resultats[resultats["Prix"] <= filtre_prix]

# Affichage des résultats
if not resultats.empty:
    st.success(f"{len(resultats)} article(s) trouvé(s)")
    st.dataframe(resultats, use_container_width=True)

    # Bouton de téléchargement
    buffer = BytesIO()
    resultats.to_excel(buffer, index=False)
    st.download_button(
        label="Exporter les résultats en Excel",
        data=buffer.getvalue(),
        file_name="resultats_filtrés.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("Aucun article ne correspond aux critères.")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:small;'>App locale - Export disponible</p>", unsafe_allow_html=True)
