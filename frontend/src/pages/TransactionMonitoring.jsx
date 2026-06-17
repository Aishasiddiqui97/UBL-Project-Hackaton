import { useState, useEffect } from "react";
import PageLayout from "../components/layout/PageLayout";
import { recentTransactions } from "../data/mockdata";
import { exportToCSV } from "../utils/exportCSV";

function RiskBadge({ risk }) {
  const colors = { High: { bg: "#450a0a", color: "#f87171" }, Medium: { bg: "#431407", color: "#fb923c" }, Low: { bg: "#052e16", color: "#4ade80" } };
  const c = colors[risk] || colors.Low;
  return <span style={{ background: c.bg, color: c.color, padding: "3px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>{risk}</span>;
}

function StatusBadge({ status }) {
  const colors = { Flagged: { bg: "#450a0a", color: "#f87171" }, "Under Review": { bg: "#431407", color: "#fb923c" }, Clear: { bg: "#052e16", color: "#4ade80" } };
  const c = colors[status] || colors.Clear;
  return <span style={{ background: c.bg, color: c.color, padding: "3px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>{status}</span>;
}

function TransactionMonitoring() {
  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState("All");
  const [filterRisk, setFilterRisk] = useState("All");
  const [selected, setSelected] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [autoRefresh, setAutoRefresh] = useState(true);

  // Auto refresh every 30 seconds
  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(() => {
      setLastUpdated(new Date());
    }, 30000);
    return () => clearInterval(interval);
  }, [autoRefresh]);

  const filtered = recentTransactions.filter((tx) => {
    const matchSearch = tx.id.toLowerCase().includes(search.toLowerCase()) || tx.account.toLowerCase().includes(search.toLowerCase());
    const matchStatus = filterStatus === "All" || tx.status === filterStatus;
    const matchRisk = filterRisk === "All" || tx.risk === filterRisk;
    return matchSearch && matchStatus && matchRisk;
  });

  const inputStyle = {
    background: "#0f172a", border: "1px solid #334155", borderRadius: "8px",
    color: "white", padding: "10px 14px", fontSize: "14px", outline: "none"
  };

  return (
    <PageLayout title="Transaction Monitoring">

      {/* Stats Row */}
      <div style={{ display: "flex", gap: "16px", marginBottom: "24px" }}>
        {[
          { label: "Total", value: recentTransactions.length, color: "#38bdf8" },
          { label: "Flagged", value: recentTransactions.filter(t => t.status === "Flagged").length, color: "#f87171" },
          { label: "Under Review", value: recentTransactions.filter(t => t.status === "Under Review").length, color: "#fb923c" },
          { label: "Clear", value: recentTransactions.filter(t => t.status === "Clear").length, color: "#4ade80" },
        ].map(card => (
          <div key={card.label} style={{ flex: 1, background: "#1e293b", border: "1px solid #334155", borderRadius: "12px", padding: "16px 20px" }}>
            <div style={{ color: "#94a3b8", fontSize: "13px", marginBottom: "6px" }}>{card.label}</div>
            <div style={{ color: card.color, fontSize: "26px", fontWeight: "700" }}>{card.value}</div>
          </div>
        ))}
      </div>

      {/* Filters Row */}
      <div style={{ display: "flex", gap: "12px", marginBottom: "20px", flexWrap: "wrap", alignItems: "center" }}>
        <div style={{ position: "relative", flex: 1, minWidth: "200px" }}>
          <span style={{ position: "absolute", left: "10px", top: "50%", transform: "translateY(-50%)", color: "#64748b" }}>🔍</span>
          <input
            style={{ ...inputStyle, width: "100%", paddingLeft: "32px", boxSizing: "border-box" }}
            placeholder="Search by ID or Account..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <select style={inputStyle} value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
          <option value="All">All Status</option>
          <option value="Clear">Clear</option>
          <option value="Flagged">Flagged</option>
          <option value="Under Review">Under Review</option>
        </select>
        <select style={inputStyle} value={filterRisk} onChange={(e) => setFilterRisk(e.target.value)}>
          <option value="All">All Risk</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
        <button onClick={() => { setSearch(""); setFilterStatus("All"); setFilterRisk("All"); }}
          style={{ ...inputStyle, cursor: "pointer", color: "#f87171", borderColor: "#f87171" }}>
          Clear Filters
        </button>
        <button onClick={() => exportToCSV(filtered, "transactions.csv")}
          style={{ background: "#16a34a", border: "none", borderRadius: "8px", padding: "10px 16px", color: "white", fontSize: "13px", fontWeight: "600", cursor: "pointer" }}>
          ⬇️ Export CSV
        </button>
        <button onClick={() => { setAutoRefresh(p => !p); }}
          style={{ background: autoRefresh ? "#1e3a5f" : "#1e293b", border: `1px solid ${autoRefresh ? "#38bdf8" : "#334155"}`, borderRadius: "8px", padding: "10px 14px", color: autoRefresh ? "#38bdf8" : "#94a3b8", fontSize: "13px", cursor: "pointer" }}>
          {autoRefresh ? "🔄 Auto ON" : "⏸ Auto OFF"}
        </button>
      </div>

      {/* Last Updated */}
      <div style={{ color: "#475569", fontSize: "12px", marginBottom: "12px" }}>
        Last updated: {lastUpdated.toLocaleTimeString()}
      </div>

      <div style={{ display: "flex", gap: "20px" }}>
        {/* Table */}
        <div style={{ flex: 2, background: "#1e293b", border: "1px solid #334155", borderRadius: "12px", padding: "24px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
            <h3 style={{ color: "white", fontSize: "15px" }}>All Transactions</h3>
            <span style={{ color: "#94a3b8", fontSize: "13px" }}>{filtered.length} records</span>
          </div>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid #334155" }}>
                {["ID", "Account", "Amount", "Type", "Status", "Risk", "Date"].map(h => (
                  <th key={h} style={{ color: "#94a3b8", textAlign: "left", padding: "10px 12px", fontWeight: "500" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr><td colSpan={7} style={{ color: "#94a3b8", textAlign: "center", padding: "32px" }}>No transactions found</td></tr>
              ) : (
                filtered.map((tx) => (
                  <tr key={tx.id} onClick={() => setSelected(tx)}
                    style={{ borderBottom: "1px solid #0f172a", cursor: "pointer", background: selected?.id === tx.id ? "#0f172a" : "transparent" }}
                    onMouseEnter={e => { if (selected?.id !== tx.id) e.currentTarget.style.background = "#162032"; }}
                    onMouseLeave={e => { if (selected?.id !== tx.id) e.currentTarget.style.background = "transparent"; }}>
                    <td style={{ padding: "12px", color: "#38bdf8" }}>{tx.id}</td>
                    <td style={{ padding: "12px", color: "white" }}>{tx.account}</td>
                    <td style={{ padding: "12px", color: "white" }}>PKR {tx.amount.toLocaleString()}</td>
                    <td style={{ padding: "12px", color: "#94a3b8" }}>{tx.type}</td>
                    <td style={{ padding: "12px" }}><StatusBadge status={tx.status} /></td>
                    <td style={{ padding: "12px" }}><RiskBadge risk={tx.risk} /></td>
                    <td style={{ padding: "12px", color: "#94a3b8" }}>{tx.date}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Details Panel */}
        <div style={{ flex: 1, background: "#1e293b", border: "1px solid #334155", borderRadius: "12px", padding: "24px", alignSelf: "flex-start" }}>
          <h3 style={{ color: "white", fontSize: "15px", marginBottom: "20px" }}>Transaction Details</h3>
          {!selected ? (
            <p style={{ color: "#94a3b8", fontSize: "14px" }}>Click a transaction to view details</p>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              {[
                { label: "Transaction ID", value: selected.id, color: "#38bdf8" },
                { label: "Account", value: selected.account },
                { label: "Amount", value: `PKR ${selected.amount.toLocaleString()}` },
                { label: "Type", value: selected.type },
                { label: "Date", value: selected.date },
              ].map(({ label, value, color }) => (
                <div key={label} style={{ borderBottom: "1px solid #334155", paddingBottom: "12px" }}>
                  <div style={{ color: "#94a3b8", fontSize: "12px", marginBottom: "4px" }}>{label}</div>
                  <div style={{ color: color || "white", fontSize: "15px", fontWeight: "500" }}>{value}</div>
                </div>
              ))}
              <div style={{ borderBottom: "1px solid #334155", paddingBottom: "12px" }}>
                <div style={{ color: "#94a3b8", fontSize: "12px", marginBottom: "6px" }}>Status</div>
                <StatusBadge status={selected.status} />
              </div>
              <div>
                <div style={{ color: "#94a3b8", fontSize: "12px", marginBottom: "6px" }}>Risk Level</div>
                <RiskBadge risk={selected.risk} />
              </div>
              <button onClick={() => exportToCSV([selected], `${selected.id}.csv`)}
                style={{ background: "#16a34a", border: "none", borderRadius: "8px", padding: "10px", color: "white", fontSize: "13px", fontWeight: "600", cursor: "pointer", marginTop: "8px" }}>
                ⬇️ Export This Transaction
              </button>
            </div>
          )}
        </div>
      </div>
    </PageLayout>
  );
}

export default TransactionMonitoring;