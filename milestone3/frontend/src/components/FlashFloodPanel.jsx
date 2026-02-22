import React from "react";

const FlashFloodPanel = ({ metrics }) => {
  const flood = metrics?.flash_flood;

  if (!flood) {
    return (
      <div className="bg-gray-800 p-6 rounded-2xl border border-gray-700">
        <h2 className="text-xl font-bold mb-4">Flash Flood Monitor</h2>
        <p className="text-gray-400">No traffic data available.</p>
      </div>
    );
  }

  const {
    current_rate,
    threshold,
    status, // "normal" | "surge"
    window_seconds
  } = flood;

  const isSurge = status?.toLowerCase() === "surge";

  return (
    <div
      className={`bg-gray-900 p-6 rounded-2xl border transition-all duration-300 ${
        isSurge
          ? "border-red-600 shadow-red-500/30 shadow-lg"
          : "border-gray-800"
      }`}
    >
      <h2 className="text-xl font-bold mb-4">Flash Flood Monitor</h2>

      {/* STATUS BADGE */}
      <div className="flex justify-between items-center mb-4">
        <span className="text-gray-400">Status</span>
        <span
          className={`px-3 py-1 rounded-full text-sm font-semibold ${
            isSurge
              ? "bg-red-600 animate-pulse text-white"
              : "bg-green-600 text-white"
          }`}
        >
          {isSurge ? "SURGE DETECTED" : "NORMAL"}
        </span>
      </div>

      {/* METRICS */}
      <div className="space-y-3 text-sm">

        <div className="flex justify-between">
          <span className="text-gray-400">Current Rate</span>
          <span
            className={`font-semibold ${
              isSurge ? "text-red-400" : "text-white"
            }`}
          >
            {current_rate} req/s
          </span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-400">Threshold</span>
          <span className="text-white font-medium">
            {threshold} req/s
          </span>
        </div>

        <div className="flex justify-between">
          <span className="text-gray-400">Window</span>
          <span className="text-white font-medium">
            {window_seconds}s
          </span>
        </div>

      </div>

      {/* ALERT MESSAGE */}
      {isSurge && (
        <div className="mt-4 text-sm text-red-400 border-t border-red-800 pt-3">
          Traffic surge detected. System may trigger rate limiting or fallback routing.
        </div>
      )}
    </div>
  );
};

export default FlashFloodPanel;