/**
 * Safely formats a date string into a readable format.
 * Example output: "Feb 21, 2026 • 14:32"
 */
export const formatDate = (dateInput) => {
    if (!dateInput) return "N/A";
  
    const date = new Date(dateInput);
    if (isNaN(date.getTime())) return "Invalid Date";
  
    return date.toLocaleString(undefined, {
      year: "numeric",
      month: "short",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    });
  };
  
  /**
   * Returns relative time like:
   * "5m ago", "2h ago", "3d ago"
   */
  export const timeAgo = (dateInput) => {
    if (!dateInput) return "N/A";
  
    const date = new Date(dateInput);
    if (isNaN(date.getTime())) return "Invalid Date";
  
    const now = new Date();
    const diffMs = now - date;
  
    const seconds = Math.floor(diffMs / 1000);
    const minutes = Math.floor(diffMs / (1000 * 60));
    const hours = Math.floor(diffMs / (1000 * 60 * 60));
    const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  
    if (seconds < 60) return `${seconds}s ago`;
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
  };
  
  /**
   * Formats date for compact display
   * Example: 21/02/2026
   */
  export const formatShortDate = (dateInput) => {
    if (!dateInput) return "N/A";
  
    const date = new Date(dateInput);
    if (isNaN(date.getTime())) return "Invalid Date";
  
    return date.toLocaleDateString();
  };