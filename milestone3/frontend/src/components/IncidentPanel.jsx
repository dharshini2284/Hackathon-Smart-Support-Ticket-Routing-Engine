import React from "react";
import { formatDate, timeAgo } from "../utils/formatDate";

/* Severity color mapping */
const getSeverityStyles = (severity = "") => {
  switch (severity.toLowerCase()) {
    case "low":
      return "bg-green-600/20 text-green-400 border-green-500/30";
    case "medium":
      return "bg-yellow-600/20 text-yellow-400 border-yellow-500/30";
    case "high":
      return "bg-red-600/20 text-red-400 border-red-500/30";
    case "critical":
      return "bg-red-700/30 text-red-300 border-red-600 animate-pulse";
    default:
      return "bg-gray-700 text-gray-300 border-gray-600";
  }
};

const IncidentCard = ({ incident }) => {
  if (!incident) return null;

  const {
    id = "N/A",
    title = "Untitled Incident",
    description = "No description available.",
    severity = "unknown",
    status = "open",
    created_at,
  } = incident;

  const severityStyle = getSeverityStyles(severity);
  const isResolved = status?.toLowerCase() === "resolved";

  return (
    <div className="bg-gray-900 p-5 rounded-2xl border border-gray-800 hover:shadow-xl transition duration-300">
      
      {/* Header */}
      <div className="flex justify-between items-center mb-3">
        <span
          className={`px-3 py-1 text-xs font-semibold rounded-full border ${severityStyle}`}
        >
          {severity.toUpperCase()}
        </span>

        <span
          className={`text-xs font-medium ${
            isResolved ? "text-green-400" : "text-yellow-400"
          }`}
        >
          {status.toUpperCase()}
        </span>
      </div>

      {/* Title */}
      <h3 className="text-lg font-semibold mb-2">
        {title}
      </h3>

      {/* Description */}
      <p className="text-sm text-gray-400 mb-4 line-clamp-3">
        {description}
      </p>

      {/* Footer */}
      <div className="flex justify-between text-xs text-gray-500">
        <span>ID: {id}</span>
        <span title={formatDate(created_at)}>
          {timeAgo(created_at)}
        </span>
      </div>
    </div>
  );
};

const IncidentPanel = ({ incidents = [] }) => {
  if (!Array.isArray(incidents) || incidents.length === 0) {
    return (
      <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700">
        <h3 className="text-lg font-semibold mb-2">Active Incidents</h3>
        <p className="text-gray-400">No incidents detected 🎉</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      {incidents.map((incident, index) => (
        <IncidentCard
          key={incident?.id || index}
          incident={incident}
        />
      ))}
    </div>
  );
};

export default IncidentPanel;