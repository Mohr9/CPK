#import 
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

### Mise en page


def load_data(uploaded_file):
    """Charge un fichier CSV ou Excel et retourne un DataFrame."""
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            return pd.read_excel(uploaded_file)
    return None

def display_dataframe(df):
    """Affiche les premières lignes du DataFrame."""
    st.write("### Aperçu du DataFrame")
    st.write(df.head())

def select_column(df):
    """Permet à l'utilisateur de choisir une colonne."""
    return st.selectbox("Sélectionnez une colonne", df.columns)



def calcul_CPK(df, column):
    """Affiche des informations et statistiques sur la colonne sélectionnée."""
    st.write(f"Statistiques de la colonne **{column}**")


    #moyenne std :
    means = df[column].mean()
    std_dev = np.std(df[column], ddof = 1)

    #CPK :
    LSL = 1.5  # Limite inférieure
    USL = 50  # Limite supérieure

    # Calcul du Cpk
    cpk = np.minimum((means - LSL) / (3 * std_dev), (USL - means) / (3 * std_dev))

    lim_basse = means - 3* std_dev
    lim_haute = means + 3*std_dev
    
    st.write(f"**Moyenne :** {means:.3f}")
    st.write(f"**Std :** {std_dev:.3f}")
    st.write(f"**CPK :** {cpk:.3f}")
    
    
    plt.figure(figsize=(8,6))
    plt.grid()
    
    #xcol = st.selectbox("Sélectionnez l'axe x", df.columns)
    #ycol = st.selectbox("Sélectionnez l'axe y", df.columns)
    
    
    
    plt.title(f"Cpk = {cpk:.3f}")

        # Tracer les données
    abs = [i+1 for i in range(df[column].shape[0])]
    ax = sns.lineplot(x=abs, y=df[column])

        # Ajouter les limites LSL et USL
    ax.axhline(1.5, color="red", linestyle="-", label="LSL (1.5)")
    ax.axhline(lim_basse, c = "red", label = "Limite basse",linestyle = "--")
    ax.axhline(lim_haute, c = "red", label = "Limite haute",linestyle = "--")

        # Ajuster les limites de l'axe Y
    plt.ylim(0, 7)

        # Afficher la légende
    plt.legend()

        # Affichage du graphique dans Streamlit
    st.pyplot(plt)
    
    



### --- Interface Streamlit ---
st.title("Calcul CPK")

uploaded_file = st.file_uploader("Importez un fichier CSV ou Excel", type=["csv", "xlsx"])
df = load_data(uploaded_file)



if df is not None:
    display_dataframe(df)
    column = select_column(df)  # Retappez cette ligne manuellement
    if st.button("Calculer le CPK"):
        if column is not None:
            calcul_CPK(df, column)
        else:
            st.write("Veuillez sélectionner une colonne.")

