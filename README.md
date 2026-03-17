# Exemplo de GitLab CI/CD - Painel Visual

Este projeto demonstra o cenário de forma visual:

> "Nossa equipe trabalha em branches separadas, e quando o código é enviado para o GitLab os testes rodam automaticamente antes de liberar a integração na main."

## O que existe neste exemplo

- Interface web com quadro visual (Backlog -> Em teste -> Aprovado)
- API em Flask para criar cards e mover status
- Testes automatizados com pytest
- Pipeline no GitLab em `.gitlab-ci.yml` que roda os testes em push/MR

## Estrutura

- `app.py`: backend Flask e rotas da API
- `templates/index.html`: interface visual
- `static/style.css`: estilo do painel
- `static/app.js`: lógica da interface
- `tests/test_app.py`: testes de página e endpoints
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

## Como abrir o painel visual

```bash
.venv\Scripts\python app.py
```

Depois abra no navegador:

- `http://127.0.0.1:5000`

Teste rápido de API (PowerShell):

```bash
$body = '{"dev":"Carlos","branch":"feature/carlos-carrinho","tarefa":"Tela de carrinho"}'
Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:5000/api/cards' -ContentType 'application/json' -Body $body | ConvertTo-Json
```
