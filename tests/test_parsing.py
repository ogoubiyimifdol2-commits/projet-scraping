"""Tests unitaires pour les fonctions de conversion et d'analyse HTML.

Ces tests utilisent le module standard unittest de Python.
"""

import unittest
from models.produit import Produit
from scraper.fallback_data import obtenir_produits_secours
from scraper.parsing import convertir_prix, extraire_produits


class TestParsing(unittest.TestCase):
    """Tests unitaires du module scraper/parsing.py."""

    def test_convertir_prix_dollar(self):
        """Vérifie la conversion correcte d'un prix en dollars."""
        self.assertEqual(convertir_prix("$295.99"), 295.99)
        self.assertEqual(convertir_prix(" $12.50 "), 12.50)

    def test_convertir_prix_euro_avec_virgule(self):
        """Vérifie la conversion d'un montant avec virgule et symbole euro."""
        self.assertEqual(convertir_prix("416,50 €"), 416.50)
        self.assertEqual(convertir_prix("49,99€"), 49.99)

    def test_convertir_prix_avec_espaces_milliers(self):
        """Vérifie la conversion avec espaces ou séparateurs de milliers."""
        self.assertEqual(convertir_prix("1 299,00 €"), 1299.00)
        self.assertEqual(convertir_prix("1.450,99 €"), 1450.99)
        self.assertEqual(convertir_prix("2 499 €"), 2499.00)

    def test_convertir_prix_invalide(self):
        """Vérifie qu'une exception est levée pour des entrées invalides."""
        with self.assertRaises(ValueError):
            convertir_prix("gratuit")
        with self.assertRaises(ValueError):
            convertir_prix("")

    def test_extraire_produits_amazon_html(self):
        """Vérifie l'extraction d'un produit depuis la structure HTML Amazon."""
        html_amazon = """
        <div data-component-type="s-search-result" data-asin="B09XYZ123">
            <img class="s-image" src="https://m.media-amazon.com/images/I/71test.jpg" />
            <h2>
                <a class="a-link-normal" href="/dp/B09XYZ123">
                    <span class="a-size-medium">Asus ZenBook 14 OLED</span>
                </a>
            </h2>
            <span class="a-price">
                <span class="a-offscreen">899,99 €</span>
            </span>
            <span class="a-icon-alt">4,5 sur 5 étoiles</span>
            <span class="a-size-base s-underline-text">1 420</span>
        </div>
        """
        produits = extraire_produits(html_amazon, categorie="Ordinateurs portables")

        self.assertEqual(len(produits), 1)
        produit = produits[0]
        self.assertEqual(produit.nom, "Asus ZenBook 14 OLED")
        self.assertEqual(produit.prix, 899.99)
        self.assertEqual(produit.categorie, "Ordinateurs portables")
        self.assertEqual(produit.note, 5)  # 4.5 arrondi à 5
        self.assertEqual(produit.nb_avis, 1420)
        self.assertTrue(produit.url_produit.endswith("/dp/B09XYZ123"))
        self.assertEqual(produit.url_image, "https://m.media-amazon.com/images/I/71test.jpg")

    def test_extraire_produits_fallback_html(self):
        """Vérifie le fonctionnement sur un conteneur produit générique."""
        html_exemple = """
        <div class="product-wrapper card-body">
            <img class="image" src="/images/test.png" />
            <h4 class="price">$599.99</h4>
            <h4><a class="title" href="/product/123" title="Lenovo ThinkPad">Lenovo ThinkPad</a></h4>
            <p class="description">PC portable professionnel.</p>
            <div class="ratings">
                <p class="review-count">4 reviews</p>
                <p data-rating="4"><span class="ws-icon-star"></span></p>
            </div>
        </div>
        """
        produits = extraire_produits(html_exemple, categorie="Laptops")

        self.assertEqual(len(produits), 1)
        produit = produits[0]
        self.assertEqual(produit.nom, "Lenovo ThinkPad")
        self.assertEqual(produit.prix, 599.99)
        self.assertEqual(produit.note, 4)
        self.assertEqual(produit.nb_avis, 4)

    def test_catalogue_secours_amazon_electronique(self):
        """Vérifie la disponibilité du catalogue de secours (Téléphones, MacBook, AirPods)."""
        for cat in ["Téléphones", "MacBook", "AirPods"]:
            produits = obtenir_produits_secours(cat)
            self.assertGreater(len(produits), 0, f"Aucun produit de secours pour {cat}")
            self.assertTrue(all(p.prix > 0 for p in produits))
            self.assertTrue(all(p.categorie == cat for p in produits))


class TestProduitModel(unittest.TestCase):
    """Tests unitaires pour le modèle Produit."""

    def test_prix_positif_valide(self):
        """Un prix positif doit être accepté."""
        p = Produit(nom="Clavier", prix=45.0, categorie="Accessoires")
        self.assertEqual(p.prix, 45.0)

    def test_prix_negatif_refuse(self):
        """Un prix négatif doit lever une ValueError."""
        with self.assertRaises(ValueError):
            Produit(nom="Souris", prix=-10.0, categorie="Accessoires")

    def test_vers_dict(self):
        """La méthode vers_dict doit retourner un dictionnaire avec toutes les clés."""
        p = Produit(nom="Écran", prix=150.0, categorie="Écrans")
        d = p.vers_dict()
        self.assertIn("nom", d)
        self.assertIn("prix", d)
        self.assertEqual(d["nom"], "Écran")
        self.assertEqual(d["prix"], 150.0)


if __name__ == "__main__":
    unittest.main()
