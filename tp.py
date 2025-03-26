import io
import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

# Titre de l'application
st.title("Analyse des données de ventes par région")

# Chargement des données
st.header("Chargement des données")
filename = 'BeansDataSet.csv'

try:
    data = pd.read_csv(filename)
    st.success("Dataset chargé avec succès")
except Exception as e:
    st.error(f"Échec du chargement des données : {e}")
    st.stop()

# Affichage d'un aperçu des données
st.subheader("Aperçu des données")
st.write(data.head(5), " - Les 5 premières lignes")
st.write(data.tail(5), " - Les 5 dernières lignes")
st.write(f"Dimensions des données : {data.shape[0]} lignes et {data.shape[1]} colonnes")


# Statistiques descriptives
st.subheader("Statistiques descriptives")
st.write(data.describe(include='all'))

# Transactions par région
st.subheader("Transactions par région")
region_counts = data['Region'].value_counts()
st.write(region_counts)

# Moyenne des ventes par région
st.subheader("Moyenne des ventes par région")
try:
    mean_sales = data.groupby('Region').mean(numeric_only=True)
    st.write(mean_sales)
except Exception as e:
    st.error(f"Erreur lors du calcul des moyennes : {e}")

# Somme des ventes par région
st.subheader("Somme des ventes par région")
try:
    sum_sales = data.groupby('Region').sum(numeric_only=True)
    sum_sales['Total'] = sum_sales.sum(axis=1)
    st.write(sum_sales)
except Exception as e:
    st.error(f"Erreur lors du calcul des sommes : {e}")

# Visualisation des données
st.header("Visualisation des données")

# Graphique des ventes moyennes par région
st.subheader("Ventes moyennes par région")
try:
    fig1, ax1 = plt.subplots(figsize=(9, 6))
    mean_sales.reset_index().plot(
        x='Region',
        kind='bar',
        ax=ax1,
        title="Moyenne des ventes par région"
    )
    st.pyplot(fig1)
except Exception as e:
    st.error(f"Erreur lors de la création du graphique des moyennes : {e}")

# Graphique des ventes totales par région
st.subheader("Ventes totales par région")
try:
    fig2, ax2 = plt.subplots(figsize=(9, 6))
    sum_sales.reset_index().plot(
        x='Region',
        kind='bar',
        ax=ax2,
        title="Somme des ventes par région"
    )
    st.pyplot(fig2)
except Exception as e:
    st.error(f"Erreur lors de la création du graphique des totaux : {e}")

# ✅ Matrice de corrélation
st.subheader('Matrice de Corrélation entre produits')
try:
    fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
    corr_matrix = data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].corr()
    sn.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax_corr)
    st.pyplot(fig_corr)
except Exception as e:
    st.error(f"Erreur lors de la matrice de corrélation : {e}")

# ✅ Boîtes à moustaches
st.subheader('Boîtes à moustaches des ventes')

try:
    fig_box, ax_box = plt.subplots(figsize=(15, 10))
    data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].plot(
        kind='box', subplots=False, ax=ax_box, layout=(2, 3), sharex=False, sharey=False)
    st.pyplot(fig_box)
except Exception as e:
    st.error(f"Erreur lors des boîtes à moustaches : {e}")

# ✅ Graphiques de densité
st.subheader('Graphiques de densité des ventes')
try:
    fig_density, ax_density = plt.subplots(figsize=(15, 10))
    data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].plot(
        kind='density', subplots=False, ax=ax_density)
    st.pyplot(fig_density)
except Exception as e:
    st.error(f"Erreur lors des graphiques de densité : {e}")


st.subheader('Pairplot')
graphe = sn.pairplot(data)
st.pyplot(graphe.fig)

st.subheader('Pairplot Arabica vs Espresso (hue Cappuccino)')    
graphe2=sn.pairplot(data,hue='Cappuccino',vars=['Arabica','Espresso'])
st.pyplot(graphe2.fig)


# Répartition des ventes pour une région
st.subheader("Répartition des ventes pour une région")
region_choice = st.selectbox("Choisissez une région :", sum_sales.index)
try:
    selected_region = sum_sales.loc[region_choice].drop('Total').sort_values(ascending=False)
    fig3, ax3 = plt.subplots()
    selected_region.plot.pie(
        autopct='%1.1f%%',
        startangle=30,
        ax=ax3,
        title=f"Répartition des ventes pour {region_choice}"
    )
    st.pyplot(fig3)
except Exception as e:
    st.error(f"Erreur lors de la création du graphique circulaire : {e}")

# Analyse des ventes par channel
st.subheader("Ventes par channel")
try:
    df_channel = data.drop('Region', axis=1).groupby('Channel').mean(numeric_only=True)
    df_channel['Total'] = df_channel.sum(axis=1)
    st.write(df_channel)

    # Graphique des ventes par channel
    fig4, ax4 = plt.subplots(figsize=(9, 6))
    df_channel.drop('Total', axis=1).reset_index().plot(
        x='Channel',
        kind='bar',
        ax=ax4,
        title="Ventes par channel"
    )
    st.pyplot(fig4)
except Exception as e:
    st.error(f"Erreur lors de l'analyse des ventes par channel : {e}")

st.write("Analyse terminée avec succès !")
