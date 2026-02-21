import { useState } from "react";

function App() {
  const [inputText, setInputText] = useState("");
  const [tickets, setTickets] = useState([]);

  const submitTickets = async () => {
    const ticketArray = inputText
      .split("\n")
      .map(t => t.trim())
      .filter(t => t.length > 0);

    if (ticketArray.length === 0) return;

    const res = await fetch("http://127.0.0.1:8000/tickets/bulk", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(ticketArray)
    });

    const data = await res.json();

    const initialTickets = data.ticket_ids.map((id, index) => ({
      id,
      ticket_text: ticketArray[index],
      status: "processing"
    }));

    setTickets(initialTickets);
    setInputText("");

    data.ticket_ids.forEach(id => pollStatus(id));
  };

  const pollStatus = (ticket_id) => {
    const interval = setInterval(async () => {
      const res = await fetch(`http://127.0.0.1:8000/tickets/${ticket_id}`);
      const data = await res.json();

      if (data.status === "completed") {
        setTickets(prev =>
          prev.map(ticket =>
            ticket.id === ticket_id
              ? { id: ticket_id, ...data }
              : ticket
          )
        );
        clearInterval(interval);
      }
    }, 1500);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h2>Smart Support Monitoring Dashboard</h2>

      <textarea
        rows="6"
        cols="70"
        placeholder="Enter multiple tickets (one per line)"
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />

      <br /><br />

      <button onClick={submitTickets}>
        Process Tickets
      </button>

      <h3 style={{ marginTop: "30px" }}>Ticket Results</h3>

      <table border="1" cellPadding="8" style={{ width: "100%" }}>
        <thead>
          <tr>
            <th>Ticket</th>
            <th>Status</th>
            <th>Category</th>
            <th>Urgency</th>
            <th>Latency (ms)</th>
            <th>Webhook</th>
          </tr>
        </thead>
        <tbody>
          {tickets.map(ticket => (
            <tr key={ticket.id}>
              <td>{ticket.ticket_text}</td>
              <td>{ticket.status}</td>
              <td>{ticket.category || "-"}</td>
              <td>
                {ticket.urgency_score !== undefined
                  ? ticket.urgency_score.toFixed(2)
                  : "-"}
              </td>
              <td>
                {ticket.latency_ms !== undefined
                  ? ticket.latency_ms
                  : "-"}
              </td>
              <td>
                {ticket.webhook_triggered
                  ? "🚨 Triggered"
                  : ticket.status === "completed"
                    ? "—"
                    : "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;