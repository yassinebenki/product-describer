import requests
import json
import os
import random

RAW_DATA_PATH = "data/raw/products.json"

def fetch_products(api_url="https://dummyjson.com/products", limit=10):
    # L'API a 100 produits au total, on choisit un point de départ aléatoire
    max_skip = 100 - limit
    skip = random.randint(0, max_skip)
    
    print(f"→ Récupération de {limit} produits à partir de l'index {skip}...")
    response = requests.get(api_url, params={"limit": limit, "skip": skip})
    response.raise_for_status()
    
    products = response.json()["products"]
    return products

def save_products(products, path=RAW_DATA_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    products = fetch_products()
    save_products(products)
    print(f"{len(products)} produits enregistrés dans {RAW_DATA_PATH}")
