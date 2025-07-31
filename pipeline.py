import json
import argparse
import os

from ingest_products import fetch_products, save_products, RAW_DATA_PATH
from describer import describe_products, save_descriptions, DESCRIPTION_PATH
from generate_html import load_descriptions, generate_html, save_html  # NEW

def load_products(path=RAW_DATA_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_pipeline(category_filter=None, use_real_model=False, api_key=None):
    print("→ Récupération des produits...")
    products = fetch_products()

    if category_filter:
        products = [p for p in products if p["category"].lower() == category_filter.lower()]
        if not products:
            print(f"Aucun produit trouvé pour la catégorie : {category_filter}")
            return

    save_products(products)

    print("→ Génération des descriptions...")
    descriptions = describe_products(products, use_real_model=use_real_model, api_key=api_key)
    save_descriptions(descriptions)

    print(f"✅ Descriptions enregistrées dans {DESCRIPTION_PATH}")

    # Générer automatiquement le HTML à la fin
    print("→ Génération du fichier HTML...")
    html = generate_html(descriptions)
    save_html(html)

    print("✅ Pipeline complet avec HTML généré ✔️")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pipeline de génération de descriptions de produits")
    parser.add_argument("--category", type=str, help="Filtrer par catégorie (ex: laptops)")
    parser.add_argument("--real-model", action="store_true", help="Utiliser le vrai modèle Cohere")
    parser.add_argument("--api-key", type=str, help="Clé API Cohere (facultatif si définie dans les variables d'environnement)")

    args = parser.parse_args()
    api_key = args.api_key or os.getenv("COHERE_API_KEY")
    run_pipeline(category_filter=args.category, use_real_model=args.real_model, api_key=api_key)
