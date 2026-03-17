# Exemplo de GitLab CI/CD - API de Cálculo

Este projeto demonstra o cenário:

> "Nossa equipe está desenvolvendo uma pequena API de cálculo. Cada desenvolvedor trabalha em uma branch diferente, e quando o código é enviado para o repositório o GitLab executa testes automaticamente antes de permitir a integração no projeto principal."

## O que existe neste exemplo

- API em Flask com endpoint de saúde e cálculo
- Testes automatizados com pytest
- Pipeline no GitLab em `.gitlab-ci.yml` que roda os testes em push/MR

## Estrutura

- `app.py`: API e função principal de cálculo
- `tests/test_app.py`: testes unitários e de endpoint
- `.gitlab-ci.yml`: pipeline CI

## Regras de integração (mensagem da apresentação)

- Cada pessoa desenvolve em branch própria (`feature/ana`, `feature/bruno`, etc.)
- Ao abrir Merge Request para `main`, o GitLab roda a stage `test`
- Se qualquer teste falhar, o MR fica bloqueado para merge
- Apenas com pipeline verde o código pode ser integrado

## Como executar localmente

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pytest -q
```

## Como rodar a API localmente

```bash
.venv\Scripts\python app.py
```

Teste rápido:

```bash
curl -X POST http://127.0.0.1:5000/calcular \
  -H "Content-Type: application/json" \
  -d '{"operacao":"soma","a":10,"b":5}'
```

## Roteiro de demo para sua apresentação

1. Mostre que a branch `main` está estável com pipeline verde.
2. Crie uma branch de dev: `feature/ana-ajusta-calculo`.
3. Faça uma mudança que quebre um teste (ex.: alterar regra da divisão).
4. Envie para o GitLab e abra um Merge Request.
5. Mostre o pipeline falhando na stage `test` e o merge bloqueado.
6. Corrija o código na mesma branch.
7. Mostre o novo pipeline passando e o merge sendo liberado.

## Exemplo de comandos Git para encenar o fluxo

```bash
git checkout -b feature/ana-ajusta-calculo
# editar código
.venv\Scripts\python -m pytest -q
git add .
git commit -m "feat: ajusta regra de calculo"
git push -u origin feature/ana-ajusta-calculo
```

Depois, abra o Merge Request no GitLab para `main`.

## Pipeline do GitLab

O arquivo `.gitlab-ci.yml` executa:

- `pip install -r requirements.txt`
- `pytest -q --maxfail=1`

Se `pytest` retornar erro, o job falha e o MR não deve ser integrado.
