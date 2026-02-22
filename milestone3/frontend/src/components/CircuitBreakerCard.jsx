import React from "react";

const getStateStyles = (state) => {
  switch (state?.toLowerCase()) {
    case "closed":
      return {
        badge: "bg-green-600",
        text: "text-green-400",
        glow: "",
      };
    case "half-open":
      return {
        badge: "bg-yellow-500",
        text: "text-yellow-400",
        glow: "",
      };
    case "open":
      return {
        badge: "bg-red-600 animate-pulse",
        text: "text-red-400",
        glow: "shadow-red-500/40 shadow-lg",
      };
    default:
      return {
        badge: "bg-gray-500",
        text: "text-gray-400",
        glow: "",
      };
  }
};

const CircuitBreakerCard = ({ metrics }) => {
  const breaker = metrics?.circuit_breaker;

  if (!breaker) {
    return (
      <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700">
        <h2 className="text-xl font-bold mb-4">Circuit Breaker</h2>
        <p className="text-gray-400">No breaker data available.</p>
      </div>
    );
  }

  const { state, failure_count, last_failure_time } = breaker;
  const styles = getStateStyles(state);

  return (
    <div
      className={`bg-gray-900 p-6 rounded-2xl border border-gray-800 transition-all duration-300 ${styles.glow}`}
    >
      <h2 className="text-xl font-bold mb-4">Circuit Breaker</h2>

      <div className="flex items-center justify-between mb-4">
        <span className="text-gray-400">State</span>
        <span
          className={`px-3 py-1 rounded-full text-sm font-semibold text-white ${styles.badge}`}
        >
          {state?.toUpperCase()}
        </span>
      </div>

      <div className="space-y-2 text-sm">
        <div className="flex justify-between">
          <span className="text-gray-400">Failure Count</span>
          <span className="text-white font-medium">
            {failure_count ?? 0}
          </span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-400">Last Failure</span>
          <span className={`font-medium ${styles.text}`}>
            {last_failure_time || "N/A"}
          </span>
        </div>
      </div>
    </div>
  );
};

export default CircuitBreakerCard;