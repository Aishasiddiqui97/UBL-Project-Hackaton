import { useState } from "react";
import PageLayout from "../components/layout/PageLayout";
import { exportToCSV } from "../utils/exportCSV";
import { recentTransactions, fraudAlerts, openCases } from "../data/mockdata";

const reports = [
  { id: "RPT001", name: "Monthly Fraud Summary", type: "Summary", generatedDate: "2026-06-16", author: "System Admin", cases: 4, fileSize: "2.4 MB", status: "Ready" },
  { id: "RPT002", name: "Case Activity Report", type: "Activity", generatedDate: "2026-06-15", author: "John Doe", cases: 4, fileSize: "1.8 MB", status: "Ready" },
  { id: "RPT003", name: "Risk Assessment Q2 2026", type: "Risk Analysis", generatedDate: "2026-06-14", author: "Sarah Smith", cases: 12, fileSize: "5.2 MB", status: "Ready" },
  { id: "RPT004", name: "Transaction Pattern Analysis", type: "Analysis", generatedDate: "2026-06-13", author: "Mike Johnson", cases: 8, fileSize: "3.1 MB", status: "Ready" },
  { id: "RPT005", name: "Daily Alert Summary", type: "Summary", generatedDate: "2026-06-16", author: "System Admin", cases: 2, fileSize: "0.9 MB", status: "Ready" },
  { id: "RPT006", name: "Compliance Audit Report", type: "Audit", generatedDate: "2026-06-10", author: "Lisa Brown", cases: 20, fileSize: "7.5 MB", status: "Ready" },
];

const typeColors = {
  Summary: { bg: "#1e3a5f", color: "#93c5fd" },
  Activity: { bg: "#3b1f5e", color: "#c4b5fd" },
  "Risk Analysis": { bg: "#450a0a", color: "#f87171" },
  Analysis: { bg: "#431407", color: "#fb923c" },
  Audit: { bg: "#052e16", color: "#4ade80" },
};

const exportMap = {
  RPT001: { data: fraudAlerts, filename: "fraud_summary.csv" },
  RPT002: { data: openCases, filename: "case_activity.csv" },
  RPT003: { data: fraudAlerts, filename: "risk_assessment.csv" },
  RPT004: { data: recentTransactions, filename: "transaction_patterns.csv" },
  RPT005: { data: fraudAlerts, filename: "daily_alerts.csv" },
  RPT006: { data: recentTransactions, filename: "compliance_audit.csv" },
};

function Reports() {
  const [selectedReport, setSelectedReport] = useState(null);
  const [filterType, setFilterType] = useState("All");
  const [downloaded, setDownloaded] = useState(null);

  const reportTypes = ["All", "Summary", "Activity", "Risk Analysis", "Analysis", "Audit"];
  const filtered = filterType === "All" ? reports : reports.filter(r => r.type === filterType);

  const handleDownload = (report) => {
    const exp = exportMap[report.id];
    if (exp) {
      exportToCSV(exp.data, exp.filename);
      setDownloaded(report.id);
      setTimeout(() => setDownloaded(null), 2000);
    }
  };

  return (
    <PageLayout title="Reports & Analytics">

      {/* Stats */}
      <div style={{ display: "flex", gap: "20px", marginBottom: "32px" }}>
        {[
          { label: "Total Reports", value: reports.length, color: "#38bdf8", icon: "📄" },
          { label: "This Month", value: 3, color: "#4ade80", icon: "📅" },
          { label: "Pending", value: 0, color: "#fb923c", icon: "⏳" },
          { label: "Archived", value: 2, color: "#c4b5fd", icon: "📦" },
        ].map(({ label, value, color, icon }) => (
          <div key={label} style={{ flex: 1, background: "#1e293b", border: "1px solid #334155", borderRadius: "12px", padding: "24px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
              <span style={{ color: "#94a3b8", fontSize: "14px" }}>{label}</span>
              <span style={{ fontSize: "22px" }}>{icon}</span>
            </div>
            <div style={{ color, fontSize: "32px", fontWeight: "700" }}>{value}</div>
          </div>
        ))}
      </div>

      {/* Filters + Generate */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
        <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
          {reportTypes.map(type => (
            <button key={type} onClick={() => setFilterType(type)}
              style={{ padding: "6px 16px", borderRadius: "6px", fontSize: "13px", cursor: "pointer", background: filterType === type ? "#2563eb" : "#1e293b", border: filterType === type ? "1px solid #3b82f6" : "1px solid #334155", color: filterType === type ? "white" : "#94a3b8" }}>
              {type}
            </button>
          ))}
        </div>
        <div style={{ display: "flex", gap: "10px" }}>
          <button onClick={() => exportToCSV(recentTransactions, "all_transactions.csv")}
            style={{ background: "#16a34a", border: "none", borderRadius: "8px", padding: "8px 18px", color: "white", fontSize: "14px", cursor: "pointer", fontWeight: "600" }}>
            ⬇️ Export All CSV
          </button>
          <button style={{ background: "#2563eb", border: "none", borderRadius: "8px", padding: "8px 18px", color: "white", fontSize: "14px", cursor: "pointer", fontWeight: "600" }}>
            + Generate Report
          </button>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: "20px" }}>

        {/* Table */}
        <div style={{ background: "#1e293b", border: "1px solid #334155", borderRadius: "12px", overflow: "hidden" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid #334155", background: "#0f172a" }}>
                {["Report Name", "Type", "Date", "Author", "Actions"].map(h => (
                  <th key={h} style={{ color: "#94a3b8", textAlign: "left", padding: "12px 16px", fontWeight: "500" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.map(report => (
                <tr key={report.id} onClick={() => setSelectedReport(report)}
                  style={{ borderBottom: "1px solid #1e293b", cursor: "pointer", background: selectedReport?.id === report.id ? "#0f2040" : "transparent" }}
                  onMouseEnter={e => { if (selectedReport?.id !== report.id) e.currentTarget.style.background = "#162032"; }}
                  onMouseLeave={e => { if (selectedReport?.id !== report.id) e.currentTarget.style.background = "transparent"; }}>
                  <td style={{ padding: "14px 16px" }}>
                    <div style={{ color: "white", fontWeight: "600" }}>{report.name}</div>
                    <div style={{ color: "#64748b", fontSize: "12px" }}>{report.id}</div>
                  </td>
                  <td style={{ padding: "14px 16px" }}>
                    <span style={{ background: typeColors[report.type]?.bg, color: typeColors[report.type]?.color, padding: "3px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>{report.type}</span>
                  </td>
                  <td style={{ padding: "14px 16px", color: "#94a3b8" }}>{report.generatedDate}</td>
                  <td style={{ padding: "14px 16px", color: "#94a3b8" }}>{report.author}</td>
                  <td style={{ padding: "14px 16px" }}>
                    <div style={{ display: "flex", gap: "8px" }}>
                      <button onClick={e => { e.stopPropagation(); setSelectedReport(report); }}
                        style={{ background: "none", border: "none", cursor: "pointer", fontSize: "16px" }}>👁️</button>
                      <button onClick={e => { e.stopPropagation(); handleDownload(report); }}
                        style={{ background: "none", border: "none", cursor: "pointer", fontSize: "16px" }}
                        title="Download CSV">
                        {downloaded === report.id ? "✅" : "⬇️"}
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Details Panel */}
        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          <div style={{ background: "#1e293b", border: "1px solid #334155", borderRadius: "12px", padding: "24px" }}>
            <h3 style={{ color: "white", fontSize: "15px", marginBottom: "16px" }}>Report Details</h3>
            {!selectedReport ? (
              <p style={{ color: "#94a3b8", fontSize: "14px" }}>Select a report to view details</p>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", gap: "14px", fontSize: "14px" }}>
                {[
                  { label: "Report ID", value: selectedReport.id, color: "#38bdf8" },
                  { label: "Author", value: selectedReport.author },
                  { label: "File Size", value: selectedReport.fileSize },
                  { label: "Cases Included", value: selectedReport.cases },
                  { label: "Status", value: selectedReport.status, color: "#4ade80" },
                ].map(({ label, value, color }) => (
                  <div key={label} style={{ borderBottom: "1px solid #334155", paddingBottom: "10px" }}>
                    <div style={{ color: "#94a3b8", fontSize: "12px", marginBottom: "4px" }}>{label}</div>
                    <div style={{ color: color || "white", fontWeight: "600" }}>{value}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {selectedReport && (
            <div style={{ background: "#1e293b", border: "1px solid #334155", borderRadius: "12px", padding: "24px" }}>
              <h3 style={{ color: "white", fontSize: "15px", marginBottom: "16px" }}>Actions</h3>
              <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
                <button onClick={() => handleDownload(selectedReport)}
                  style={{ background: "#16a34a", border: "none", borderRadius: "8px", padding: "10px", color: "white", fontSize: "14px", cursor: "pointer" }}>
                  {downloaded === selectedReport.id ? "✅ Downloaded!" : "⬇️ Download CSV"}
                </button>
                <button style={{ background: "#2563eb", border: "none", borderRadius: "8px", padding: "10px", color: "white", fontSize: "14px", cursor: "pointer" }}>
                  👁️ View Report
                </button>
                <button style={{ background: "#334155", border: "none", borderRadius: "8px", padding: "10px", color: "white", fontSize: "14px", cursor: "pointer" }}>
                  📤 Share Report
                </button>
                <button style={{ background: "#334155", border: "none", borderRadius: "8px", padding: "10px", color: "white", fontSize: "14px", cursor: "pointer" }}>
                  📦 Archive
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </PageLayout>
  );
}

export default Reports;