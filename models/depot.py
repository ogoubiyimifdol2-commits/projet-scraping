"""Dépôt de données pour la persistance des produits avec SQLite.

Ce module permet de stocker, lister et gérer les produits dans une base
de données locale SQLite en évitant les doublons d'URL.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, List, Optional

from config import CHEMIN_BDD
from models.produit import Produit


class Depot:
    """Gère les opérations de lecture et d'écriture en base SQLite."""

    def __init__(self, chemin_bdd: Optional[Path] = None):
        """Initialise le dépôt et crée la table si nécessaire."""
        self.chemin_bdd = str(chemin_bdd or CHEMIN_BDD)
        self.creer_table()

    @contextmanager
    def _obtenir_connexion(self) -> Generator[sqlite3.Connection, None, None]:
        """Ouvre une connexion, valide les transactions et la ferme proprement."""
        conn = sqlite3.connect(self.chemin_bdd)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def creer_table(self) -> None:
        """Crée la table des produits si elle n'existe pas encore."""
        sql = """
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prix REAL NOT NULL,
            categorie TEXT NOT NULL,
            description TEXT,
            note INTEGER,
            nb_avis INTEGER,
            url_produit TEXT UNIQUE,
            url_image TEXT,
            chemin_image TEXT
        );
        """
        with self._obtenir_connexion() as conn:
            conn.execute(sql)

    def ajouter(self, produit: Produit) -> bool:
        """Ajoute un produit en base. Évite les doublons sur l'URL du produit.

        Renvoie True si le produit a été inséré, False s'il existait déjà.
        """
        sql = """
        INSERT OR IGNORE INTO produits (
            nom, prix, categorie, description, note, nb_avis,
            url_produit, url_image, chemin_image
        ) VALUES (
            :nom, :prix, :categorie, :description, :note, :nb_avis,
            :url_produit, :url_image, :chemin_image
        );
        """
        with self._obtenir_connexion() as conn:
            curseur = conn.execute(sql, produit.vers_dict())
            return curseur.rowcount > 0

    def ajouter_plusieurs(self, produits: List[Produit]) -> int:
        """Ajoute une liste de produits en base.

        Renvoie le nombre de nouveaux produits insérés.
        """
        nb_ajouts = 0
        for produit in produits:
            if self.ajouter(produit):
                nb_ajouts += 1
        return nb_ajouts

    def lister(self) -> List[Produit]:
        """Récupère l'ensemble des produits enregistrés en base."""
        sql = """
        SELECT nom, prix, categorie, description, note, nb_avis,
               url_produit, url_image, chemin_image
        FROM produits
        ORDER BY id ASC;
        """
        produits = []
        with self._obtenir_connexion() as conn:
            curseur = conn.execute(sql)
            for ligne in curseur.fetchall():
                produits.append(
                    Produit(
                        nom=ligne[0],
                        prix=ligne[1],
                        categorie=ligne[2],
                        description=ligne[3],
                        note=ligne[4],
                        nb_avis=ligne[5],
                        url_produit=ligne[6],
                        url_image=ligne[7],
                        chemin_image=ligne[8],
                    )
                )
        return produits

    def compter(self) -> int:
        """Renvoie le nombre total de produits stockés en base."""
        sql = "SELECT COUNT(*) FROM produits;"
        with self._obtenir_connexion() as conn:
            curseur = conn.execute(sql)
            return curseur.fetchone()[0]

    def tout_supprimer(self) -> None:
        """Supprime tous les produits de la base."""
        sql = "DELETE FROM produits;"
        with self._obtenir_connexion() as conn:
            conn.execute(sql)
