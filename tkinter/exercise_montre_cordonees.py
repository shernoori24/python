import tkinter as tk
from tkinter import messagebox

# Fonction appelée lors du clic sur le bouton
def afficher_infos():
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    email = entry_email.get()

    infos = f"Nom : {nom}\nPrénom : {prenom}\nEmail : {email}"
    messagebox.showinfo("Informations saisies", infos)
    messagebox.showinfo("Informations saisies", "vous aves bien lu les info")

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Formulaire d'informations")
fenetre.geometry("300x250")

# Widgets de saisie
label_nom = tk.Label(fenetre, text="Nom:")
label_nom.pack(pady=5)
entry_nom = tk.Entry(fenetre)
entry_nom.pack()

label_prenom = tk.Label(fenetre, text="Prénom:")
label_prenom.pack(pady=5)
entry_prenom = tk.Entry(fenetre)
entry_prenom.pack()

label_email = tk.Label(fenetre, text="Email:")
label_email.pack(pady=5)
entry_email = tk.Entry(fenetre)
entry_email.pack()

# Bouton pour afficher les infos
bouton = tk.Button(fenetre, text="Afficher mes infos", command=afficher_infos)
bouton.pack(pady=20)

# Boucle principale 
fenetre.mainloop()
 