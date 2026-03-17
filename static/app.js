const colunas = {
  backlog: document.getElementById("coluna-backlog"),
  em_teste: document.getElementById("coluna-em_teste"),
  aprovado: document.getElementById("coluna-aprovado"),
};

const statusSequencia = ["backlog", "em_teste", "aprovado"];
const outputRuntime = document.getElementById("runtime-output");

function mostrarOutputRuntime(texto, tipo) {
  outputRuntime.classList.remove("ok", "error");
  outputRuntime.classList.add(tipo);
  outputRuntime.textContent = texto;
}

function limparColunas() {
  Object.values(colunas).forEach((coluna) => {
    coluna.innerHTML = "";
  });
}

function proximoStatus(atual) {
  const indice = statusSequencia.indexOf(atual);
  if (indice === -1 || indice === statusSequencia.length - 1) {
    return null;
  }
  return statusSequencia[indice + 1];
}

async function carregarCards() {
  const resposta = await fetch("/api/cards");
  const cards = await resposta.json();

  limparColunas();

  cards.forEach((card) => {
    const elemento = document.createElement("article");
    elemento.className = "card";

    const proximo = proximoStatus(card.status);
    const botaoAcao = proximo
      ? `<button data-id="${card.id}" data-status="${proximo}" class="warn">Mover para ${proximo.replace("_", " ")}</button>`
      : "";

    elemento.innerHTML = `
      <strong>${card.tarefa}</strong>
      <small>${card.dev} • ${card.branch}</small>
      <div class="actions">${botaoAcao}</div>
    `;

    colunas[card.status].appendChild(elemento);
  });

  document.querySelectorAll(".actions button").forEach((botao) => {
    botao.addEventListener("click", async (evento) => {
      const id = Number(evento.currentTarget.dataset.id);
      const status = evento.currentTarget.dataset.status;

      await fetch(`/api/cards/${id}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      });

      await carregarCards();
    });
  });
}

document
  .getElementById("novo-card-form")
  .addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const dev = document.getElementById("dev").value;
    const branch = document.getElementById("branch").value;
    const tarefa = document.getElementById("tarefa").value;

    await fetch("/api/cards", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ dev, branch, tarefa }),
    });

    evento.target.reset();
    await carregarCards();
  });

carregarCards();

document
  .getElementById("simular-erro-btn")
  .addEventListener("click", async () => {
    const resposta = await fetch("/api/simular-erro", {
      method: "POST",
    });

    const corpo = await resposta.json();
    if (!resposta.ok) {
      mostrarOutputRuntime(
        `Erro ${resposta.status} - ${corpo.tipo}: ${corpo.erro}`,
        "error"
      );
      return;
    }

    mostrarOutputRuntime(`Sucesso ${resposta.status}: ${corpo.mensagem}`, "ok");
  });
