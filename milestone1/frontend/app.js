const API_BASE = "http://localhost:8000";

async function submitTicket() {
  const text = document.getElementById("ticketText").value;

  if (!text) return;

  const response = await fetch(`${API_BASE}/tickets`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text })
  });

  const data = await response.json();

  document.getElementById("result").innerHTML = `
    <p><strong>ID:</strong> ${data.ticket_id}</p>
    <p><strong>Category:</strong> ${data.category}</p>
    <p><strong>Urgent:</strong> ${data.urgent}</p>
  `;

  document.getElementById("ticketText").value = "";

  loadQueue();
  loadQueueSize();
}

async function loadQueueSize() {
  const response = await fetch(`${API_BASE}/queue`);
  const data = await response.json();
  document.getElementById("queueSize").innerText = data.queue_size;
}

async function loadQueue() {
  const response = await fetch(`${API_BASE}/tickets`);
  const data = await response.json();

  const table = document.getElementById("queueTable");
  table.innerHTML = "";

  data.tickets.forEach(item => {
    const ticket = item.ticket;

    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${ticket.id}</td>
      <td>${ticket.category}</td>
      <td class="${ticket.urgent ? 'urgent' : ''}">
        ${ticket.urgent}
      </td>
    `;
    table.appendChild(row);
  });
}

setInterval(loadQueueSize, 3000);
setInterval(loadQueue, 3000);

loadQueueSize();
loadQueue();