from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


STATUS_VALIDOS = {"backlog", "em_teste", "aprovado"}

cards = [
    {
        "id": 1,
        "dev": "Ana",
        "branch": "feature/ana-login",
        "tarefa": "Tela de login",
        "status": "backlog",
    },
    {
        "id": 2,
        "dev": "Bruno",
        "branch": "feature/bruno-dashboard",
        "tarefa": "Dashboard inicial",
        "status": "em_teste",
    },
]

proximo_id = 3


def buscar_card(card_id: int):
    for card in cards:
        if card["id"] == card_id:
            return card
    return None


@app.get("/")
def pagina_inicial():
    return render_template("index.html")


@app.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@app.get("/api/cards")
def listar_cards():
    return jsonify(cards), 200


@app.post("/api/cards")
def criar_card():
    global proximo_id

    dados = request.get_json(silent=True) or {}
    dev = (dados.get("dev") or "").strip()
    tarefa = (dados.get("tarefa") or "").strip()
    branch = (dados.get("branch") or "").strip()

    if not dev or not tarefa or not branch:
        return jsonify({"erro": "Envie os campos: dev, tarefa e branch"}), 400

    card = {
        "id": proximo_id,
        "dev": dev,
        "branch": branch,
        "tarefa": tarefa,
        "status": "backlog",
    }
    cards.append(card)
    proximo_id += 1

    return jsonify(card), 201


@app.patch("/api/cards/<int:card_id>/status")
def atualizar_status(card_id: int):
    dados = request.get_json(silent=True) or {}
    status = dados.get("status")

    if status not in STATUS_VALIDOS:
        return jsonify({"erro": f"Status inválido: {status}"}), 400

    card = buscar_card(card_id)
    if card is None:
        return jsonify({"erro": "Card não encontrado"}), 404

    card["status"] = status
    return jsonify(card), 200


@app.post("/api/simular-erro")
def simular_erro_execucao():
    try:
        _ = 1 / 0
    except ZeroDivisionError:
        return (
            jsonify(
                {
                    "erro": "Simulação de erro em execução: divisão por zero.",
                    "tipo": "ZeroDivisionError",
                }
            ),
            500,
        )

    return jsonify({"mensagem": "Sem erro"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
