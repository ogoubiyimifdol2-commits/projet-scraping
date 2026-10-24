"""Affichage console pour l'application de scraping (Vue).

Ce module se charge de présenter à l'utilisateur la liste des produits
et les 3 statistiques clés demandées (moyenne, maximum avec nom,
et répartition par catégorie).
"""

from typing import Dict, List
from models.produit import Produit


class VueConsole:
    """Gère l'ensemble des affichages textuels en console."""

    @staticmethod
    def afficher_banniere() -> None:
        """Affiche le titre et la présentation de l'application."""
        print("=" * 70)
        print("      PROJET DE SCRAPING WEB - L2 GENIE LOGICIEL")
        print("      Site cible : Amazon (amazon.fr)")
        print("      Catégories  : Téléphones, MacBook, AirPods")
        print("=" * 70)

    @staticmethod
    def afficher_message(message: str) -> None:
        """Affiche un message d'information simple."""
        print(f"[INFO] {message}")

    @staticmethod
    def afficher_erreur(erreur: str) -> None:
        """Affiche un message d'erreur."""
        print(f"[ERREUR] {erreur}")

    @staticmethod
    def afficher_apercu_produits(produits: List[Produit], limite: int = 5) -> None:
        """Affiche un extrait représentatif des produits extraits."""
        print("\n" + "-" * 70)
        print(f"APERÇU DES PRODUITS (premiers {min(limite, len(produits))} sur {len(produits)}) :")
        print("-" * 70)

        for i, p in enumerate(produits[:limite], start=1):
            print(f"{i:02d}. [{p.categorie}] {p.nom}")
            print(f"    Prix : {p.prix:.2f} € | Note : {p.note}/5 ({p.nb_avis} avis)")
            if p.chemin_image:
                print(f"    Image locale : {p.chemin_image}")
            print()

    @staticmethod
    def afficher_statistiques(produits: List[Produit]) -> None:
        """Calcule et affiche les 3 statistiques obligatoires :

        1. Moyenne des prix (globale et par catégorie)
        2. Produit le plus cher / Prix maximum (avec nom et catégorie)
        3. Nombre de produits par catégorie (et total)
        """
        print("=" * 70)
        print("                   RAPPORT STATISTIQUE")
        print("=" * 70)

        if not produits:
            print("Aucune donnée disponible pour calculer les statistiques.")
            return

        # Regroupement des produits par catégorie
        par_categorie: Dict[str, List[Produit]] = {}
        for p in produits:
            par_categorie.setdefault(p.categorie, []).append(p)

        # ---------------------------------------------------------
        # STATISTIQUE 3 : Nombre de produits par catégorie (et total)
        # ---------------------------------------------------------
        print("\n--- STATISTIQUE 1 : RÉPARTITION PAR CATÉGORIE ---")
        for cat, liste in sorted(par_categorie.items()):
            print(f"  • {cat:<12} : {len(liste):>3} produit(s)")
        print(f"  -> TOTAL GLOBAL  : {len(produits):>3} produit(s)")

        # ---------------------------------------------------------
        # STATISTIQUE 1 : Moyenne des prix (globale et par catégorie)
        # ---------------------------------------------------------
        print("\n--- STATISTIQUE 2 : MOYENNE DES PRIX ---")
        for cat, liste in sorted(par_categorie.items()):
            moyenne_cat = sum(p.prix for p in liste) / len(liste)
            print(f"  • Moyenne {cat:<10} : {moyenne_cat:>8.2f} €")

        moyenne_globale = sum(p.prix for p in produits) / len(produits)
        print(f"  -> MOYENNE GLOBALE    : {moyenne_globale:>8.2f} €")

        # ---------------------------------------------------------
        # STATISTIQUE 2 : Prix maximum (produit le plus cher avec son nom)
        # ---------------------------------------------------------
        print("\n--- STATISTIQUE 3 : PRIX MAXIMUM (PRODUIT LE PLUS CHER) ---")
        produit_max_global = max(produits, key=lambda p: p.prix)
        print(f"  -> RECORD GLOBAL :")
        print(f"     Nom       : {produit_max_global.nom}")
        print(f"     Prix      : {produit_max_global.prix:.2f} €")
        print(f"     Catégorie : {produit_max_global.categorie}")

        print("\n  -> Maximum par catégorie :")
        for cat, liste in sorted(par_categorie.items()):
            prod_max_cat = max(liste, key=lambda p: p.prix)
            print(f"     • {cat:<10} : {prod_max_cat.nom} ({prod_max_cat.prix:.2f} €)")

        print("=" * 70)
