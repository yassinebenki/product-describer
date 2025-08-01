# generate_html.py
import json
import os
from collections import defaultdict

DESCRIPTION_PATH = "data/descriptions/descriptions.json"
OUTPUT_HTML_PATH = "data/descriptions/output.html"


#Not used
############################
def load_descriptions(path=DESCRIPTION_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
#############################

def generate_html(descriptions):
    grouped = defaultdict(list)  # Pas besoin d'initialiser le dictionnaire avec des catégories vides
    for item in descriptions:
        category = item.get("category", "Autre")
        grouped[category].append(item)

    html = [
        "<!DOCTYPE html>",
        "<html lang='fr'>",
        "<head>",
        "  <meta charset='UTF-8'>",
        "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        "  <title>Descriptions de Produits</title>",
        "  <style>",
        "    body { font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px; }",
        "    h1 { text-align: center; color: #333; }",
        "    .category { margin-top: 40px; }",
        "    .product { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }",
        "    .product-title { font-size: 18px; font-weight: bold; color: #2c3e50; }",
        "    .product-desc { margin-top: 5px; color: #555; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <h1>Descriptions Générées</h1>"
    ]

    for category, items in grouped.items():
        html.append(f"<div class='category'><h2>{category.title()}</h2>")
        for item in items:
            html.append("<div class='product'>")
            html.append(f"  <div class='product-title'>{item['title']}</div>")
            html.append(f"  <div class='product-desc'>{item['description']}</div>")
            html.append("</div>")
        html.append("</div>")  # fin catégorie

    html.append("</body></html>")
    return "\n".join(html)

def save_html(content, path=OUTPUT_HTML_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Fichier HTML généré dans : {path}")

# Test routine
if __name__ == "__main__":
    descriptions = load_descriptions()
    html = generate_html(descriptions)
    save_html(html)
