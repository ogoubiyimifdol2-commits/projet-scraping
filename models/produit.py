"""Modèle représentant un produit.

Ce module définit la classe Produit avec ses attributs métier,
la validation du prix et une méthode d'exportation vers un dictionnaire.
"""


class Produit:
    """Représente un produit scrapé sur le site d'e-commerce."""

    def __init__(
        self,
        nom: str,
        prix: float,
        categorie: str,
        description: str = "",
        note: int = 0,
        nb_avis: int = 0,
        url_produit: str = "",
        url_image: str = "",
        chemin_image: str = "",
    ):
        """Initialise un nouveau produit avec validation des données."""
        self.valider_prix(prix)

        self.nom = str(nom).strip()
        self.prix = float(prix)
        self.categorie = str(categorie).strip()
        self.description = str(description).strip()
        self.note = int(note)
        self.nb_avis = int(nb_avis)
        self.url_produit = str(url_produit).strip()
        self.url_image = str(url_image).strip()
        self.chemin_image = str(chemin_image).strip()

    @staticmethod
    def valider_prix(prix: float) -> None:
        """Vérifie que le prix est un nombre positif ou nul."""
        try:
            valeur = float(prix)
        except (ValueError, TypeError):
            raise ValueError(f"Le prix '{prix}' n'est pas un nombre valide.")

        if valeur < 0:
            raise ValueError(f"Le prix ne peut pas être négatif : {valeur}")

    def vers_dict(self) -> dict:
        """Convertit l'objet Produit en dictionnaire."""
        return {
            "nom": self.nom,
            "prix": self.prix,
            "categorie": self.categorie,
            "description": self.description,
            "note": self.note,
            "nb_avis": self.nb_avis,
            "url_produit": self.url_produit,
            "url_image": self.url_image,
            "chemin_image": self.chemin_image,
        }

    def __repr__(self) -> str:
        """Affichage lisible pour le débogage."""
        return f"<Produit: {self.nom} ({self.prix}€, {self.categorie})>"
