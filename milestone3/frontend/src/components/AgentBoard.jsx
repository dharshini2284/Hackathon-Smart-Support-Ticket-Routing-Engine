import React from "react";

const StatusIndicator = ({ status }) => {
  const colorMap = {
    healthy: "bg-green-500",
    degraded: "bg-yellow-500",
    down: "bg-red-500",
  };

  return (
    <span
      className={`inline-block w-3 h-3 rounded-full ${
        colorMap[status] || "bg-gray-400"
      }`}
    />
  );
};

const AgentCard = ({ name, status, latency }) => {
  return (
    <div className="bg-gray-800 p-4 rounded-2xl shadow-md hover:shadow-xl transition duration-300 border border-gray-700">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">{name}</h3>
        <StatusIndicator status={status} />
      </div>

      <div className="mt-3 text-sm text-gray-400">
        <p>
          Status:{" "}
          <span className="capitalize font-medium text-white">{status}</span>
        </p>
        <p>Latency: {latency} ms</p>
      </div>
    </div>
  );
};

const AgentBoard = ({ metrics }) => {
  if (!metrics || !metrics.agents) {
    return (
      <div className="bg-gray-800 p-6 rounded-2xl shadow-md border border-gray-700">
        <h2 className="text-xl font-bold mb-4">Agent Status</h2>
        <p className="text-gray-400">No agent data available.</p>
      </div>
    );
  }

  return (
    <div className="bg-gray-900 p-6 rounded-2xl shadow-lg border border-gray-800">
      <h2 className="text-xl font-bold mb-4">AI Agent Board</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {metrics.agents.map((agent, index) => (
          <AgentCard
            key={index}
            name={agent.name}
            status={agent.status}
            latency={agent.latency}
          />
        ))}
      </div>
    </div>
  );
};

export default AgentBoard;