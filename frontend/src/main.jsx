import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { ThemeProvider } from "./context/ThemeContext.jsx";
import { AuthProvider } from "./context/AuthContext.jsx";
import { setupTokenRefresh } from "./utils/auth.js";
import { checkAndClearInvalidTokens } from "./utils/clearAuth.js";

// Clear any invalid tokens first
checkAndClearInvalidTokens();

// Setup automatic token refresh
setupTokenRefresh();

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <ThemeProvider>
      <AuthProvider>
        <App />
      </AuthProvider>
    </ThemeProvider>
  </StrictMode>
);