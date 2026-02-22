import React, { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout";

import {
  fetchIncidents,
  fetchMetrics,
  fetchTickets,
} from "../api/client";

const Dashboard = () => {
  const [incidents, setIncidents] = useState([]);
  const [metrics, setMetrics] = useState({});
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    try {
      setError(null);

      const [incidentData, metricsData, ticketsData] =
        await Promise.all([
          fetchIncidents(),
          fetchMetrics(),
          fetchTickets(),
        ]);

      // Handle incident object → convert to array
      // Transform backend incident → UI format
      if (
        incidentData &&
        incidentData.status &&
        incidentData.status !== "NO_ACTIVE_INCIDENT"
      ) {
        const mappedIncident = {
          id: incidentData.incident_id,
          title: `Master Incident (${incidentData.ticket_count} tickets)`,
          description: `High similarity ticket flood detected.`,
          severity: incidentData.severity,
          status: incidentData.status,
          created_at: Date.now(), // optional placeholder
        };

        setIncidents([mappedIncident]);
      } else {
        setIncidents([]);
      }

      setMetrics(metricsData || {});
      setTickets(ticketsData || []);
    } catch (err) {
      console.error("Dashboard load error:", err);
      setError("Failed to load dashboard data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();

    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-950 text-white">
        <div className="bg-red-600/20 border border-red-600 text-red-400 px-6 py-4 rounded-xl">
          {error}
        </div>
      </div>
    );
  }

  return (
    <DashboardLayout
      incidents={incidents}
      metrics={metrics}
      tickets={tickets}
      loading={loading}
    />
  );
};

export default Dashboard;