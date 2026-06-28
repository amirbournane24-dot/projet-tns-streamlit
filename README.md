# Simulation temps réel de signaux

Ce projet présente une application Python de simulation temps réel de signaux et de traitement numérique du signal.

## Version finale Streamlit

Le fichier `app.py` contient la version finale de l'application développée avec Streamlit.

Cette version permet de :
- générer différents signaux ;
- ajouter un bruit blanc gaussien ;
- appliquer un filtrage passe-bas ;
- réaliser une analyse fréquentielle du signal d'entrée par FFT ;
- surveiller le temps de calcul ;
- afficher les résultats dans une interface web interactive.

## Versions locales

Le dossier `versions_locales` contient les premières versions locales du projet :

- `client.py` : envoi des commandes utilisateur ;
- `simulation.py` : exécution de la simulation ;
- `echange.txt` : fichier utilisé pour la communication entre le client et le serveur.

Ces fichiers correspondent à la phase de développement local avant la réorganisation du projet dans l'application finale Streamlit.

## Dépendances

Les bibliothèques nécessaires sont indiquées dans le fichier `requirements.txt`.
