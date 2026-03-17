from flask import Flask, jsonify, request

app = Flask(__name__)


def calcular(operacao: str, a: float, b: float) -> float:
    if operacao == "soma":
        return a + b
    if operacao == "subtracao":
        return a - b
    if operacao == "multiplicacao":
        return a * b
    if operacao == "divisao":
        if b == 0:
            raise ValueError("Divisão por zero não é permitida")
        return a / b
    raise ValueError(f"Operação inválida: {operacao}")


@app.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@app.post("/calcular")
def calcular_endpoint():
    dados = request.get_json(silent=True) or {}
    operacao = dados.get("operacao")
    a = dados.get("a")
    b = dados.get("b")

    if operacao is None or a is None or b is None:
        return (
            jsonify({"erro": "Envie os campos: operacao, a e b"}),
            400,
        )

    try:
        resultado = calcular(operacao, float(a), float(b))
        return jsonify({"resultado": resultado}), 200
    except ValueError as exc:
        return jsonify({"erro": str(exc)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
