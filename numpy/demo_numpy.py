import pandas as pd
import numpy as np
import ast

# 1. Charger le fichier CSV
df = pd.read_csv("etudiants_personnes_generes.csv")

# 2. Filtrer les étudiants uniquement
df_etudiants = df[df['Type'] == 'Etudiant'].copy()

# 3. Convertir les colonnes de notes (chaînes) en vraies listes Python
df_etudiants['Notes'] = df_etudiants['Notes'].apply(ast.literal_eval)

# 4. Convertir en tableau NumPy
notes_array = np.array(df_etudiants['Notes'].tolist())

# 5. Récupérer les moyennes sous forme de tableau NumPy
moyennes = df_etudiants['Moyenne'].to_numpy()

# 6. Calcul des statistiques
moyenne_generale = np.mean(moyennes)
mediane = np.median(moyennes)
ecart_type = np.std(moyennes)

# 7. Filtrer les étudiants ayant une moyenne > 15
etudiants_sup_15 = df_etudiants[df_etudiants['Moyenne'] > 15]

# 8. Affichage des résultats
print("Moyenne générale :", moyenne_generale)
print("Médiane :", mediane)
print("Écart-type :", ecart_type)
print("\nÉtudiants ayant une moyenne > 15 :")
print(etudiants_sup_15[['Nom', 'Moyenne']])
