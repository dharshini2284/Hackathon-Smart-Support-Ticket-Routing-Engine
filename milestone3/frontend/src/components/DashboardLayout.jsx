import React, { useState } from "react";
import AgentBoard from "./AgentBoard";
import IncidentPanel from "./IncidentPanel";
import FlashFloodPanel from "./FlashFloodPanel";
import CircuitBreakerCard from "./CircuitBreakerCard";
import TicketTable from "./TicketTable";
import { runSimulation } from "../api/client";

const DashboardLayout = ({
  incidents = [],
  metrics = {},
  tickets = [],
  loading = false,
}) => {
  const [simulating, setSimulating] = useState(false);

  const handleSimulation = async () => {
    try {
      setSimulating(true);
      await runSimulation(300, 0.4); // 300 tickets, 40% duplicates
    } catch (error) {
      console.error("Simulation failed:", error);
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-gray-950 text-white">

      {/* HEADER */}
      <header className="border-b border-gray-800 px-8 py-5 flex justify-between items-center backdrop-blur-md bg-gray-900/60 sticky top-0 z-50">

        {/* LEFT: Simulation Button */}
        <button
          disabled={simulating}
          onClick={handleSimulation}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition ${simulating
              ? "bg-gray-600 cursor-not-allowed"
              : "bg-indigo-600 hover:bg-indigo-700"
            }`}
        >
          {simulating ? "Simulating..." : "Run Simulation"}
        </button>

        {/* CENTER: Title */}
        <div className="text-center">
          <h1 className="text-3xl font-bold tracking-tight">
            AI Incident Management
          </h1>
          <p className="text-sm text-gray-400">
            Real-time monitoring & intelligent orchestration
          </p>
        </div>

        {/* RIGHT: Status Badge */}
        <div className="flex items-center gap-4">
          <div className="px-4 py-1 rounded-full bg-green-600/20 text-green-400 text-sm font-medium border border-green-500/30">
            System Operational
          </div>
        </div>
      </header>

      {/* MAIN CONTENT */}
      <main className="px-8 py-8 space-y-10">

        {loading && (
          <div className="text-center text-gray-400 animate-pulse">
            Loading dashboard data...
          </div>
        )}

        {/* TOP METRICS ROW */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
          <AgentBoard metrics={metrics} />
          <FlashFloodPanel metrics={metrics} />
          <CircuitBreakerCard metrics={metrics} />
        </div>

        {/* INCIDENTS SECTION */}
        <section>
          <h2 className="text-2xl font-semibold mb-4">
            Active Incidents
          </h2>
          <IncidentPanel incidents={incidents} />
        </section>

        {/* TICKETS SECTION */}
        <section>
          <h2 className="text-2xl font-semibold mb-4">
            Ticket Overview
          </h2>
          <TicketTable tickets={tickets} />
        </section>

      </main>
    </div>
  );
};

export default DashboardLayout;