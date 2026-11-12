import os
import csv
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

DATA_DIR = "data"
CSV_FILE = os.path.join(DATA_DIR, "inventory.csv")

FIELDNAMES = ["id", "name", "category", "quantity", "price", "location", "created_at"]


def init_csv():
    """Створює папку та CSV файл з заголовками, якщо вони відсутні."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()


def read_csv():
    """Читає всі товари з CSV-файлу."""
    init_csv()
    items = []
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append(row)
    return items


def write_csv(items):
    """Записує список товарів у CSV-файл."""
    init_csv()
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for item in items:
            writer.writerow(item)


@app.route("/items", methods=["GET"])
def get_items():
    items = read_csv()
    return jsonify(items), 200


@app.route("/items", methods=["POST"])
def add_item():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    # Валідація типів даних
    name = data.get("name")
    category = data.get("category")
    try:
        quantity = int(data.get("quantity"))
        price = float(data.get("price"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid types for quantity (int) or price (float)"}), 400

    location = data.get("location", "")

    items = read_csv()
    # Генеруємо унікальний ID (на основі максимального існуючого або кількості)
    new_id = str(max([int(i["id"]) for i in items], default=0) + 1)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_row = {
        "id": new_id,
        "name": str(name),
        "category": str(category),
        "quantity": str(quantity),
        "price": str(price),
        "location": str(location),
        "created_at": created_at
    }

    items.append(new_row)
    write_csv(items)
    return jsonify(new_row), 201


@app.route("/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        quantity = int(data.get("quantity"))
        price = float(data.get("price"))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid types for quantity (int) or price (float)"}), 400

    items = read_csv()
    found = False

    for item in items:
        if item["id"] == str(item_id):
            item["name"] = str(data.get("name", item["name"]))
            item["category"] = str(data.get("category", item["category"]))
            item["quantity"] = str(quantity)
            item["price"] = str(price)
            item["location"] = str(data.get("location", item["location"]))
            found = True
            break

    if not found:
        return jsonify({"error": "Item not found"}), 404

    write_csv(items)
    return jsonify({"message": "Item updated successfully"}), 200


@app.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    items = read_csv()
    new_items = [i for i in items if i["id"] != str(item_id)]

    if len(new_items) == len(items):
        return jsonify({"error": "Item not found"}), 404

    write_csv(new_items)
    return jsonify({"message": "Item deleted successfully"}), 200


if __name__ == "__main__":
    init_csv()
    app.run(host="0.0.0.0", port=5000, debug=True)