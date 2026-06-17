import { useTheme } from "../../context/ThemeContext";
import { openCases } from "../../data/mockdata";

const OpenCases = ({ limit = 5 }) => {
  const theme = useTheme();
  const priorityColors = {
    High: { bg: "#450a0a", color: "#f87171" },
    Medium: { bg: "#431407", color: "#fb923c" },
    Low: { bg: "#052e16", color: "#4ade80" },
  };
  const statusColors = {
    Open: "#f87171", "In Progress": "#fb923c", Closed: "#4ade80",
  };

  return (
    <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
      <h3 style={{ color: theme.text, fontSize: "15px", fontWeight: "600", marginBottom: "16px" }}>Open Cases</h3>
      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        {openCases.slice(0, limit).map(c => {
          const p = priorityColors[c.priority] || priorityColors.Low;
          return (
            <div key={c.id} style={{ background: theme.bg, border: `1px solid ${theme.border}`, borderRadius: "10px", padding: "14px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
                <span style={{ color: "#38bdf8", fontSize: "12px", fontWeight: "600" }}>{c.id}</span>
                <span style={{ background: p.bg, color: p.color, padding: "2px 8px", borderRadius: "20px", fontSize: "11px", fontWeight: "600" }}>{c.priority}</span>
              </div>
              <div style={{ color: theme.text, fontSize: "14px", marginBottom: "4px" }}>{c.title}</div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: theme.subtext, fontSize: "12px" }}>{c.account} · {c.date}</span>
                <span style={{ color: statusColors[c.status] || "#94a3b8", fontSize: "12px", fontWeight: "500" }}>{c.status}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default OpenCases;