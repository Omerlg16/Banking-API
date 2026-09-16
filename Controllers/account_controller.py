from flask import Flask, jsonify, request, render_template
from Services.account_service import balance, deposit, withdraw
from Services.auth_service import register, login, verify_token
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/accounts/<int:account_id>/balance", methods=["GET"])
def balance_route(account_id):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Token manquant"}), 401

    token = auth_header.replace("Bearer ", "")

    payload, erreur = verify_token(token)
    if erreur:
        return jsonify({"error": erreur}), 401

    resultat, erreur = balance(account_id)

    if erreur:
        return jsonify({"error": erreur}), 404

    return jsonify({"solde": resultat}), 200


@app.route("/api/accounts/<int:account_id>/deposit", methods=["POST"])
def deposit_route(account_id):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Token manquant"}), 401

    token = auth_header.replace("Bearer ", "")

    payload, erreur = verify_token(token)
    if erreur:
        return jsonify({"error": erreur}), 401

    data = request.get_json()
    amount = data.get("amount")

    resultat, erreur = deposit(account_id, amount)

    if erreur:
        return jsonify({"error": erreur}), 400

    return jsonify({"solde": resultat}), 200


@app.route("/api/accounts/<int:account_id>/withdraw", methods=["POST"])
def withdraw_route(account_id):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Token manquant"}), 401

    token = auth_header.replace("Bearer ", "")

    payload, erreur = verify_token(token)
    if erreur:
        return jsonify({"error": erreur}), 401

    data = request.get_json()
    amount = data.get("amount")

    resultat, erreur = withdraw(account_id, amount)

    if erreur:
        return jsonify({"error": erreur}), 400

    return jsonify({"solde": resultat}), 200


@app.route("/api/auth/register", methods=["POST"])
def register_route():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    resultat, erreur = register(email, password)

    if erreur:
        return jsonify({"error": erreur}), 400

    return jsonify({"email": resultat}), 201


@app.route("/api/auth/login", methods=["POST"])
def login_route():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    token, erreur = login(email, password)

    if erreur:
        return jsonify({"error": erreur}), 401

    return jsonify({"token": token}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)