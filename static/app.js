// Frontend logic for the Cashback app - Nology Challenge.
// Plain JavaScript: it only talks to the Python API over HTTP (fetch).

const form = document.getElementById("cashback-form");
const resultEl = document.getElementById("result");
const historyBody = document.getElementById("history-body");

// Format numbers as Brazilian currency (R$ 1.234,56).
const brl = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

// Turn the stored client_type ("vip"/"regular") into a friendly label.
function clientLabel(clientType) {
  return clientType.toLowerCase() === "vip" ? "VIP" : "Comum";
}

// Handle the form: ask the API for the cashback, then refresh the history.
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const params = new URLSearchParams({
    client_type: document.getElementById("client-type").value,
    purchase_amount: document.getElementById("purchase-amount").value,
  });

  const response = await fetch(`/api/cashback?${params}`);
  const data = await response.json();

  resultEl.textContent = `Cashback: ${brl.format(data.cashback)}`;
  resultEl.hidden = false;

  loadHistory();
});

// Load the query history for this IP and render it in the table.
async function loadHistory() {
  const response = await fetch("/api/history");
  const rows = await response.json();

  historyBody.innerHTML = "";

  if (rows.length === 0) {
    historyBody.innerHTML =
      '<tr><td colspan="4" class="empty">Nenhuma consulta ainda.</td></tr>';
    return;
  }

  for (const row of rows) {
    const date = new Date(row.created_at).toLocaleString("pt-BR");
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${clientLabel(row.client_type)}</td>
      <td>${brl.format(row.purchase_amount)}</td>
      <td>${brl.format(row.cashback)}</td>
      <td>${date}</td>
    `;
    historyBody.appendChild(tr);
  }
}

// Show the history as soon as the page opens.
loadHistory();
