# api.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import BaseModel, ValidationError
import json, os
from finmanAI2 import show_income, show_expense, show_balance, process_chat

app = Flask(__name__)
CORS(app)

DATA_FILE = "finman.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"account_dets": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# -----------------------
# Request Models
# -----------------------

class ChatRequest(BaseModel):
    message: str

# -----------------------
# Endpoints
# -----------------------

@app.route("/incomes", methods=["GET"])
def get_incomes():
    d = load_data()
    items = []
    for e in d.get("account_dets", []):
        if e.get("transaction_type") == "income":
            items.append({"category": e.get("category"), "amount": e.get("amount")})
    return jsonify(items)

@app.route("/expenses", methods=["GET"])
def get_expenses():
    d = load_data()
    items = []
    for e in d.get("account_dets", []):
        if e.get("transaction_type") == "expense":
            items.append({"category": e.get("category"), "amount": e.get("amount")})
    return jsonify(items)

@app.route("/balance", methods=["GET"])
def get_balance():
    d = load_data()
    try:
        val = show_balance(d)  # returns the numeric balance (it also prints)
        return jsonify({"balance": val})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/report", methods=["GET"])
def get_report():
    d = load_data()
    inc = sum(e["amount"] for e in d["account_dets"] if e["transaction_type"] == "income")
    exp = sum(e["amount"] for e in d["account_dets"] if e["transaction_type"] == "expense")
    bal = inc - exp
    return jsonify({"type": "report", "message": f"Total Income: {inc} | Total Expense: {exp} | Balance: {bal}"})

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        req = ChatRequest(**data)
    except (TypeError, ValidationError) as e:
        return jsonify({"error": "Invalid request", "details": str(e)}), 400

    if process_chat is None:
        return jsonify({
            "type": "clarification",
            "message": "Chat backend not wired. Please expose process_chat(message) in your_chat_backend.py and import it."
        })
    result = process_chat(req.message)
    if not isinstance(result, dict) or "type" not in result or "message" not in result:
        return jsonify({"error": "process_chat returned an invalid response."}), 500
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=8000)