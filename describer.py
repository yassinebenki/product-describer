import os
import json
import cohere

DESCRIPTION_PATH = "data/descriptions/descriptions.json"

def call_model(prompt: str, use_real_model: bool = False, api_key: str = None) -> str:
    if use_real_model:
        if api_key is None:
            raise ValueError("API key must be provided for real model usage.")
        try:
            co = cohere.Client(api_key)
            response = co.generate(
                model="command-r-plus",
                prompt=prompt,
                max_tokens=100,
                temperature=0.7
            )
            return response.generations[0].text.strip()
        except cohere.CohereError as e:
            return f"[ERROR - Cohere] {str(e)}"
        except Exception as e:
            return f"[ERROR - Unexpected] {str(e)}"
    else:
        return f"[SIMULATED DESCRIPTION] {prompt}"

def generate_description(product, use_real_model=False, api_key=None):
    prompt = (
        f"Write a short, friendly product description for a {product['category']} named "
        f"\"{product['title']}\" priced at {product['price']}$ with a {product['rating']}★ rating."
    )
    return call_model(prompt, use_real_model=use_real_model, api_key=api_key)

def describe_products(products, use_real_model=False, api_key=None):
    described = []
    for product in products:
        print(f"→ Génération pour : {product['title']}")
        description = generate_description(product, use_real_model, api_key)
        described.append({
            "id": product["id"],
            "title": product["title"],
            "category": product["category"],
            "description": description
        })
    return described

def save_descriptions(descriptions, path=DESCRIPTION_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(descriptions, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    raise RuntimeError("Ce fichier est destiné à être importé depuis pipeline.py")
