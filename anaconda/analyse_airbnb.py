import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuration des graphiques
sns.set_theme(style="whitegrid", palette="husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14

def load_and_clean_data(filename):
    """Charge et nettoie les données Airbnb"""
    # Chargement des données
    df = pd.read_csv(filename)
    
    # Nettoyage des données
    # Conversion de la colonne prix en numérique et suppression des valeurs manquantes
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
    df = df.dropna(subset=['price'])
    
    # Suppression des prix aberrants (0 ou > 5000)
    df = df[(df['price'] > 0) & (df['price'] < 5000)]
    
    # Nettoyage des noms de quartiers et types de logement
    df['neighbourhood'] = df['neighbourhood'].str.strip()
    df['room_type'] = df['room_type'].str.strip()
    
    return df

def generate_visualizations(df):
    """Génère les visualisations des données Airbnb"""
    
    # 1. Distribution des prix
    plt.figure()
    sns.histplot(df['price'], bins=50, kde=True)
    plt.title('Distribution des prix des logements Airbnb')
    plt.xlabel('Prix (CHF/nuit)')
    plt.ylabel('Nombre de logements')
    plt.xlim(0, 1000)
    plt.tight_layout()
    plt.savefig('distribution_prix.png')
    plt.close()
    
    # 2. Prix par type de logement
    plt.figure()
    sns.boxplot(x='room_type', y='price', data=df, showfliers=False)
    plt.title('Prix par type de logement')
    plt.xlabel('Type de logement')
    plt.ylabel('Prix (CHF/nuit)')
    plt.ylim(0, 500)
    plt.tight_layout()
    plt.savefig('prix_par_type.png')
    plt.close()
    
    # 3. Top 10 des quartiers les plus chers
    plt.figure()
    quartiers_prix = df.groupby('neighbourhood')['price'].mean().nlargest(10)
    sns.barplot(x=quartiers_prix.values, y=quartiers_prix.index, orient='h')
    plt.title('Top 10 des quartiers les plus chers')
    plt.xlabel('Prix moyen (CHF/nuit)')
    plt.ylabel('Quartier')
    plt.tight_layout()
    plt.savefig('top10_quartiers_chers.png')
    plt.close()

def main():
    try:
        # Chargement et nettoyage des données
        df = load_and_clean_data('listings.csv')
        
        # Affichage des informations de base
        print("\n=== Statistiques de base ===")
        print(f"Nombre de logements analysés: {len(df)}")
        print(f"Prix moyen: {df['price'].mean():.2f} CHF")
        print(f"Prix médian: {df['price'].median():.2f} CHF")
        print("\nTypes de logements disponibles:")
        print(df['room_type'].value_counts())
        
        # Génération des visualisations
        generate_visualizations(df)
        print("\nVisualisations générées avec succès:")
        print("- distribution_prix.png")
        print("- prix_par_type.png")
        print("- top10_quartiers_chers.png")
        
    except FileNotFoundError:
        print("Erreur: Le fichier 'listings.csv' n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur s'est produite: {str(e)}")


main()