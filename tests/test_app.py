from app import app, calcular


def test_calcular_soma():
    assert calcular("soma", 2, 3) == 5


def test_calcular_subtracao():
    assert calcular("subtracao", 10, 4) == 6


def test_calcular_multiplicacao():
    assert calcular("multiplicacao", 3, 7) == 21


def test_calcular_divisao():
    assert calcular("divisao", 12, 3) == 4


def test_health_check():
    cliente = app.test_client()
    resposta = cliente.get("/health")

    assert resposta.status_code == 200
    assert resposta.get_json()["status"] == "ok"


def test_calcular_endpoint_sucesso():
    cliente = app.test_client()
    resposta = cliente.post(
        "/calcular",
        json={"operacao": "soma", "a": 5, "b": 8},
    )

    assert resposta.status_code == 200
    assert resposta.get_json()["resultado"] == 13


def test_calcular_endpoint_divisao_por_zero():
    cliente = app.test_client()
    resposta = cliente.post(
        "/calcular",
        json={"operacao": "divisao", "a": 9, "b": 0},
    )

    assert resposta.status_code == 400
    assert "Divisão por zero" in resposta.get_json()["erro"]
