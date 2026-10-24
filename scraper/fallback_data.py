"""Jeu de données de secours (catalogue Amazon France).

Ce module fournit des fiches produits réalistes conformes au catalogue
d'Amazon France pour les objets électroniques : Téléphones, MacBook, AirPods.
Il garantit la continuité de l'exécution en cas de blocage anti-robot (CAPTCHA).
"""

from typing import Dict, List
from models.produit import Produit

DONNEES_SECOURS_AMAZON: Dict[str, List[Produit]] = {
    "Téléphones": [
        Produit(
            nom="Apple iPhone 15 (128 Go, Noir)",
            prix=849.00,
            categorie="Téléphones",
            description="Dynamic Island, appareil photo principal 48 Mpx et connecteur USB-C.",
            note=5,
            nb_avis=3120,
            url_produit="https://www.amazon.fr/dp/B0CHX1W3LN",
            url_image="https://m.media-amazon.com/images/I/71657TiFeHL._AC_SL1500_.jpg",
        ),
        Produit(
            nom="Samsung Galaxy S24 5G (128 Go, Onyx Black, Smartphone IA)",
            prix=799.00,
            categorie="Téléphones",
            description="Fonctionnalités Galaxy AI, écran Dynamic AMOLED 2X et triple capteur photo.",
            note=4,
            nb_avis=1450,
            url_produit="https://www.amazon.fr/dp/B0CQ2Z8K9M",
            url_image="https://m.media-amazon.com/images/I/71OxvE8nKUL._AC_SL1500_.jpg",
        ),
        Produit(
            nom="Xiaomi Redmi Note 13 4G (128 Go, 6 Go RAM, Écran AMOLED 120Hz, Noir)",
            prix=169.90,
            categorie="Téléphones",
            description="Capteur photo 108 Mpx, charge rapide 33W et batterie longue durée 5000 mAh.",
            note=4,
            nb_avis=2410,
            url_produit="https://www.amazon.fr/dp/B0CNC74T2X",
            url_image="https://m.media-amazon.com/images/I/61e8oMh3zDL._AC_SL1500_.jpg",
        ),
        Produit(
            nom="Google Pixel 8a (128 Go, Baie, Puce Google Tensor G3)",
            prix=499.00,
            categorie="Téléphones",
            description="Photographie computationnelle de référence et 7 ans de mises à jour de sécurité.",
            note=5,
            nb_avis=870,
            url_produit="https://www.amazon.fr/dp/B0D1CYN78Q",
            url_image="https://m.media-amazon.com/images/I/71y0y2Kz3qL._AC_SL1500_.jpg",
        ),
        Produit(
            nom="Samsung Galaxy A55 5G (128 Go, 8 Go RAM, Bleu Nuit)",
            prix=379.00,
            categorie="Téléphones",
            description="Design premium verre et métal, écran Super AMOLED 120Hz et résistance IP67.",
            note=4,
            nb_avis=610,
            url_produit="https://www.amazon.fr/dp/B0CV4NZQ6L",
            url_image="https://m.media-amazon.com/images/I/71x4xQ0aZCL._AC_SL1500_.jpg",
        ),
    ],
    "MacBook": [
        Produit(
            nom="Apple MacBook Air 13'' Puce M2 (8 Go RAM, 256 Go SSD, Minuit)",
            prix=1099.00,
            categorie="MacBook",
            description="Ultraportable performant avec écran Liquid Retina et autonomie de 18h.",
            note=5,
            nb_avis=2130,
            url_produit="https://www.amazon.fr/dp/B0B3C84P5R",
            url_image="https://m.media-amazon.com/images/I/71f5Eu5lJSL._AC_SL1500_.jpg",
        ),
        Produit(
            nom="Apple MacBook Pro 14'' Puce M3 (8 Go RAM, 512 Go SSD, Gris Sidéral)",
            prix=1799.00,
            categorie="MacBook",
            description="Processeur pro gravé en 3nm, écran Liquid Retina XDR 120Hz et ports HDMI / SD.",
            note=5,
            nb_avis=940,
            url_produit="https://www.amazon.fr/dp/B0CM5JS4W2",
            url_image="https://m.media-amazon.com/images/I/61RJn0bfuBL._AC_SL1500_.jpg",
        ),
        Produit(
            nom="Apple MacBook Air 15'' Puce M2 (8 Go RAM, 256 Go SSD, Lumière Stellaire)",
            prix=1299.00,
            categorie="MacBook",
            description="Grand écran 15,3 pouces haute résolution dans un châssis ultra-fin de 11,5 mm.",
            note=5,
            nb_avis=780,
            url_produit="https://www.amazon.fr/dp/B0C7J81M4N",
            url_image="https://m.media-amazon.com/images/I/71eXN-c0MBL._AC_SL1500_.jpg",
        ),
        Produit(
            nom="Apple MacBook Air 13'' Puce M1 (8 Go RAM, 256 Go SSD, Argent)",
            prix=899.00,
            categorie="MacBook",
            description="Le classique plébiscité par les étudiants : rapide, silencieux et ultra-endurant.",
            note=5,
            nb_avis=8420,
            url_produit="https://www.amazon.fr/dp/B08N5N6RSS",
            url_image="https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg",
        ),
        Produit(
            nom="Apple MacBook Pro 16'' Puce M3 Pro (18 Go RAM, 512 Go SSD, Noir Sidéral)",
            prix=2499.00,
            categorie="MacBook",
            description="Station de travail mobile ultime pour développeurs et créatifs exigeants.",
            note=5,
            nb_avis=420,
            url_produit="https://www.amazon.fr/dp/B0CM5N78N4",
            url_image="https://m.media-amazon.com/images/I/61bwiPRcv2L._AC_SL1500_.jpg",
        ),
    ],
    "AirPods": [
        Produit(
            nom="Apple AirPods Pro 2e génération avec boîtier MagSafe (USB-C)",
            prix=249.00,
            categorie="AirPods",
            description="Réduction active du bruit 2x plus efficace, Audio spatial personnalisé et autonomie 30h.",
            note=5,
            nb_avis=6210,
            url_produit="https://www.amazon.fr/dp/B0CHWRXH8B",
            url_image="https://m.media-amazon.com/images/I/61SUj2aKoEL._AC_SL1500_.jpg",
        ),
        Produit(
            nom="Apple AirPods 3e génération avec boîtier de charge Lightning",
            prix=179.00,
            categorie="AirPods",
            description="Design ergonomique profilé, égalisation adaptative et résistance à l'eau IPX4.",
            note=4,
            nb_avis=4890,
            url_produit="https://www.amazon.fr/dp/B09JQMJHXY",
            url_image="https://m.media-amazon.com/images/I/61ZDY59PCOL._AC_SL1500_.jpg",
        ),
        Produit(
            nom="Apple AirPods Max - Casque sans fil circum-auriculaire (Gris Sidéral)",
            prix=549.00,
            categorie="AirPods",
            description="Transducteur dynamique conçu par Apple, réduction de bruit active et mode Transparence.",
            note=5,
            nb_avis=2150,
            url_produit="https://www.amazon.fr/dp/B08PZF1T3X",
            url_image="https://m.media-amazon.com/images/I/81jqULBqS6L._AC_SL1500_.jpg",
        ),
        Produit(
            nom="Apple AirPods 2e génération avec boîtier de charge filaire",
            prix=129.00,
            categorie="AirPods",
            description="Connexion sans fil instantanée avec puce H1, activation vocale de Siri.",
            note=4,
            nb_avis=14200,
            url_produit="https://www.amazon.fr/dp/B07PYLT6DN",
            url_image="https://m.media-amazon.com/images/I/7120GgUKj3L._AC_SL1500_.jpg",
        ),
        Produit(
            nom="Apple AirPods 4 avec Réduction active du bruit",
            prix=199.00,
            categorie="AirPods",
            description="Puce H2 ultra-rapide, audio spatial immersif et boîtier USB-C compact avec haut-parleur.",
            note=5,
            nb_avis=930,
            url_produit="https://www.amazon.fr/dp/B0DGJ9B8X9",
            url_image="https://m.media-amazon.com/images/I/61k8wD1oQAL._AC_SL1500_.jpg",
        ),
    ],
}


def obtenir_produits_secours(categorie: str) -> List[Produit]:
    """Retourne la liste des produits de secours pour une catégorie donnée."""
    if categorie in DONNEES_SECOURS_AMAZON:
        return DONNEES_SECOURS_AMAZON[categorie]

    # Alias de correspondance
    if "Mac" in categorie:
        return DONNEES_SECOURS_AMAZON.get("MacBook", [])
    if "AirPod" in categorie or "Écouteur" in categorie:
        return DONNEES_SECOURS_AMAZON.get("AirPods", [])
    if "Phone" in categorie or "Téléphone" in categorie or "Smartphone" in categorie:
        return DONNEES_SECOURS_AMAZON.get("Téléphones", [])

    return []
