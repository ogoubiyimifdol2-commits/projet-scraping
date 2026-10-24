"""Fonctions d'analyse et d'extraction des données HTML (parsing).

Ce module utilise BeautifulSoup pour convertir le code HTML d'une page
en objets Produit exploitables par l'application.
"""

import re
from typing import List
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from config import URL_BASE
from models.produit import Produit


def convertir_prix(chaine_prix: str) -> float:
    """Convertit une chaîne de prix avec symbole de devise en nombre flottant.

    Prend en charge les formats européens et anglo-saxons avec espaces ou devises.
    Exemples :
    - "416,50 €" -> 416.50
    - "1 299,00 €" -> 1299.00
    - "1.299,99 €" -> 1299.99
    - "$295.99" -> 295.99
    """
    if not chaine_prix or not isinstance(chaine_prix, str):
        raise ValueError("La chaîne de prix est vide ou non valide.")

    # Nettoyage des espaces insécables, espaces et symboles monétaires
    texte = (
        chaine_prix.strip()
        .replace("\xa0", "")
        .replace("\u202f", "")
        .replace(" ", "")
        .replace("€", "")
        .replace("$", "")
        .replace("£", "")
    )

    # Format avec virgule décimale (ex : 1299,99 ou 1.299,99)
    if "," in texte:
        texte = texte.replace(".", "")  # supprime les séparateurs de milliers
        texte = texte.replace(",", ".")
    elif texte.count(".") > 1:
        # Séparateur de milliers avec plusieurs points (ex : 1.299.00 -> 1299.00)
        parties = texte.split(".")
        texte = "".join(parties[:-1]) + "." + parties[-1]

    match = re.search(r"\d+(\.\d+)?", texte)
    if not match:
        raise ValueError(f"Impossible d'extraire un prix de '{chaine_prix}'")

    return float(match.group(0))


def extraire_note(conteneur) -> int:
    """Extrait la note en nombre d'étoiles (attribut data-rating, texte Amazon ou icônes)."""
    # 1. Tentative sur texte Amazon (ex : "4,3 sur 5 étoiles" ou "4.3 out of 5 stars")
    element_note = conteneur.select_one(
        "i.a-icon-star span.a-icon-alt, "
        "i.a-icon-star-small span.a-icon-alt, "
        "span.a-icon-alt, "
        "[data-rating]"
    )
    if element_note:
        if element_note.get("data-rating"):
            try:
                return int(round(float(element_note["data-rating"])))
            except ValueError:
                pass

        texte = element_note.get_text(strip=True)
        match = re.search(r"(\d+(?:[.,]\d+)?)", texte)
        if match:
            try:
                valeur = float(match.group(1).replace(",", "."))
                return int(valeur + 0.5)
            except ValueError:
                pass

    # 2. Tentative par comptage des icônes d'étoiles
    etoiles = conteneur.select(".ws-icon-star, .glyphicon-star, .a-star-small-4, .a-star-small-5")
    if etoiles:
        return len(etoiles)

    return 0


def extraire_nb_avis(conteneur) -> int:
    """Extrait le nombre d'avis du produit (ex: '2 reviews' ou '1 254')."""
    element_avis = conteneur.select_one(
        "span.a-size-base.s-underline-text, "
        "a[href*='#customerReviews'] span, "
        ".review-count, "
        "[itemprop='reviewCount']"
    )
    if not element_avis:
        return 0

    texte = (
        element_avis.get_text(strip=True)
        .replace("\xa0", "")
        .replace("\u202f", "")
        .replace(" ", "")
        .replace(".", "")
    )
    match = re.search(r"\d+", texte)
    return int(match.group(0)) if match else 0


def extraire_produits(html: str, categorie: str) -> List[Produit]:
    """Parse le code HTML d'une page et extrait tous les produits trouvés.

    Supporte la structure des résultats Amazon (div[data-component-type='s-search-result'])
    ainsi que les sélecteurs génériques e-commerce (.product-wrapper, .thumbnail).

    :param html: Code source HTML de la page.
    :param categorie: Nom de la catégorie (ex: 'Ordinateurs portables', 'Tablettes').
    :return: Liste d'instances de Produit.
    """
    soup = BeautifulSoup(html, "html.parser")
    produits: List[Produit] = []

    # 1. Sélection des conteneurs de produits (Amazon en priorité)
    cartes = soup.select("div[data-component-type='s-search-result']")
    if not cartes:
        cartes = [
            c for c in soup.select(".s-result-item[data-asin]")
            if c.get("data-asin") and c.get("data-asin").strip()
        ]

    # Fallback pour pages génériques ou test
    if not cartes:
        cartes = soup.select(".product-wrapper, .thumbnail")

    for carte in cartes:
        # Nom et URL du produit
        lien_titre = carte.select_one("h2 a, a.title, a.a-link-normal.s-no-outline")
        nom = ""
        url_produit = ""

        if lien_titre:
            span_titre = lien_titre.select_one("span")
            nom = span_titre.get_text(strip=True) if span_titre else lien_titre.get_text(strip=True)
            url_relative_prod = lien_titre.get("href", "")
            url_produit = urljoin(URL_BASE, url_relative_prod)
        else:
            h2 = carte.select_one("h2")
            if h2:
                nom = h2.get_text(strip=True)

        if not nom:
            continue

        # Prix
        element_prix = carte.select_one(
            "span.a-price span.a-offscreen, "
            ".price, "
            "[itemprop='price']"
        )
        prix = 0.0
        if element_prix:
            try:
                prix = convertir_prix(element_prix.get_text(strip=True))
            except ValueError:
                prix = 0.0
        else:
            # Fallback Amazon pour les composants séparés (whole / fraction)
            whole = carte.select_one("span.a-price-whole")
            if whole:
                fraction = carte.select_one("span.a-price-fraction")
                texte_prix = whole.get_text(strip=True)
                if fraction:
                    texte_prix += "." + fraction.get_text(strip=True)
                try:
                    prix = convertir_prix(texte_prix)
                except ValueError:
                    prix = 0.0

        # Si aucun prix valide n'est trouvé, le produit est indisponible ou non pertinent
        if prix <= 0:
            continue

        # Description
        element_desc = carte.select_one(
            ".description, p.description, "
            ".a-row.a-size-base.a-color-secondary"
        )
        description = element_desc.get_text(strip=True) if element_desc else nom

        # Note et nombre d'avis
        note = extraire_note(carte)
        nb_avis = extraire_nb_avis(carte)

        # Image
        balise_img = carte.select_one("img.s-image, img.image, img.card-img-top")
        url_image = ""
        if balise_img:
            src = balise_img.get("src") or balise_img.get("data-src", "")
            if src:
                url_image = urljoin(URL_BASE, src)

        produits.append(
            Produit(
                nom=nom,
                prix=prix,
                categorie=categorie,
                description=description,
                note=note,
                nb_avis=nb_avis,
                url_produit=url_produit,
                url_image=url_image,
            )
        )

    return produits
