"""Téléchargement et gestion des photos des produits.

Ce module télécharge les images dans le dossier data/images/ en utilisant
la bibliothèque requests, avec un User-Agent identifiable, une pause entre
chaque requête et une gestion robuste des erreurs.
"""

import time
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

import requests

from config import DOSSIER_IMAGES, PAUSE_SECONDES, USER_AGENT
from models.produit import Produit


class TelechargeurImages:
    """Gère le téléchargement local des visuels de produits."""

    def __init__(
        self,
        dossier_destination: Path = DOSSIER_IMAGES,
        pause: float = PAUSE_SECONDES,
    ):
        """Initialise le gestionnaire d'images.

        :param dossier_destination: Répertoire où enregistrer les images.
        :param pause: Temps d'attente (en secondes) entre deux téléchargements.
        """
        self.dossier_destination = Path(dossier_destination)
        self.dossier_destination.mkdir(parents=True, exist_ok=True)
        self.pause = pause
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Referer": "https://www.amazon.fr/",
        })

    def _obtenir_nom_fichier(self, url_image: str, index: int) -> str:
        """Génère un nom de fichier local propre et unique pour l'image."""
        nom_origine = Path(urlparse(url_image).path).name
        if not nom_origine:
            nom_origine = "image.png"
        return f"{index:03d}_{nom_origine}"

    def telecharger_une_image(self, url_image: str, index: int) -> Optional[str]:
        """Télécharge une image individuelle depuis son URL.

        :param url_image: URL complète de l'image.
        :param index: Identifiant pour préserver l'unicité du fichier.
        :return: Chemin relatif ou absolu du fichier téléchargé, ou None en cas d'échec.
        """
        if not url_image:
            return None

        nom_fichier = self._obtenir_nom_fichier(url_image, index)
        chemin_fichier = self.dossier_destination / nom_fichier

        # Si l'image a déjà été téléchargée, on réutilise le fichier existant
        if chemin_fichier.exists() and chemin_fichier.stat().st_size > 0:
            return str(chemin_fichier)

        try:
            reponse = self.session.get(url_image, timeout=10)
            reponse.raise_for_status()

            with open(chemin_fichier, "wb") as fichier:
                fichier.write(reponse.content)

            # Pause éthique entre deux téléchargements d'images
            time.sleep(self.pause)
            return str(chemin_fichier)

        except Exception as erreur:
            print(f"  [Avertissement] Échec téléchargement image '{url_image}': {erreur}")
            return None

    def telecharger_images_produits(self, produits: List[Produit]) -> int:
        """Télécharge les images de toute la liste de produits et met à jour chemin_image.

        :param produits: Liste d'instances de Produit.
        :return: Nombre d'images correctement associées.
        """
        print(f"\n[Images] Début du téléchargement des images ({len(produits)} produits)...")
        succes = 0

        for index, produit in enumerate(produits, start=1):
            if produit.url_image:
                chemin = self.telecharger_une_image(produit.url_image, index)
                if chemin:
                    produit.chemin_image = chemin
                    succes += 1

        print(f"[Images] Téléchargement terminé : {succes}/{len(produits)} images traitées.")
        return succes
