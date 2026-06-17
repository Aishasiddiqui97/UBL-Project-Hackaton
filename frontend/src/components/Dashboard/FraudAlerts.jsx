import { useTheme } from "../../context/ThemeContext";
import { fraudAlerts } from "../../data/mockdata";

const FraudAlerts = ({ limit = 5 }) => {
  const theme = useTheme();
  const statusColors = {
    Open: { bg: "#450a0a", color: "#f87171" },
    "In Progress": { bg: "#431407", color: "#fb923c" },
    Resolved: { bg: "#052e16", color: "#4ade80" },
  };

  return (
    <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
      <h3 style={{ color: theme.text, fontSize: "15px", fontWeight: "600", marginBottom: "16px" }}>Recent Fraud Alerts</h3>
      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        {fraudAlerts.slice(0, limit).map(alert => {
          const s = statusColors[alert.status] || statusColors.Open;
          const probColor = alert.probability >= 80 ? "#f87171" : alert.probability >= 60 ? "#fb923c" : "#4ade80";
          return (
            <div key={alert.id} style={{ background: theme.bg, border: `1px solid ${theme.border}`, borderRadius: "10px", padding: "14px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                <span style={{ color: "#38bdf8", fontSize: "13px", fontWeight: "600" }}>{alert.id}</span>
                <span style={{ background: s.bg, color: s.color, padding: "2px 8px", borderRadius: "20px", fontSize: "11px", fontWeight: "600" }}>{alert.status}</span>
              </div>
              <div style={{ color: theme.text, fontSize: "14px", marginBottom: "4px" }}>{alert.type}</div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ color: theme.subtext, fontSize: "12px" }}>{alert.account} · {alert.date}</span>
                <span style={{ color: probColor, fontSize: "12px", fontWeight: "700" }}>{alert.probability}%</span>
              </div>
              <div style={{ width: "100%", background: theme.border, borderRadius: "20px", height: "4px", marginTop: "8px" }}>
                <div style={{ width: `${alert.probability}%`, background: probColor, borderRadius: "20px", height: "4px" }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default FraudAlerts;