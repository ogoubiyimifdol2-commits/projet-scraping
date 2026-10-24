"""Point d'entrée principal de l'application de scraping.

Ce script lance l'orchestrateur du projet (ControleurPrincipal) qui
exécute l'ensemble du cycle de manière 100% automatique : scraping des objets
électroniques (Téléphones, MacBook, AirPods), téléchargement des photos,
base de données SQLite, export CSV et rapport statistique.
"""

import sys
from controllers.controleur import ControleurPrincipal


def main() -> None:
    """Fonction principale de démarrage."""
    try:
        controleur = ControleurPrincipal()
        controleur.executer()
    except KeyboardInterrupt:
        print("\n[INFO] Programme interrompu par l'utilisateur.")
        sys.exit(0)
    except Exception as erreur:
        print(f"\n[ERREUR IMPRÉVUE] {erreur}")
        sys.exit(1)


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
