// Frontend logic for the Cashback app - Nology Challenge.
// Plain JavaScript: it only talks to the Python API over HTTP (fetch).

const form = document.getElementById("cashback-form");
const amountInput = document.getElementById("purchase-amount");
const resultEl = document.getElementById("result");
const resultValue = document.getElementById("result-value");
const resultMeta = document.getElementById("result-meta");
const historyBody = document.getElementById("history-body");

const prefersReduced = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
).matches;

// Format numbers as Brazilian currency (R$ 1.234,56).
const brl = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

// Turn the stored client_type ("vip"/"regular") into a friendly label.
function clientLabel(clientType) {
  return clientType.toLowerCase() === "vip" ? "VIP" : "Comum";
}

// Count the cashback value up from zero — a small, satisfying reveal.
function animateValue(end) {
  if (prefersReduced) {
    resultValue.textContent = brl.format(end);
    return;
  }
  const duration = 700;
  const start = performance.now();
  function tick(now) {
    const t = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - t, 3); // easeOutCubic
    resultValue.textContent = brl.format(end * eased);
    if (t < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

// Handle the form: ask the API for the cashback, then refresh the history.
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const clientType = document.querySelector(
    'input[name="client_type"]:checked'
  ).value;
  const purchaseAmount = amountInput.value;

  const params = new URLSearchParams({
    client_type: clientType,
    purchase_amount: purchaseAmount,
  });

  const response = await fetch(`/api/cashback?${params}`);
  const data = await response.json();

  // Reveal the result and animate the number.
  resultMeta.textContent = `em uma compra de ${brl.format(
    Number(purchaseAmount)
  )} · cliente ${clientLabel(clientType)}`;
  resultEl.hidden = false;
  resultEl.classList.remove("show");
  void resultEl.offsetWidth; // restart the animation
  resultEl.classList.add("show");
  animateValue(data.cashback);

  loadHistory();
});

// Load the query history for this IP and render it in the table.
async function loadHistory() {
  const response = await fetch("/api/history");
  const rows = await response.json();

  historyBody.innerHTML = "";

  if (rows.length === 0) {
    historyBody.innerHTML =
      '<tr><td colspan="4" class="empty">Nenhuma consulta ainda — calcule a primeira acima.</td></tr>';
    return;
  }

  for (const row of rows) {
    const isVip = row.client_type.toLowerCase() === "vip";
    const date = new Date(row.created_at).toLocaleString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><span class="pill ${isVip ? "pill-vip" : "pill-regular"}">${clientLabel(
      row.client_type
    )}</span></td>
      <td>${brl.format(row.purchase_amount)}</td>
      <td>${brl.format(row.cashback)}</td>
      <td>${date}</td>
    `;
    historyBody.appendChild(tr);
  }
}

// Show the history as soon as the page opens.
loadHistory();
