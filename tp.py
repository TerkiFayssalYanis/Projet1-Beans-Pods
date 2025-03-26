import io
import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

# Titre de l'application
st.title("Analyse des données de ventes par région")

# Menu de navigation
menu = st.sidebar.selectbox('Navigation', ['Aperçu des données', 'Visualisation', 'Analyse en Texte'])

# Chargement des données (toujours disponible)
filename = 'BeansDataSet.csv'
data = pd.read_csv(filename)

if menu == 'Aperçu des données':
    st.header("Chargement des données")
    st.success("Sucess de lecture ")

    # Affichage d'un aperçu des données
    st.subheader("Aperçu des données")
    st.write(data.head(5), " - Les 5 premières lignes")
    st.write(data.tail(5), " - Les 5 dernières lignes")
    st.write(f"Dimensions: {data.shape[0]} lignes et {data.shape[1]} colonnes")

    st.subheader("Statistiques descriptives")
    st.write(data.describe())

    st.subheader("Transactions par région")
    region_counts = data['Region'].value_counts()
    st.write(region_counts)

    st.subheader("Moyenne des ventes par région")
    try:
        mean_sales = data.groupby('Region').mean(numeric_only=True)
        st.write(mean_sales)
    except Exception as e:
        st.error(f"Erreur lors du calcul des moyennes : {e}")

    st.subheader("Somme des ventes par région")
    try:
        sum_sales = data.groupby('Region').sum(numeric_only=True)
        sum_sales['Total'] = sum_sales.sum(axis=1)
        st.write(sum_sales)
    except Exception as e:
        st.error(f"Erreur lors du calcul des sommes : {e}")

elif menu == 'Visualisation':
    st.header("Visualisation des données")

    st.subheader("Ventes moyennes par région")
    try:
        fig1, ax1 = plt.subplots(figsize=(9, 6))
        mean_sales = data.groupby('Region').mean(numeric_only=True)
        mean_sales.reset_index().plot(x='Region', kind='bar', ax=ax1, title="Moyenne des ventes par région")
        st.pyplot(fig1)
    except Exception as e:
        st.error(f"Erreur lors de la création du graphique des moyennes : {e}")

    st.subheader("Ventes totales par région")
    try:
        fig2, ax2 = plt.subplots(figsize=(9, 6))
        sum_sales = data.groupby('Region').sum(numeric_only=True)
        sum_sales.reset_index().plot(
            x='Region',
            kind='bar',
            ax=ax2,
            title="Somme des ventes par région"
        )
        st.pyplot(fig2)
    except Exception as e:
        st.error(f"Erreur lors de la création du graphique des totaux : {e}")

    st.subheader('Matrice de Corrélation entre produits')
    try:
        fig_corr, ax_corr = plt.subplots(figsize=(10, 6))
        corr_matrix = data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].corr()
        sn.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax_corr)
        st.pyplot(fig_corr)
    except Exception as e:
        st.error(f"Erreur lors de la matrice de corrélation : {e}")

    st.subheader('Boîtes à moustaches des ventes')
    try:
        fig_box, ax_box = plt.subplots(figsize=(15, 10))
        data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].plot(
            kind='box', subplots=False, ax=ax_box, layout=(2, 3), sharex=False, sharey=False)
        st.pyplot(fig_box)
    except Exception as e:
        st.error(f"Erreur lors des boîtes à moustaches : {e}")

    st.subheader('Graphiques de densité des ventes')
    try:
        fig_density, ax_density = plt.subplots(figsize=(15, 10))
        data[['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']].plot(
            kind='density', subplots=False, ax=ax_density)
        st.pyplot(fig_density)
    except Exception as e:
        st.error(f"Erreur {e}")

    st.subheader('Pairplot')
    graphe = sn.pairplot(data)
    st.pyplot(graphe.fig)

    st.subheader('Pairplot Arabica vs Espresso (hue Cappuccino)')    
    graphe2 = sn.pairplot(data, hue='Cappuccino', vars=['Arabica', 'Espresso'])
    st.pyplot(graphe2.fig)

    st.subheader("Répartition des ventes pour une région")
    try:
        sum_sales = data.groupby('Region').sum(numeric_only=True)  # Calculé ici pour éviter l'erreur
        region_choice = st.selectbox("Choisissez une région :", sum_sales.index)
        selected_region = sum_sales.loc[region_choice].drop('Total', errors='ignore').sort_values(ascending=False)
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

    st.subheader("Ventes par channel")
    try:
        df_channel = data.drop('Region', axis=1).groupby('Channel').mean(numeric_only=True)
        df_channel['Total'] = df_channel.sum(axis=1)
        st.write(df_channel)

        fig4, ax4 = plt.subplots(figsize=(9, 6))
        df_channel.drop('Total', axis=1).reset_index().plot(
            x='Channel',
            kind='bar',
            ax=ax4,
            title="Ventes par channel"
        )
        st.pyplot(fig4)
    except Exception as e:
        st.error(f"Erreur lors de l'analyse : {e}")

elif menu == 'Analyse en Texte':
    st.write("""Dans le fichier CSV, il y a 368 lignes avec 6 colonnes de chiffres qui représentent des ventes, et j’ai analysé ça pour un petit projet d’élève. D’après l’aperçu des données et la visualisation, on remarque que les ventes bougent énormément d’une ligne à l’autre, sans vraiment de rythme clair. Par rapport aux régions, presque toutes les ventes viennent du Sud, avec juste quelques lignes pour le Nord et le Centre, donc le Sud domine largement. Les premières ventes qu’on voit, comme dans la ligne avec 12 669, 9 656, 7 561, 214, 2 674 et 1 338, sont assez solides, surtout dans les premières colonnes, mais pas les plus hautes du fichier. Les dernières ventes, comme dans la ligne avec 2 787, 1 698, 2 510, 65, 477 et 52, sont beaucoup plus faibles, montrant une grosse baisse par rapport à d’autres moments. En moyenne, certaines colonnes sont plus fortes : la première fait environ 15 800 par ligne, la troisième 13 600, la deuxième 10 400, la cinquième 6 000, la quatrième 3 800 et la sixième 2 200, mais ces chiffres cachent des écarts énormes. Par exemple, une ligne avec 26 373, 36 423, 22 019, 5 154, 4 337 et 16 523 montre un pic incroyable, avec la plus grosse vente dans la dernière colonne (16 523), alors qu’une autre, comme 403, 254, 610, 774, 54, 63, est presque à zéro. Les ventes grimpent parfois à des sommets, comme 92 780 ou 55 571, et chutent à presque rien, comme 3 ou 9, ce qui fait penser que ça dépend de trucs qu’on ne voit pas, peut-être le jour ou un événement spécial. La dernière colonne reste souvent plus basse, avec un maximum à 16 523, tandis que les autres montent plus haut. Bref, les ventes sont super irrégulières, avec des hauts impressionnants et des bas très marqués.""")
