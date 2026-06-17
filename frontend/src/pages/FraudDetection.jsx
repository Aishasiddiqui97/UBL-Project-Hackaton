import { useState } from "react";
import PageLayout from "../components/layout/PageLayout";
import { fraudAlerts, recentTransactions } from "../data/mockdata";
import { useTheme } from "../context/ThemeContext";

function ProbabilityBar({ value }) {
  const color = value >= 80 ? "#ef4444" : value >= 60 ? "#f59e0b" : "#22c55e";
  return (
    <div style={{ width: "100%", background: "#0f172a", borderRadius: "20px", height: "8px", marginTop: "6px" }}>
      <div style={{ width: `${value}%`, background: color, borderRadius: "20px", height: "8px", transition: "width 0.4s" }} />
    </div>
  );
}

function StatusBadge({ status }) {
  const colors = { Open: { bg: "#450a0a", color: "#f87171" }, "In Progress": { bg: "#431407", color: "#fb923c" }, Resolved: { bg: "#052e16", color: "#4ade80" } };
  const c = colors[status] || colors.Open;
  return <span style={{ background: c.bg, color: c.color, padding: "3px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>{status}</span>;
}

function FraudDetection() {
  const [selected, setSelected] = useState(null);
  const theme = useTheme();
  const suspiciousTx = recentTransactions.filter((tx) => tx.risk === "High" || tx.status === "Flagged");

  return (
    <PageLayout title="Fraud Detection">
      <div style={{ display: "flex", gap: "16px", marginBottom: "28px", flexWrap: "wrap" }}>
        {[
          { label: "Total Fraud Alerts", value: fraudAlerts.length, color: "#f87171" },
          { label: "Open Alerts", value: fraudAlerts.filter(a => a.status === "Open").length, color: "#fb923c" },
          { label: "In Progress", value: fraudAlerts.filter(a => a.status === "In Progress").length, color: "#fbbf24" },
          { label: "Resolved", value: fraudAlerts.filter(a => a.status === "Resolved").length, color: "#4ade80" },
        ].map((card) => (
          <div key={card.label} style={{ flex: "1 1 120px", background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "20px", transition: "all 0.3s" }}>
            <div style={{ color: theme.subtext, fontSize: "13px", marginBottom: "8px" }}>{card.label}</div>
            <div style={{ color: card.color, fontSize: "28px", fontWeight: "700" }}>{card.value}</div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
        {/* Alerts List */}
        <div style={{ flex: "1 1 300px", background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
          <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "20px" }}>Fraud Alerts</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
            {fraudAlerts.map((alert) => (
              <div key={alert.id} onClick={() => setSelected(alert)}
                style={{ background: theme.bg, border: selected?.id === alert.id ? "1px solid #38bdf8" : `1px solid ${theme.border}`, borderRadius: "10px", padding: "16px", cursor: "pointer", transition: "all 0.2s" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
                  <span style={{ color: "#38bdf8", fontSize: "13px", fontWeight: "600" }}>{alert.id}</span>
                  <StatusBadge status={alert.status} />
                </div>
                <div style={{ color: theme.text, fontSize: "14px", marginBottom: "4px" }}>{alert.type}</div>
                <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "10px" }}>{alert.account} · {alert.date}</div>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "4px" }}>
                  <span style={{ color: theme.subtext, fontSize: "12px" }}>Fraud Probability</span>
                  <span style={{ color: alert.probability >= 80 ? "#f87171" : alert.probability >= 60 ? "#fb923c" : "#4ade80", fontSize: "13px", fontWeight: "700" }}>{alert.probability}%</span>
                </div>
                <ProbabilityBar value={alert.probability} />
              </div>
            ))}
          </div>
        </div>

        <div style={{ flex: "1 1 300px", display: "flex", flexDirection: "column", gap: "20px" }}>
          {/* Alert Details */}
          <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
            <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "16px" }}>Alert Details</h3>
            {!selected ? <p style={{ color: theme.subtext, fontSize: "14px" }}>Click an alert to view details</p> : (
              <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
                {[{ label: "Alert ID", value: selected.id, color: "#38bdf8" }, { label: "Account", value: selected.account }, { label: "Fraud Type", value: selected.type }, { label: "Date", value: selected.date }].map(({ label, value, color }) => (
                  <div key={label} style={{ borderBottom: `1px solid ${theme.border}`, paddingBottom: "12px" }}>
                    <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "4px" }}>{label}</div>
                    <div style={{ color: color || theme.text, fontSize: "15px", fontWeight: "500" }}>{value}</div>
                  </div>
                ))}
                <div style={{ borderBottom: `1px solid ${theme.border}`, paddingBottom: "12px" }}>
                  <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "6px" }}>Status</div>
                  <StatusBadge status={selected.status} />
                </div>
                <div>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                    <span style={{ color: theme.subtext, fontSize: "12px" }}>Fraud Probability</span>
                    <span style={{ color: selected.probability >= 80 ? "#f87171" : "#fb923c", fontWeight: "700" }}>{selected.probability}%</span>
                  </div>
                  <ProbabilityBar value={selected.probability} />
                </div>
              </div>
            )}
          </div>

          {/* Suspicious Transactions */}
          <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
            <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "16px" }}>Suspicious Transactions</h3>
            <div style={{ overflowX: "auto" }}>
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "13px" }}>
                <thead>
                  <tr style={{ borderBottom: `1px solid ${theme.border}` }}>
                    {["ID", "Account", "Amount", "Type"].map((h) => (
                      <th key={h} style={{ color: theme.subtext, textAlign: "left", padding: "8px 10px", fontWeight: "500" }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {suspiciousTx.map((tx) => (
                    <tr key={tx.id} style={{ borderBottom: `1px solid ${theme.border}` }}>
                      <td style={{ padding: "10px", color: "#f87171" }}>{tx.id}</td>
                      <td style={{ padding: "10px", color: theme.text }}>{tx.account}</td>
                      <td style={{ padding: "10px", color: theme.text }}>PKR {tx.amount.toLocaleString()}</td>
                      <td style={{ padding: "10px", color: theme.subtext }}>{tx.type}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </PageLayout>
  );
}

export default FraudDetection;