import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import ast

def charger_fichier():
    chemin = filedialog.askopenfilename(filetypes=[("Fichier CSV", "*.csv")])
    if chemin:
        try:
            df = pd.read_csv(chemin)
            df_etudiants = df[df['Type'] == 'Etudiant'].copy()
            df_etudiants['Notes'] = df_etudiants['Notes'].apply(ast.literal_eval)

            moyennes = df_etudiants['Moyenne'].to_numpy()

            moyenne_generale = np.mean(moyennes)
            mediane = np.median(moyennes)
            ecart_type = np.std(moyennes)

            etudiants_sup_15 = df_etudiants[df_etudiants['Moyenne'] > 15]

            resultats = f"Moyenne générale : {moyenne_generale:.2f}\n"
            resultats += f"Médiane : {mediane:.2f}\n"
            resultats += f"Écart-type : {ecart_type:.2f}\n\n"
            resultats += "Étudiants avec moyenne > 15 :\n"

            for _, row in etudiants_sup_15.iterrows():
                resultats += f"- {row['Nom']} ({row['Moyenne']})\n"

            texte_resultat.delete("1.0", tk.END)
            texte_resultat.insert(tk.END, resultats)

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite :\n{e}")

# Création de la fenêtre
fenetre = tk.Tk()
fenetre.title("Analyse des notes des étudiants")
fenetre.geometry("500x500")

# Bouton pour charger le fichier
btn_charger = tk.Button(fenetre, text="Charger le fichier CSV", command=charger_fichier)
btn_charger.pack(pady=10)

# Zone d'affichage des résultats
texte_resultat = tk.Text(fenetre, height=25, width=60)
texte_resultat.pack(padx=10, pady=10)

# Lancer l'application
fenetre.mainloop()
