from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Temporary inventory data
inventory = [
    {
        "id": 1,
        "barcode": "3017624010701",
        "name": "Nutella",
        "brand": "Ferrero",
        "price": 650,
        "stock": 10
    },
    {
        "id": 2,
        "barcode": "5449000000996",
        "name": "Coca-Cola",
        "brand": "Coca-Cola",
        "price": 100,
        "stock": 20
    }
]

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item), 200

    return jsonify({"error": "Item not found"}), 404

@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ["barcode", "name", "brand", "price", "stock"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    new_id = max([item["id"] for item in inventory], default=0) + 1

    new_item = {
        "id": new_id,
        "barcode": data["barcode"],
        "name": data["name"],
        "brand": data["brand"],
        "price": data["price"],
        "stock": data["stock"]
    }

    inventory.append(new_item)

    return jsonify(new_item), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()

    for item in inventory:
        if item["id"] == item_id:
            if not data:
                return jsonify({"error": "No data provided"}), 400

            item.update(data)
            item["id"] = item_id

            return jsonify(item), 200

    return jsonify({"error": "Item not found"}), 404
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            return jsonify({"message": "Item deleted successfully"}), 200

    return jsonify({"error": "Item not found"}), 404
@app.route("/lookup", methods=["GET"])
def lookup_product():
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    headers = {
        "User-Agent": "InventoryManagementApp/1.0"
    }

    try:
        if barcode:
            url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}"

            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            if response.status_code != 200:
                return jsonify({"error": "Could not contact OpenFoodFacts"}), 502

            data = response.json()

            if data.get("status") != 1:
                return jsonify({"error": "Product not found"}), 404

            product = data.get("product", {})

            return jsonify({
                "barcode": barcode,
                "name": product.get("product_name", ""),
                "brand": product.get("brands", ""),
                "ingredients": product.get("ingredients_text", "")
            }), 200

        if name:
            url = "https://world.openfoodfacts.org/cgi/search.pl"

            params = {
                "search_terms": name,
                "search_simple": 1,
                "action": "process",
                "json": 1,
                "page_size": 5
            }

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=10
            )

            if response.status_code != 200:
                return jsonify({"error": "Could not contact OpenFoodFacts"}), 502

            data = response.json()

            products = []

            for product in data.get("products", []):
                products.append({
                    "barcode": product.get("code", ""),
                    "name": product.get("product_name", ""),
                    "brand": product.get("brands", "")
                })

            return jsonify(products), 200

        return jsonify({"error": "Provide either barcode or name"}), 400

    except requests.RequestException:
        return jsonify({"error": "OpenFoodFacts API is unavailable"}), 502
if __name__ == "__main__":
    app.run(debug=True)
