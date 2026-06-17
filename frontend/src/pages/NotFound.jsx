import { useNavigate } from "react-router-dom";
import { useTheme } from "../context/ThemeContext";
import { ShieldOff, ArrowLeft } from "lucide-react";

function NotFound() {
  const navigate = useNavigate();
  const theme = useTheme();

  return (
    <div style={{
      minHeight: "100vh",
      background: theme.bg,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      flexDirection: "column",
      gap: "24px",
      textAlign: "center",
      padding: "40px",
    }}>
      <div style={{
        background: "#f8717120",
        borderRadius: "50%",
        width: "80px",
        height: "80px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}>
        <ShieldOff size={36} color="#f87171" />
      </div>

      <div>
        <div style={{ color: "#f87171", fontSize: "72px", fontWeight: "700", lineHeight: 1, letterSpacing: "-2px" }}>404</div>
        <div style={{ color: theme.text, fontSize: "20px", fontWeight: "600", marginTop: "12px" }}>Page Not Found</div>
        <div style={{ color: theme.subtext, fontSize: "14px", marginTop: "8px", maxWidth: "320px" }}>
          The page you're looking for doesn't exist or you don't have access.
        </div>
      </div>

      <div style={{ display: "flex", gap: "12px" }}>
        <button
          onClick={() => navigate(-1)}
          style={{
            display: "flex", alignItems: "center", gap: "8px",
            background: "none", border: `1px solid ${theme.border}`,
            borderRadius: "8px", padding: "10px 20px",
            color: theme.subtext, fontSize: "14px", cursor: "pointer",
          }}
        >
          <ArrowLeft size={15} /> Go Back
        </button>
        <button
          onClick={() => navigate("/dashboard")}
          style={{
            display: "flex", alignItems: "center", gap: "8px",
            background: "#2563eb", border: "none",
            borderRadius: "8px", padding: "10px 20px",
            color: "white", fontSize: "14px", fontWeight: "600", cursor: "pointer",
          }}
        >
          Go to Dashboard
        </button>
      </div>

      <div style={{ color: theme.subtext, fontSize: "12px", marginTop: "8px" }}>
        AFCIP v2.1 · Secure Intelligence Platform
      </div>
    </div>
  );
}

export default NotFound;