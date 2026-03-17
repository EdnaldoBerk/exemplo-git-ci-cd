from app import app


def test_pagina_inicial():
    cliente = app.test_client()
    resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert "Painel Visual de CI/CD" in resposta.get_data(as_text=True)


def test_health_check():
    cliente = app.test_client()
    resposta = cliente.get("/health")

    assert resposta.status_code == 200
    assert resposta.get_json()["status"] == "ok"


def test_listar_cards():
    cliente = app.test_client()
    resposta = cliente.get("/api/cards")

    assert resposta.status_code == 200
    assert isinstance(resposta.get_json(), list)


def test_criar_card():
    cliente = app.test_client()
    resposta = cliente.post(
        "/api/cards",
        json={
            "dev": "Carla",
            "branch": "feature/carla-botao",
            "tarefa": "Novo botão de envio",
        },
    )

    assert resposta.status_code == 201
    corpo = resposta.get_json()
    assert corpo["dev"] == "Carla"
    assert corpo["status"] == "backlog"


def test_criar_card_campos_invalidos():
    cliente = app.test_client()
    resposta = cliente.post(
        "/api/cards",
        json={"dev": "", "branch": "", "tarefa": ""},
    )

    assert resposta.status_code == 400
    assert "Envie os campos" in resposta.get_json()["erro"]


def test_atualizar_status_card():
    cliente = app.test_client()

    criado = cliente.post(
        "/api/cards",
        json={
            "dev": "Diego",
            "branch": "feature/diego-navbar",
            "tarefa": "Navbar com links",
        },
    )
    card_id = criado.get_json()["id"]

    resposta = cliente.patch(
        f"/api/cards/{card_id}/status",
        json={"status": "em_teste"},
    )

    assert resposta.status_code == 200
    assert resposta.get_json()["status"] == "em_teste"


def test_atualizar_status_invalido():
    cliente = app.test_client()
    resposta = cliente.patch("/api/cards/1/status", json={"status": "falhou"})

    assert resposta.status_code == 400
    assert "Status inválido" in resposta.get_json()["erro"]
