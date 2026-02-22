import React from "react";

/* Severity Badge */
const SeverityBadge = ({ severity }) => {
  const styles = {
    low: "bg-green-600/20 text-green-400 border-green-500/30",
    medium: "bg-yellow-600/20 text-yellow-400 border-yellow-500/30",
    high: "bg-red-600/20 text-red-400 border-red-500/30",
    critical: "bg-red-700/30 text-red-300 border-red-600 animate-pulse",
  };

  const style =
    styles[severity?.toLowerCase()] ||
    "bg-gray-700 text-gray-300 border-gray-600";

  return (
    <span
      className={`px-2 py-1 text-xs rounded-full border font-medium ${style}`}
    >
      {severity?.toUpperCase()}
    </span>
  );
};

/* Status Badge */
const StatusBadge = ({ status }) => {
  const isResolved = status?.toLowerCase() === "resolved";

  return (
    <span
      className={`px-2 py-1 text-xs rounded-full font-medium ${
        isResolved
          ? "bg-green-600/20 text-green-400"
          : "bg-yellow-600/20 text-yellow-400"
      }`}
    >
      {status?.toUpperCase()}
    </span>
  );
};

const TicketTable = ({ incidents }) => {
  // Ensure we have an array
  const incidentList = Array.isArray(incidents) ? incidents : [];

  if (incidentList.length === 0) {
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
              <th className="px-6 py-4">Title</th>
              <th className="px-6 py-4">Severity</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4">Created At</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-gray-800">
            {incidentList.map((incident) => (
              <tr
                key={incident.id}
                className="hover:bg-gray-800 transition duration-200"
              >
                <td className="px-6 py-4 font-medium text-white">{incident.id}</td>
                <td className="px-6 py-4">{incident.title || "Untitled"}</td>
                <td className="px-6 py-4">
                  <SeverityBadge severity={incident.severity} />
                </td>
                <td className="px-6 py-4">
                  <StatusBadge status={incident.status} />
                </td>
                <td className="px-6 py-4 text-gray-400">{incident.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TicketTable;