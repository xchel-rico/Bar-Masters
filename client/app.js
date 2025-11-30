import { API_BASE } from "./config.js";

// Helper to show messages
function showMessage(id, msg, isError = false) {
  const el = document.getElementById(id);
  el.textContent = msg;
  el.style.color = isError ? "#f87171" : "#4ade80";
}

// Render bars list
function renderBars(bars) {
  const list = document.getElementById("bars-list");
  list.innerHTML = "";

  if (!bars || bars.length === 0) {
    list.textContent = "Nenhum bar encontrado.";
    return;
  }

  bars.forEach((b) => {
    const div = document.createElement("div");
    div.className = "bar-item";
    div.innerHTML = `
      <strong>${b.name}</strong> (id: ${b.id})<br>
      ${b.description || "Sem descrição"}<br>
      Endereço: ${b.address}<br>
      Dono: ${b.owner_id}<br>
      Criado em: ${b.created_at}
    `;
    list.appendChild(div);
  });
}

// ----------------------
// Registrar usuário
// ----------------------
document.getElementById("user-form").onsubmit = async (e) => {
  e.preventDefault();

  const name = document.getElementById("user-name").value;
  const email = document.getElementById("user-email").value;
  const password = document.getElementById("user-password").value;

  try {
    const res = await fetch(`${API_BASE}/api/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    });

    if (!res.ok) throw new Error("Erro ao registrar.");

    const user = await res.json();
    showMessage("user-feedback", `Usuário criado! ID: ${user.id}`);
    e.target.reset();
  } catch (err) {
    showMessage("user-feedback", err.message, true);
  }
};

// ----------------------
// Registrar bar
// ----------------------
document.getElementById("bar-form").onsubmit = async (e) => {
  e.preventDefault();

  const name = document.getElementById("bar-name").value;
  const address = document.getElementById("bar-address").value;
  const description = document.getElementById("bar-desc").value;
  const owner_id = Number(document.getElementById("bar-owner").value);

  try {
    const res = await fetch(`${API_BASE}/api/bars`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, address, description, owner_id }),
    });

    if (!res.ok) throw new Error("Erro ao cadastrar bar.");

    const bar = await res.json();
    showMessage("bar-feedback", `Bar cadastrado! ID: ${bar.id}`);
    e.target.reset();
  } catch (err) {
    showMessage("bar-feedback", err.message, true);
  }
};

// ----------------------
// Buscar bares
// ----------------------
document.getElementById("search-btn").onclick = async () => {
  const text = document.getElementById("search-text").value;

  try {
    const res = await fetch(`${API_BASE}/api/bars/search?q=${encodeURIComponent(text)}`);
    const bars = await res.json();
    renderBars(bars);
  } catch {
    renderBars([]);
  }
};

// ----------------------
// Bar aleatório
// ----------------------
document.getElementById("random-btn").onclick = async () => {
  const res = await fetch(`${API_BASE}/api/bars/random`);
  const bar = await res.json();
  renderBars(bar ? [bar] : []);
};

// ----------------------
// Novos bares
// ----------------------
document.getElementById("newest-btn").onclick = async () => {
  const res = await fetch(`${API_BASE}/api/bars/newest`);
  const bars = await res.json();
  renderBars(bars);
};

// ----------------------
// Avaliar bar
// ----------------------
document.getElementById("rate-form").onsubmit = async (e) => {
  e.preventDefault();

  const bar_id = Number(document.getElementById("rate-bar-id").value);
  const user_id = Number(document.getElementById("rate-user-id").value);
  const score = Number(document.getElementById("rate-score").value);
  const comment = document.getElementById("rate-comment").value;

  try {
    const res = await fetch(`${API_BASE}/api/bars/${bar_id}/rate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id, score, comment }),
    });

    if (!res.ok) throw new Error("Erro ao enviar avaliação.");

    const rating = await res.json();
    showMessage("rate-feedback", `Avaliação registrada! ID: ${rating.id}`);
    e.target.reset();
  } catch (err) {
    showMessage("rate-feedback", err.message, true);
  }
};
