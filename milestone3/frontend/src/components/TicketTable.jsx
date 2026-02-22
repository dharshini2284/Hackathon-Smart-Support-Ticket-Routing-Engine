import React from "react";

const TicketTable = ({ tickets = [] }) => {
  if (!Array.isArray(tickets) || tickets.length === 0) {
    return (
      <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700">
        <p className="text-gray-400">No tickets available.</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-900 rounded-2xl border border-gray-800 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm text-left text-gray-300">
          <thead className="bg-gray-800 text-gray-400 uppercase text-xs tracking-wider">
            <tr>
              <th className="px-6 py-4">Ticket ID</th>
              <th className="px-6 py-4">Category</th>
              <th className="px-6 py-4">Urgency</th>
              <th className="px-6 py-4">Agent</th>
              <th className="px-6 py-4">Priority</th>
              <th className="px-6 py-4">Breaker</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-gray-800">
            {tickets.map((ticket, index) => (
              <tr
                key={index}
                className="hover:bg-gray-800 transition duration-200"
              >
                <td className="px-6 py-4 font-medium text-white">
                  {ticket.ticket_id}
                </td>
                <td className="px-6 py-4">
                  {ticket.category}
                </td>
                <td className="px-6 py-4">
                  {ticket.urgency_score}
                </td>
                <td className="px-6 py-4">
                  {ticket.assigned_agent}
                </td>
                <td className="px-6 py-4">
                  {ticket.priority}
                </td>
                <td className="px-6 py-4">
                  {ticket.circuit_breaker_state}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TicketTable;