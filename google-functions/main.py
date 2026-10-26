import functions_framework
from flask import jsonify
import math


@functions_framework.http
def projetor_inflacao(request):
    if request.method == "OPTIONS":
        return "", 204, {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }

    if request.method != "POST":
        return jsonify({"error": "Use POST"}), 405, {
            "Access-Control-Allow-Origin": "*"
        }

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"error": "JSON invalido"}), 400, {
            "Access-Control-Allow-Origin": "*"
        }

    try:
        balance = float(dados["balance"])
        inflation = float(dados["inflation"])
        months = float(dados["months"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Parametros invalidos"}), 400, {
            "Access-Control-Allow-Origin": "*"
        }

    if not all(math.isfinite(v) for v in
               (balance, inflation, months)):
        return jsonify({"error": "Valores invalidos"}), 400, {
            "Access-Control-Allow-Origin": "*"
        }

    if balance < 0 or inflation <= -1 or months < 0 or months > 360:
        return jsonify({"error": "Valores fora dos limites"}), 400, {
            "Access-Control-Allow-Origin": "*"
        }

    real = balance / ((1 + inflation) ** (months / 12))

    return jsonify({"real": round(real, 2)}), 200, {
        "Access-Control-Allow-Origin": "*"
    }