from flask import Flask, request, jsonify
import re

app = Flask(__name__)

assets = [
    {"id": 1, "serial_number": "SN-MAC-01", "model": "MacBook Pro M3", "stock_available": 5, "status": "READY"},
    {"id": 2, "serial_number": "SN-DELL-02", "model": "Dell UltraSharp 27", "stock_available": 10, "status": "READY"},
    {"id": 3, "serial_number": "SN-THINK-03", "model": "ThinkPad X1 Carbon", "stock_available": 0, "status": "REPAIRING"}
]

allocations = [
    {
        "id": 1,
        "asset_id": 1,
        "employee_email": "dev.nguyen@company.com",
        "allocated_quantity": 1,
        "start_date": "2026-07-01",
        "duration_months": 12
    }
]

valid_statuses = ["READY", "ALLOCATED", "REPAIRING", "SCRAPPED"]

@app.route("/assets", methods=["POST"])
def create_asset():
    data = request.json
    if any(a["serial_number"] == data["serial_number"] for a in assets):
        return jsonify({"error": "Serial number must be unique"}), 400
    if len(data["model"]) < 2 or len(data["model"]) > 255:
        return jsonify({"error": "Model length must be between 2 and 255"}), 400
    if data["stock_available"] < 0:
        return jsonify({"error": "Stock must be >= 0"}), 400
    if data["status"] not in valid_statuses:
        return jsonify({"error": "Invalid status"}), 400

    new_asset = {"id": len(assets) + 1, **data}
    assets.append(new_asset)
    return jsonify(new_asset), 201

@app.route("/assets", methods=["GET"])
def list_assets():
    keyword = request.args.get("keyword")
    status = request.args.get("status")
    min_stock = request.args.get("min_stock", type=int)

    result = assets
    if keyword:
        kw = keyword.lower()
        result = [a for a in result if kw in a["serial_number"].lower() or kw in a["model"].lower()]
    if status:
        result = [a for a in result if a["status"] == status]
    if min_stock is not None:
        result = [a for a in result if a["stock_available"] >= min_stock]

    return jsonify(result)

@app.route("/assets/<int:asset_id>", methods=["GET"])
def get_asset(asset_id):
    asset = next((a for a in assets if a["id"] == asset_id), None)
    if not asset:
        return jsonify({"error": "Asset not found"}), 404
    return jsonify(asset)

@app.route("/assets/<int:asset_id>", methods=["PUT"])
def update_asset(asset_id):
    asset = next((a for a in assets if a["id"] == asset_id), None)
    if not asset:
        return jsonify({"error": "Asset not found"}), 404
    data = request.json
    asset.update(data)
    return jsonify(asset)

@app.route("/assets/<int:asset_id>", methods=["DELETE"])
def delete_asset(asset_id):
    global assets
    assets = [a for a in assets if a["id"] != asset_id]
    return jsonify({"message": "Asset deleted"}), 200

@app.route("/allocations", methods=["POST"])
def create_allocation():
    data = request.json
    asset = next((a for a in assets if a["id"] == data["asset_id"]), None)
    if not asset:
        return jsonify({"error": "Asset not found"}), 400
    if asset["status"] != "READY":
        return jsonify({"error": "Asset not available"}), 400
    if data["allocated_quantity"] <= 0:
        return jsonify({"error": "Quantity must be > 0"}), 400
    if data["allocated_quantity"] > asset["stock_available"]:
        return jsonify({"error": "Exceeds available stock"}), 400
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", data["employee_email"]):
        return jsonify({"error": "Invalid email format"}), 400
    if not (1 <= data["duration_months"] <= 12):
        return jsonify({"error": "Duration must be between 1 and 12 months"}), 400

    new_allocation = {"id": len(allocations) + 1, **data}
    allocations.append(new_allocation)
    asset["stock_available"] -= data["allocated_quantity"]
    return jsonify(new_allocation), 201

@app.route("/allocations", methods=["GET"])
def list_allocations():
    return jsonify(allocations)

