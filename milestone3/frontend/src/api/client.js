import axios from "axios";

/**
 * Base API URL
 */
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/**
 * Axios instance
 */
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 8000,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Global error handler
 */
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error?.response?.data || error.message);
    return Promise.reject(error);
  }
);

/* ============================
   API FUNCTIONS
============================ */

/**
 * Get current active incident
 */
export const fetchIncidents = async () => {
  const response = await apiClient.get("/incidents");
  return response.data;
};

/**
 * Get system metrics
 */
export const fetchMetrics = async () => {
  const response = await apiClient.get("/metrics");
  return response.data;
};

/**
 * Get processed tickets
 */
export const fetchTickets = async () => {
  const response = await apiClient.get("/tickets");
  return response.data;
};

/**
 * Submit ticket
 */
export const analyzeTicket = async (payload) => {
  const response = await apiClient.post("/tickets", payload);
  return response.data;
};

/**
 * Health check
 */
export const checkHealth = async () => {
  const response = await apiClient.get("/health");
  return response.data;
};

export const runSimulation = async (
  num_tickets = 200,
  duplicate_ratio = 0.3
) => {
  const response = await apiClient.post(
    `/simulate?num_tickets=${num_tickets}&duplicate_ratio=${duplicate_ratio}`
  );
  return response.data;
};

export default apiClient;