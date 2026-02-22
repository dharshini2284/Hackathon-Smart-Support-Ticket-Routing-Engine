import React, { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import {
  fetchIncidents,
  fetchMetrics,
} from "../api/client";

const Dashboard = () => {
  const [incidents, setIncidents] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadData = async () => {
    try {
      setError(null);

      const [incidentData, metricsData] = await Promise.all([
        fetchIncidents(),
        fetchMetrics(),
      ]);

      setIncidents(incidentData || []);
      setMetrics(metricsData || {});
    } catch (err) {
      console.error("Dashboard load error:", err);
      setError("Failed to load dashboard data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();

    // Auto refresh every 5 seconds
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
      loading={loading}
    />
  );
};

export default Dashboard;