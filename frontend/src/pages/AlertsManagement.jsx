import { useState } from "react";
import PageLayout from "../components/layout/PageLayout";
import { fraudAlerts } from "../data/mockdata";
import { useTheme } from "../context/ThemeContext";

function StatusBadge({ status }) {
  const colors = {
    Open: { bg: "#450a0a", color: "#f87171" },
    "In Progress": { bg: "#431407", color: "#fb923c" },
    Resolved: { bg: "#052e16", color: "#4ade80" },
  };
  const c = colors[status] || colors.Open;
  return <span style={{ background: c.bg, color: c.color, padding: "4px 12px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>{status}</span>;
}

function ProbabilityBar({ value }) {
  const color = value >= 80 ? "#ef4444" : value >= 60 ? "#f59e0b" : "#22c55e";
  return (
    <div style={{ width: "100%", background: "#0f172a", borderRadius: "20px", height: "6px", marginTop: "6px" }}>
      <div style={{ width: `${value}%`, background: color, borderRadius: "20px", height: "6px", transition: "width 0.4s" }} />
    </div>
  );
}

function AlertsManagement() {
  const theme = useTheme();
  const [alerts, setAlerts] = useState(fraudAlerts);
  const [selected, setSelected] = useState(null);
  const [filterStatus, setFilterStatus] = useState("All");

  const filtered = alerts.filter((a) => filterStatus === "All" || a.status === filterStatus);

  const updateStatus = (id, newStatus) => {
    setAlerts((prev) => prev.map((a) => a.id === id ? { ...a, status: newStatus } : a));
    setSelected((prev) => prev ? { ...prev, status: newStatus } : prev);
  };

  const statCards = [
    { label: "Total Alerts", value: alerts.length, color: "#38bdf8" },
    { label: "Open", value: alerts.filter(a => a.status === "Open").length, color: "#f87171" },
    { label: "In Progress", value: alerts.filter(a => a.status === "In Progress").length, color: "#fb923c" },
    { label: "Resolved", value: alerts.filter(a => a.status === "Resolved").length, color: "#4ade80" },
  ];

  return (
    <PageLayout title="Alerts Management">
      <div style={{ display: "flex", gap: "16px", marginBottom: "28px" }}>
        {statCards.map((card) => (
          <div key={card.label} style={{ flex: 1, background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "20px" }}>
            <div style={{ color: theme.subtext, fontSize: "13px", marginBottom: "8px" }}>{card.label}</div>
            <div style={{ color: card.color, fontSize: "28px", fontWeight: "700" }}>{card.value}</div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: "12px", marginBottom: "20px" }}>
        {["All", "Open", "In Progress", "Resolved"].map((s) => (
          <button key={s} onClick={() => setFilterStatus(s)} style={{
            padding: "8px 18px", borderRadius: "8px", fontSize: "13px", cursor: "pointer",
            border: filterStatus === s ? "1px solid #38bdf8" : `1px solid ${theme.border}`,
            background: filterStatus === s ? "#1e3a5f" : theme.surface,
            color: filterStatus === s ? "#38bdf8" : theme.subtext,
          }}>{s}</button>
        ))}
      </div>

      <div style={{ display: "flex", gap: "20px" }}>
        <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: "12px" }}>
          {filtered.map((alert) => (
            <div key={alert.id} onClick={() => setSelected(alert)} style={{
              background: theme.surface,
              border: selected?.id === alert.id ? "1px solid #38bdf8" : `1px solid ${theme.border}`,
              borderRadius: "12px", padding: "18px", cursor: "pointer", transition: "all 0.2s",
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                <span style={{ color: "#38bdf8", fontSize: "13px", fontWeight: "600" }}>{alert.id}</span>
                <StatusBadge status={alert.status} />
              </div>
              <div style={{ color: theme.text, fontSize: "15px", fontWeight: "500", marginBottom: "4px" }}>{alert.type}</div>
              <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "10px" }}>{alert.account} · {alert.date}</div>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
                <span style={{ color: theme.subtext, fontSize: "12px" }}>Fraud Probability</span>
                <span style={{ color: alert.probability >= 80 ? "#f87171" : "#fb923c", fontSize: "13px", fontWeight: "700" }}>{alert.probability}%</span>
              </div>
              <ProbabilityBar value={alert.probability} />
            </div>
          ))}
        </div>

        <div style={{ flex: 1, background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", alignSelf: "flex-start" }}>
          <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "20px" }}>Alert Details</h3>
          {!selected ? (
            <p style={{ color: theme.subtext, fontSize: "14px" }}>Click an alert to view details</p>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              {[
                { label: "Alert ID", value: selected.id, color: "#38bdf8" },
                { label: "Account", value: selected.account },
                { label: "Fraud Type", value: selected.type },
                { label: "Date Reported", value: selected.date },
              ].map(({ label, value, color }) => (
                <div key={label} style={{ borderBottom: `1px solid ${theme.border}`, paddingBottom: "14px" }}>
                  <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "4px" }}>{label}</div>
                  <div style={{ color: color || theme.text, fontSize: "15px", fontWeight: "500" }}>{value}</div>
                </div>
              ))}
              <div style={{ borderBottom: `1px solid ${theme.border}`, paddingBottom: "14px" }}>
                <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "8px" }}>Current Status</div>
                <StatusBadge status={selected.status} />
              </div>
              <div>
                <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "10px" }}>Update Status</div>
                <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                  {["Open", "In Progress", "Resolved"].map((s) => (
                    <button key={s} onClick={() => updateStatus(selected.id, s)} style={{
                      padding: "10px", borderRadius: "8px", fontSize: "13px", cursor: "pointer", textAlign: "left",
                      border: selected.status === s ? "1px solid #38bdf8" : `1px solid ${theme.border}`,
                      background: selected.status === s ? "#1e3a5f" : theme.bg,
                      color: selected.status === s ? "#38bdf8" : theme.subtext,
                    }}>
                      {s === "Open" ? "🔴" : s === "In Progress" ? "🟠" : "🟢"} Mark as {s}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </PageLayout>
  );
}

export default AlertsManagement;