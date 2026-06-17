import { useTheme } from "../../context/ThemeContext";
import { highRiskAccounts } from "../../data/mockdata";

const HighRiskAccounts = ({ limit = 5 }) => {
  const theme = useTheme();
  return (
    <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
      <h3 style={{ color: theme.text, fontSize: "15px", fontWeight: "600", marginBottom: "16px" }}>High Risk Accounts</h3>
      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        {highRiskAccounts.slice(0, limit).map(acc => {
          const color = acc.riskScore >= 80 ? "#f87171" : "#fb923c";
          return (
            <div key={acc.id} style={{ display: "flex", alignItems: "center", gap: "12px", padding: "12px", background: theme.bg, border: `1px solid ${theme.border}`, borderRadius: "10px" }}>
              <div style={{ width: "36px", height: "36px", background: "#450a0a", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", color: "#f87171", fontWeight: "700", fontSize: "13px", flexShrink: 0 }}>
                {acc.name.charAt(0)}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ color: theme.text, fontSize: "14px", fontWeight: "500" }}>{acc.name}</div>
                <div style={{ color: "#38bdf8", fontSize: "12px" }}>{acc.id}</div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ color, fontSize: "18px", fontWeight: "700" }}>{acc.riskScore}</div>
                <div style={{ color: theme.subtext, fontSize: "11px" }}>{acc.flagged} flagged</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default HighRiskAccounts;