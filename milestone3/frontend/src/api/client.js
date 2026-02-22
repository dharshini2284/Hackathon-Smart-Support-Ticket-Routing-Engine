import axios from "axios";

/**
 * Base API configuration
 * Change this in production using environment variables
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
 * Optional: Response interceptor for global error handling
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
 * Get all incidents
 */
export const fetchIncidents = async () => {
  const response = await apiClient.get("/incidents");
  console.log(response.data);
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
 * Analyze a new ticket
 */
export const analyzeTicket = async (payload) => {
  const response = await apiClient.post("/analyze", payload);
  return response.data;
};

/**
 * Health check
 */
export const checkHealth = async () => {
  const response = await apiClient.get("/health");
  return response.data;
};

export default apiClient;