
import os
import time
import random
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# PROJET : Simulation temps réel de signaux
# VERSION 6 : Surveillance du temps réel
#
# Objectif :
# - mesurer le temps de calcul de chaque boucle ;
# - comparer ce temps avec la période attendue ;
# - compter les dépassements ;
# - afficher une courbe de surveillance du temps réel.
# ==========================================================


# ==========================================================
# PARAMÈTRES GÉNÉRAUX
# ==========================================================

FICHIER_ECHANGE = "echange.txt"

# Fréquence d'affichage souhaitée
fe = 10
periode = 1 / fe

amplitude = 1
valeurs_frequence = [0.5, 1.0, 2.0]
f0 = random.choice(valeurs_frequence)

type_signal = "sinus"


# ==========================================================
# CRÉATION DU FICHIER D'ÉCHANGE
# ==========================================================

with open(FICHIER_ECHANGE, "w", encoding="utf-8") as f:
    f.write("")


# ==========================================================
# VARIABLES D'ÉTAT
# ==========================================================

simulation_active = False
programme_actif = True

t = 0.0
numero_echantillon = 0
nombre_depassements = 0

temps_affiches = []
signal_affiche = []

indices_boucles = []
temps_calculs = []


# ==========================================================
# INTERFACE GRAPHIQUE VERSION 6
# ==========================================================

plt.ion()

fig, (ax_signal, ax_temps) = plt.subplots(2, 1, figsize=(10, 7))
fig.canvas.manager.set_window_title("Version 6 - Surveillance du temps réel")

courbe_signal, = ax_signal.plot([], [], "-", linewidth=2, label="Signal")
courbe_temps, = ax_temps.plot([], [], "-", linewidth=2, label="Temps de calcul")
ligne_limite = ax_temps.axhline(periode, linestyle="--", linewidth=2, label="Période limite")

ax_signal.set_title("Signal simulé en temps réel")
ax_signal.set_xlabel("Temps (s)")
ax_signal.set_ylabel("Amplitude")
ax_signal.set_ylim(-1.5, 1.5)
ax_signal.grid(True)
ax_signal.legend()

ax_temps.set_title("Surveillance du temps réel")
ax_temps.set_xlabel("Numéro de boucle")
ax_temps.set_ylabel("Temps de calcul (s)")
ax_temps.set_ylim(0, periode * 2)
ax_temps.grid(True)
ax_temps.legend()

plt.tight_layout()


# ==========================================================
# AFFICHAGE CONSOLE
# ==========================================================

print("==================================================")
print("PROJET : Simulation temps réel de signaux")
print("VERSION 6 : Surveillance du temps réel")
print("Serveur lancé.")
print()
print("Commandes disponibles :")
print("debut, fin, arret")
print("tirage, reponse")
print("sinus, carre, rampe, bruit")
print("surveillance, reset")
print()
print("Le serveur lit le fichier echange.txt.")
print("==================================================")


# ==========================================================
# LECTURE DU FICHIER ECHANGE.TXT
# ==========================================================

def lire_message():
    if not os.path.exists(FICHIER_ECHANGE):
        return None

    with open(FICHIER_ECHANGE, "r", encoding="utf-8") as f:
        contenu = f.read().strip()

    if contenu == "":
        return None

    with open(FICHIER_ECHANGE, "w", encoding="utf-8") as f:
        f.write("")

    return contenu.lower()


# ==========================================================
# REMISE À ZÉRO
# ==========================================================

def reset_affichage():
    global numero_echantillon, nombre_depassements

    temps_affiches.clear()
    signal_affiche.clear()
    indices_boucles.clear()
    temps_calculs.clear()

    numero_echantillon = 0
    nombre_depassements = 0

    courbe_signal.set_data([], [])
    courbe_temps.set_data([], [])

    fig.canvas.draw()
    fig.canvas.flush_events()


# ==========================================================
# CALCUL DU SIGNAL
# ==========================================================

def calculer_signal(t, type_signal, f0, amplitude):
    if type_signal == "sinus":
        return amplitude * np.sin(2 * np.pi * f0 * t)

    elif type_signal == "carre":
        valeur = np.sin(2 * np.pi * f0 * t)
        if valeur >= 0:
            return amplitude
        else:
            return -amplitude

    elif type_signal == "rampe":
        periode_signal = 1 / f0
        return amplitude * (2 * ((t % periode_signal) / periode_signal) - 1)

    elif type_signal == "bruit":
        return amplitude * np.random.randn()

    else:
        return amplitude * np.sin(2 * np.pi * f0 * t)


# ==========================================================
# BOUCLE PRINCIPALE
# ==========================================================

while programme_actif:
    debut_boucle = time.time()

    message = lire_message()

    # ------------------------------------------------------
    # COMMANDES DE BASE
    # ------------------------------------------------------

    if message == "debut":
        simulation_active = True
        print("Message reçu : debut")
        print("La simulation commence.")

    elif message == "fin":
        simulation_active = False
        print("Message reçu : fin")
        print("La simulation est mise en pause.")

    elif message == "arret":
        print("Message reçu : arret")
        print("Arrêt complet du programme.")
        programme_actif = False
        break

    # ------------------------------------------------------
    # COMMANDES PARAMÈTRES
    # ------------------------------------------------------

    elif message == "tirage":
        f0 = random.choice(valeurs_frequence)
        t = 0.0
        simulation_active = False
        reset_affichage()
        print("Message reçu : tirage")
        print("Nouvelle fréquence tirée :", f0, "Hz")

    elif message == "sinus":
        type_signal = "sinus"
        t = 0.0
        simulation_active = False
        reset_affichage()
        print("Message reçu : sinus")
        print("Signal choisi : sinusoïdal")

    elif message == "carre":
        type_signal = "carre"
        t = 0.0
        simulation_active = False
        reset_affichage()
        print("Message reçu : carre")
        print("Signal choisi : carré")

    elif message == "rampe":
        type_signal = "rampe"
        t = 0.0
        simulation_active = False
        reset_affichage()
        print("Message reçu : rampe")
        print("Signal choisi : rampe")

    elif message == "bruit":
        type_signal = "bruit"
        t = 0.0
        simulation_active = False
        reset_affichage()
        print("Message reçu : bruit")
        print("Signal choisi : bruit blanc")

    # ------------------------------------------------------
    # VERSION 6 : COMMANDES SURVEILLANCE
    # ------------------------------------------------------

    elif message == "surveillance":
        t = 0.0
        simulation_active = False
        reset_affichage()
        print("Message reçu : surveillance")
        print("Mode surveillance du temps réel activé.")

    elif message == "reset":
        t = 0.0
        simulation_active = False
        reset_affichage()
        print("Message reçu : reset")
        print("Compteurs remis à zéro.")

    elif message == "reponse":
        print("Message reçu : reponse")
        print("Type de signal :", type_signal)
        print("Fréquence utilisée :", f0, "Hz")
        print("Fréquence d'affichage :", fe, "Hz")
        print("Période attendue :", periode, "s")
        print("Nombre d'échantillons :", numero_echantillon)
        print("Nombre de dépassements :", nombre_depassements)

    # ------------------------------------------------------
    # CALCUL TEMPS RÉEL
    # ------------------------------------------------------

    if simulation_active:
        x = calculer_signal(t, type_signal, f0, amplitude)

        temps_affiches.append(t)
        signal_affiche.append(x)

        temps_affiches = temps_affiches[-200:]
        signal_affiche = signal_affiche[-200:]

        courbe_signal.set_data(temps_affiches, signal_affiche)

        if t > 20:
            ax_signal.set_xlim(t - 20, t)
        else:
            ax_signal.set_xlim(0, 20)

        ax_signal.set_title(
            f"Signal temps réel : {type_signal}, f = {f0} Hz"
        )

        t += periode
        numero_echantillon += 1

    # ------------------------------------------------------
    # MESURE DU TEMPS DE CALCUL
    # ------------------------------------------------------

    temps_calcul = time.time() - debut_boucle

    if simulation_active:
        indices_boucles.append(numero_echantillon)
        temps_calculs.append(temps_calcul)

        indices_boucles = indices_boucles[-200:]
        temps_calculs = temps_calculs[-200:]

        if temps_calcul > periode:
            nombre_depassements += 1
            etat = "DEPASSEMENT"
        else:
            etat = "OK"

        courbe_temps.set_data(indices_boucles, temps_calculs)

        if len(indices_boucles) > 1:
            ax_temps.set_xlim(indices_boucles[0], indices_boucles[-1] + 1)
        else:
            ax_temps.set_xlim(0, 10)

        ax_temps.set_ylim(0, periode * 2)
        ax_temps.set_title(
            f"Surveillance temps réel : {etat} | dépassements = {nombre_depassements}"
        )

        print(
            f"n = {numero_echantillon} | "
            f"temps calcul = {temps_calcul:.4f} s | "
            f"limite = {periode:.4f} s | état = {etat}"
        )

    fig.canvas.draw()
    fig.canvas.flush_events()

    # ------------------------------------------------------
    # ATTENTE POUR RESPECTER LA PÉRIODE
    # ------------------------------------------------------

    temps_total = time.time() - debut_boucle
    temps_attente = periode - temps_total

    if temps_attente > 0:
        time.sleep(temps_attente)


# ==========================================================
# FERMETURE
# ==========================================================

plt.close(fig)

if os.path.exists(FICHIER_ECHANGE):
    os.remove(FICHIER_ECHANGE)

print("Serveur arrêté.")
