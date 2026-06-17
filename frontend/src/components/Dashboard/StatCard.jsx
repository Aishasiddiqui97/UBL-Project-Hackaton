import { useTheme } from "../../context/ThemeContext";

const StatCard = ({ title, value, subtitle, icon, color = "#38bdf8" }) => {
  const theme = useTheme();
  return (
    <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", flex: 1, transition: "all 0.3s" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
        <span style={{ color: theme.subtext, fontSize: "14px" }}>{title}</span>
        <span style={{ fontSize: "22px" }}>{icon}</span>
      </div>
      <div style={{ color, fontSize: "32px", fontWeight: "700" }}>{value}</div>
      {subtitle && <div style={{ color: theme.subtext, fontSize: "12px", marginTop: "6px" }}>{subtitle}</div>}
    </div>
  );
};

export default StatCard;