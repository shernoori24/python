import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Configuration améliorée
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'figure.figsize': (12, 7),
    'axes.titlesize': 16,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10
})

def load_and_clean_data(filename):
    """Charge et nettoie les données Steam de manière robuste"""
    try:
        df = pd.read_csv(filename, parse_dates=['date_release'])
        
        # Conversion et nettoyage des colonnes critiques
        numeric_cols = ['price_final', 'positive_ratio', 'user_reviews']
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        # Filtrage avancé
        df = df[
            (df['price_final'].between(0, 100)) &
            (df['positive_ratio'].between(0, 100)) &
            (df['user_reviews'] > 0)
        ].copy()
        
        # Feature engineering
        df['release_year'] = df['date_release'].dt.year
        df['recommendation_score'] = (df['positive_ratio'] * df['user_reviews']) / 1000
        
        return df.dropna(subset=numeric_cols)
    
    except Exception as e:
        print(f"Erreur lors du chargement: {str(e)}")
        return None

def generate_visualizations(df):
    """Génère les visualisations avec des améliorations"""
    
    # 1. Top 10 des jeux (combinaison ratio + nombre avis)
    plt.figure(figsize=(12, 8))
    top_df = df.nlargest(10, 'recommendation_score')
    sns.barplot(x='recommendation_score', y='title', data=top_df, palette="rocket")
    plt.title("Top 10 des jeux Steam\n(Score = Ratio Positif × Nombre Avis)", pad=20)
    plt.xlabel("Score de Recommendation")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig('top_jeux.png', dpi=120, bbox_inches='tight')
    plt.close()
    
    # 2. Distribution des prix (avec zoom sur la plage principale)
    plt.figure(figsize=(12, 6))
    sns.histplot(df['price_final'], bins=30, kde=True, color='skyblue')
    plt.title("Distribution des Prix des Jeux Steam", pad=15)
    plt.xlabel("Prix Final (€)")
    plt.ylabel("Nombre de Jeux")
    plt.xlim(0, 50)
    plt.grid(True, alpha=0.3)
    plt.savefig('prix_distribution.png', dpi=120)
    plt.close()
    
    # 3. Corrélation prix-recommandation (avec régression)
    plt.figure(figsize=(12, 6))
    sns.regplot(x='price_final', y='positive_ratio', data=df, 
                scatter_kws={'alpha':0.4}, line_kws={'color':'red'})
    plt.title("Relation entre Prix et Taux de Recommendation", pad=15)
    plt.xlabel("Prix Final (€)")
    plt.ylabel("Taux de Recommendation (%)")
    plt.grid(True, alpha=0.3)
    plt.savefig('correlation.png', dpi=120)
    plt.close()
    
    # 4. Bonus: Evolution dans le temps (non demandé mais utile)
    if 'release_year' in df.columns:
        plt.figure(figsize=(12, 6))
        yearly = df.groupby('release_year')['price_final'].mean()
        yearly.plot(marker='o')
        plt.title("Evolution du Prix Moyen par Année de Sortie", pad=15)
        plt.xlabel("Année de Sortie")
        plt.ylabel("Prix Moyen (€)")
        plt.grid(True, alpha=0.3)
        plt.savefig('evolution_prix.png', dpi=120)
        plt.close()

def analyze_data(df):
    """Effectue l'analyse quantitative"""
    analysis = {
        'nb_jeux': len(df),
        'prix_moyen': df['price_final'].mean(),
        'prix_median': df['price_final'].median(),
        'ratio_moyen': df['positive_ratio'].mean(),
        'jeu_plus_recommandé': df.loc[df['positive_ratio'].idxmax()]['title'],
        'correlation': df[['price_final', 'positive_ratio']].corr().iloc[0,1]
    }
    return analysis

def main():
    print(f"\n{' Analyse des Données Steam ':=^80}")
    print(f"Date d'exécution: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    df = load_and_clean_data('steam_games.csv')
    if df is None:
        return
    
    # Analyse
    results = analyze_data(df)
    
    print("\n=== Résultats Clés ===")
    print(f"1. Jeu le plus recommandé: {results['jeu_plus_recommandé']}")
    print(f"2. Prix moyen: {results['prix_moyen']:.2f}€ (médiane: {results['prix_median']:.2f}€)")
    print(f"3. Fourchette de prix courante: {df['price_final'].mode()[0]}€")
    print(f"4. Corrélation prix-recommandation: {results['correlation']:.2f}")
    
    # Visualisations
    generate_visualizations(df)
    
    print("\n=== Visualisations Générées ===")
    print("- top_jeux.png (Top 10 des jeux recommandés)")
    print("- prix_distribution.png (Distribution des prix)")
    print("- correlation.png (Relation prix-recommandation)")
    print("- evolution_prix.png (Bonus: Evolution temporelle)")
    
    print("\nAnalyse terminée avec succès!")

if __name__ == "__main__":
    main()