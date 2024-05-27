import flet as ft
import subprocess


def main(page: ft.Page):
    # Fonction pour exécuter le script Python
    def on_button_click(e):
        # La commande à exécuter
        commande = ['python', 'main.py']

        # Exécuter la commande
        resultat = subprocess.run(commande, capture_output=True, text=True)

    # Création du bouton
    bouton = ft.ElevatedButton(
        text="Exécuter le script", on_click=on_button_click)

    # Ajouter les widgets à la page
    page.add(bouton)


# Exécuter l'application Flet
ft.app(target=main)
