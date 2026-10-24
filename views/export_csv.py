"""Exportation des données au format CSV (Vue).

Ce module implémente la classe ExportCsv pour sauvegarder les données
extraites dans un fichier CSV avec encodage utf-8-sig et séparateur ';'.
"""

import csv
from pathlib import Path
from typing import List, Optional

from config import CHEMIN_CSV
from models.produit import Produit


class ExportCsv:
    """Gère l'export des objets Produit au format CSV."""

    COLONNES = [
        "nom",
        "prix",
        "categorie",
        "description",
        "note",
        "nb_avis",
        "url_produit",
        "url_image",
        "chemin_image",
    ]

    def __init__(self, chemin_fichier: Optional[Path] = None):
        """Initialise l'exportateur avec le chemin cible."""
        self.chemin_fichier = Path(chemin_fichier or CHEMIN_CSV)
        self.chemin_fichier.parent.mkdir(parents=True, exist_ok=True)

    def exporter(self, produits: List[Produit]) -> Path:
        """Exporte la liste de produits dans le fichier CSV.

        Utilise l'encodage utf-8-sig (compatibilité Excel immédiate sous Windows)
        et le point-virgule comme séparateur de colonnes.

        :param produits: Liste d'instances de Produit.
        :return: Chemin du fichier CSV généré.
        """
        with open(
            self.chemin_fichier,
            mode="w",
            encoding="utf-8-sig",
            newline="",
        ) as fichier_csv:
            redacteur = csv.DictWriter(
                fichier_csv,
                fieldnames=self.COLONNES,
                delimiter=";",
            )
            # Écriture de la ligne d'en-têtes
            redacteur.writeheader()

            # Écriture des données
            for produit in produits:
                redacteur.writerow(produit.vers_dict())

        return self.chemin_fichier
