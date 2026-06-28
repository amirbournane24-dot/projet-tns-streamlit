
import sys
import os
import time

# ==========================================================
# PROJET : Simulation temps réel de signaux
# VERSION 6 : Surveillance du temps réel
# Fichier : client.py
# Rôle : client
# ==========================================================


FICHIER_ECHANGE = "echange.txt"


commandes_valides = [
    "debut",
    "fin",
    "arret",

    "tirage",
    "reponse",

    "sinus",
    "carre",
    "rampe",
    "bruit",

    "surveillance",
    "reset"
]


if len(sys.argv) < 2:
    print("VERSION 6 : Surveillance du temps réel")
    print()
    print("Utilisation : python client.py commande")
    print()
    print("Commandes disponibles :")
    print("  debut        : lancer la simulation")
    print("  fin          : mettre la simulation en pause")
    print("  arret        : arrêter complètement le serveur")
    print("  tirage       : tirer une nouvelle fréquence")
    print("  reponse      : afficher les paramètres temps réel")
    print("  sinus        : choisir un signal sinusoïdal")
    print("  carre        : choisir un signal carré")
    print("  rampe        : choisir un signal rampe")
    print("  bruit        : choisir un bruit blanc")
    print("  surveillance : activer le mode surveillance")
    print("  reset        : remettre les compteurs à zéro")
    sys.exit()


commande = sys.argv[1].lower()


if commande not in commandes_valides:
    print("Commande invalide :", commande)
    print("Commandes possibles :")
    print("debut, fin, arret, tirage, reponse, sinus, carre, rampe, bruit, surveillance, reset")
    sys.exit()


while True:
    if not os.path.exists(FICHIER_ECHANGE):
        with open(FICHIER_ECHANGE, "w", encoding="utf-8") as f:
            f.write("")
        break

    with open(FICHIER_ECHANGE, "r", encoding="utf-8") as f:
        contenu = f.read().strip()

    if contenu == "":
        break

    time.sleep(0.1)


with open(FICHIER_ECHANGE, "w", encoding="utf-8") as f:
    f.write(commande)


print("VERSION 6 : Surveillance du temps réel")
print("Commande envoyée :", commande)
