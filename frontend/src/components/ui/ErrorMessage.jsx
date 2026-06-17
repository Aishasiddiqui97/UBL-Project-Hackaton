import { useTheme } from "../../context/ThemeContext";

const ErrorMessage = ({ message = "Something went wrong." }) => {
  const theme = useTheme();
  return (
    <div style={{ background: "#450a0a", border: "1px solid #f87171", borderRadius: "10px", padding: "14px 18px", display: "flex", alignItems: "center", gap: "10px" }}>
      <span style={{ fontSize: "18px" }}>⚠️</span>
      <span style={{ color: "#f87171", fontSize: "14px" }}>{message}</span>
    </div>
  );
};

export default ErrorMessage;