"""Configuration générale du projet de scraping.

Ce fichier centralise l'ensemble des constantes utilisées dans l'application :
les URLs cibles, les limites de pagination, les pauses éthiques, le User-Agent
et les chemins d'accès aux fichiers (base de données, exports, images).
"""

from pathlib import Path

# --- URLs et Catégories cibles (Objets électroniques) ---
URL_BASE = "https://www.amazon.fr"

CATEGORIES = {
    "Téléphones": f"{URL_BASE}/s?k=smartphone",
    "MacBook": f"{URL_BASE}/s?k=macbook",
    "AirPods": f"{URL_BASE}/s?k=airpods",
}

# --- Paramètres de scraping éthique et configuration ---
PAGES_MAX = 3
PAUSE_SECONDES = 2.0  # Pause respectueuse pour éviter les surcharges et blocages
SANS_FENETRE = False  # False permet d'ouvrir Chrome visiblement pour éviter le blocage anti-robot Amazon
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

# --- Chemins des dossiers et fichiers ---
DOSSIER_RACINE = Path(__file__).resolve().parent
DOSSIER_DATA = DOSSIER_RACINE / "data"
DOSSIER_IMAGES = DOSSIER_DATA / "images"
DOSSIER_EXPORTS = DOSSIER_RACINE / "exports"

CHEMIN_BDD = DOSSIER_DATA / "produits.db"
CHEMIN_CSV = DOSSIER_EXPORTS / "produits.csv"

# Création des dossiers s'ils n'existent pas encore
DOSSIER_DATA.mkdir(parents=True, exist_ok=True)
DOSSIER_IMAGES.mkdir(parents=True, exist_ok=True)
DOSSIER_EXPORTS.mkdir(parents=True, exist_ok=True)
