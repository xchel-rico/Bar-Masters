import { API_BASE } from "./config.js";

// --- UTILITÁRIOS ---

function showMessage(id, msg, isError = false) {
  const el = document.getElementById(id);
  if (el) {
    el.textContent = msg;
    el.style.color = isError ? "#f75a68" : "#04d361";
  }
}

// Verifica se há usuário logado
function getCurrentUser() {
  const user = localStorage.getItem("bm_user");
  return user ? JSON.parse(user) : null;
}

// Atualiza o menu (Entrar vs Sair)
function updateNav() {
  const authLink = document.getElementById("nav-auth");
  if (!authLink) return;

  const user = getCurrentUser();
  if (user) {
    authLink.textContent = `Sair (${user.name.split(" ")[0]})`;
    authLink.href = "#";
    authLink.onclick = () => {
      localStorage.removeItem("bm_user");
      window.location.href = "login.html";
    };
  } else {
    authLink.textContent = "Entrar";
    authLink.href = "login.html";
  }
}
// Executa ao carregar
updateNav();


function renderBars(bars) {
  const list = document.getElementById("bars-list");
  if (!list) return;

  list.innerHTML = "";
  if (!bars || bars.length === 0) {
    list.innerHTML = '<p class="empty-state">Nenhum bar encontrado.</p>';
    return;
  }

  bars.forEach((b) => {
    const div = document.createElement("div");
    div.className = "bar-item";
    div.innerHTML = `
      <div class="bar-header">
        <h3>${b.name}</h3>
        <a href="bar.html?id=${b.id}" class="btn-outline" style="padding: 2px 8px; font-size: 0.8rem; text-decoration: none;">Ver</a>
      </div>
      <p style="color: #a8a8b3; font-size: 0.9rem;">${b.description || "Sem descrição"}</p>
      <small style="display:block; margin-top:0.5rem">📍 ${b.address}</small>
    `;
    list.appendChild(div);
  });
}

// ==========================================
// LÓGICA POR PÁGINA
// ==========================================

// 1. PÁGINA DE LOGIN
const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.onsubmit = async (e) => {
    e.preventDefault();
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    try {
      const res = await fetch(`${API_BASE}/api/users/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) throw new Error("Email ou senha inválidos");

      const user = await res.json();
      // Salva no navegador
      localStorage.setItem("bm_user", JSON.stringify(user));
      
      showMessage("login-feedback", "Login realizado! Redirecionando...");
      setTimeout(() => window.location.href = "index.html", 1000);

    } catch (err) {
      showMessage("login-feedback", err.message, true);
    }
  };
}

// 2. PÁGINA "TODOS OS BARES" (Carregamento Automático)
if (window.location.pathname.includes("bars.html")) {
    // Busca os 100 bares mais recentes ao abrir a página
    fetch(`${API_BASE}/api/bars/newest?limit=100`)
      .then(res => res.json())
      .then(bars => renderBars(bars))
      .catch(() => {
        const list = document.getElementById("bars-list");
        if(list) list.innerHTML = "Erro ao carregar bares.";
      });
}

// 3. PÁGINA DE CADASTRO DE USUÁRIO (Signup)
const userForm = document.getElementById("user-form");
if (userForm) {
  userForm.onsubmit = async (e) => {
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
      showMessage("user-feedback", "Conta criada! Vá para o login.");
      e.target.reset();
    } catch (err) {
      showMessage("user-feedback", err.message, true);
    }
  };
}

// 4. PÁGINA DE CADASTRO DE BAR (Exige Login)
const barForm = document.getElementById("bar-form");
if (barForm) {
    const user = getCurrentUser();
    if (!user) {
        document.querySelector("main").innerHTML = `
            <div style="text-align:center; margin-top: 3rem;">
                <h2>🚫 Acesso Restrito</h2>
                <p>Você precisa estar logado para cadastrar um bar.</p>
                <a href="login.html"><button class="btn-primary" style="width:200px">Fazer Login</button></a>
            </div>
        `;
    } else {
        // Preenche o ID do dono automaticamente
        document.getElementById("bar-owner").value = user.id;
        document.getElementById("bar-owner").readOnly = true;

        barForm.onsubmit = async (e) => {
            e.preventDefault();
            const name = document.getElementById("bar-name").value;
            const address = document.getElementById("bar-address").value;
            const description = document.getElementById("bar-desc").value;
            
            try {
            const res = await fetch(`${API_BASE}/api/bars`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, address, description, owner_id: user.id }),
            });
            if (!res.ok) throw new Error("Erro ao cadastrar.");
            const bar = await res.json();
            showMessage("bar-feedback", `Bar criado! ID: ${bar.id}`);
            e.target.reset();
            } catch (err) {
            showMessage("bar-feedback", err.message, true);
            }
        };
    }
}

// 5. BUSCA
const searchForm = document.getElementById("search-form");
if (searchForm) {
  
  // Ação do Botão Buscar
  searchForm.onsubmit = async (e) => {
    e.preventDefault();
    const text = document.getElementById("search-text").value;
    try {
      const res = await fetch(`${API_BASE}/api/bars/search?q=${encodeURIComponent(text)}`);
      renderBars(await res.json());
    } catch { renderBars([]); }
  };

  // Ação do Botão "Aleatório" (Redireciona para o bar)
  const randomBtn = document.getElementById("random-btn");
  if (randomBtn) {
    randomBtn.onclick = async () => {
        try {
            const res = await fetch(`${API_BASE}/api/bars/random`);
            const bar = await res.json();
            // Se encontrou um bar, vai para a página dele
            if (bar && bar.id) {
                window.location.href = `bar.html?id=${bar.id}`;
            } else {
                showMessage("search-feedback", "Nenhum bar encontrado.", true); // Caso o banco esteja vazio
            }
        } catch (err) {
            console.error(err);
        }
    };
  }

  // Ação do Botão "Novos" (Lista na tela)
  const newestBtn = document.getElementById("newest-btn");
  if (newestBtn) {
    newestBtn.onclick = async () => {
        try {
            const res = await fetch(`${API_BASE}/api/bars/newest`);
            const bars = await res.json();
            renderBars(bars);
        } catch (err) {
            console.error(err);
        }
    };
  }
}

// 6. DETALHES DO BAR (Exige Login para Avaliar)
const detailsCard = document.getElementById("bar-details-card");
if (detailsCard) {
  const params = new URLSearchParams(window.location.search);
  const barId = params.get("id");

  // Carrega infos do bar
  if (barId) {
    fetch(`${API_BASE}/api/bars/${barId}`)
      .then(res => res.ok ? res.json() : null)
      .then(bar => {
        if(bar) {
            document.getElementById("detail-name").textContent = bar.name;
            document.getElementById("detail-desc").textContent = bar.description;
            document.getElementById("detail-address").textContent = bar.address;
            document.getElementById("detail-owner").textContent = bar.owner_id;
        }
      });
  }

  // Verifica Login para mostrar formulário de avaliação
  const rateSection = document.getElementById("rate-section"); // Vamos adicionar esse ID no HTML
  const user = getCurrentUser();

  if (!user) {
      if(rateSection) {
          rateSection.innerHTML = `
            <div style="background: #202024; padding: 1rem; border-radius: 8px; text-align: center;">
                <p>🔒 <strong>Faça login</strong> para avaliar este bar.</p>
                <a href="login.html" class="btn-outline" style="display:inline-block; margin-top:0.5rem; padding: 0.5rem 1rem;">Entrar</a>
            </div>
          `;
      }
  } else {
      // Se logado, habilita o form
      const rateForm = document.getElementById("rate-form");
      if (rateForm) {
        document.getElementById("rate-user-id").value = user.id; // Campo oculto
        
        rateForm.onsubmit = async (e) => {
            e.preventDefault();
            const score = Number(document.getElementById("rate-score").value);
            const comment = document.getElementById("rate-comment").value;

            try {
            const res = await fetch(`${API_BASE}/api/bars/${barId}/rate`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: user.id, score, comment }),
            });
            if (!res.ok) throw new Error("Erro ao avaliar.");
            showMessage("rate-feedback", "Avaliação enviada!");
            e.target.reset();
            } catch (err) {
            showMessage("rate-feedback", err.message, true);
            }
        };
      }
  }
}