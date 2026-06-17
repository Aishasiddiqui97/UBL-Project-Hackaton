import PageLayout from "../components/layout/PageLayout";
import { highRiskAccounts, riskDistribution } from "../data/mockdata";
import { useTheme } from "../context/ThemeContext";
import { RadialBarChart, RadialBar, PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";

const COLORS = ["#22c55e", "#f59e0b", "#ef4444"];

function RiskLevelBadge({ score }) {
  if (score >= 80) return <span style={{ background: "#450a0a", color: "#f87171", padding: "4px 12px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>High Risk</span>;
  if (score >= 60) return <span style={{ background: "#431407", color: "#fb923c", padding: "4px 12px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>Medium Risk</span>;
  return <span style={{ background: "#052e16", color: "#4ade80", padding: "4px 12px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>Low Risk</span>;
}

function ScoreBar({ score }) {
  const color = score >= 80 ? "#ef4444" : score >= 60 ? "#f59e0b" : "#22c55e";
  return (
    <div style={{ width: "100%", background: "#0f172a", borderRadius: "20px", height: "8px", marginTop: "6px" }}>
      <div style={{ width: `${score}%`, background: color, borderRadius: "20px", height: "8px", transition: "width 0.4s" }} />
    </div>
  );
}

function RiskScoring() {
  const theme = useTheme();
  const avgScore = Math.round(highRiskAccounts.reduce((a, b) => a + b.riskScore, 0) / highRiskAccounts.length);
  const radialData = [{ name: "Risk Score", value: avgScore, fill: avgScore >= 80 ? "#ef4444" : avgScore >= 60 ? "#f59e0b" : "#22c55e" }];

  return (
    <PageLayout title="Risk Scoring">

      {/* Top Row */}
      <div style={{ display: "flex", gap: "20px", marginBottom: "28px", flexWrap: "wrap" }}>

        {/* Avg Risk Score Gauge */}
        <div style={{ flex: "1 1 200px", background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", textAlign: "center", transition: "all 0.3s" }}>
          <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "8px" }}>Average Risk Score</h3>
          <p style={{ color: theme.subtext, fontSize: "13px", marginBottom: "16px" }}>Across all high-risk accounts</p>
          <ResponsiveContainer width="100%" height={200}>
            <RadialBarChart cx="50%" cy="50%" innerRadius="60%" outerRadius="90%" data={radialData} startAngle={180} endAngle={0}>
              <RadialBar dataKey="value" cornerRadius={10} background={{ fill: theme.bg }} />
            </RadialBarChart>
          </ResponsiveContainer>
          <div style={{ color: avgScore >= 80 ? "#f87171" : avgScore >= 60 ? "#fb923c" : "#4ade80", fontSize: "40px", fontWeight: "700", marginTop: "-40px" }}>
            {avgScore}
          </div>
          <div style={{ marginTop: "8px" }}>
            <RiskLevelBadge score={avgScore} />
          </div>
        </div>

        {/* Risk Distribution Pie */}
        <div style={{ flex: "1 1 200px", background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
          <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "8px" }}>Risk Distribution</h3>
          <p style={{ color: theme.subtext, fontSize: "13px", marginBottom: "8px" }}>All accounts by risk level</p>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={riskDistribution} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label={({ value }) => `${value}%`}>
                {riskDistribution.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
              </Pie>
              <Tooltip contentStyle={{ background: theme.surface, border: `1px solid ${theme.border}`, color: theme.text }} />
              <Legend wrapperStyle={{ color: theme.subtext, fontSize: "13px" }} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Risk Level Indicators */}
        <div style={{ flex: "1 1 200px", background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
          <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "20px" }}>Risk Level Indicators</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
            {[
              { label: "Low Risk", range: "Score 0 – 59", color: "#4ade80", bg: "#052e16", count: "62% of accounts" },
              { label: "Medium Risk", range: "Score 60 – 79", color: "#fb923c", bg: "#431407", count: "25% of accounts" },
              { label: "High Risk", range: "Score 80 – 100", color: "#f87171", bg: "#450a0a", count: "13% of accounts" },
            ].map((item) => (
              <div key={item.label} style={{ background: item.bg, borderRadius: "10px", padding: "14px 16px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div>
                    <div style={{ color: item.color, fontWeight: "600", fontSize: "14px" }}>{item.label}</div>
                    <div style={{ color: theme.subtext, fontSize: "12px", marginTop: "2px" }}>{item.range}</div>
                  </div>
                  <div style={{ color: item.color, fontSize: "13px", fontWeight: "500" }}>{item.count}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* High Risk Accounts Table */}
      <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s", overflowX: "auto" }}>
        <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "20px" }}>High Risk Accounts</h3>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
          <thead>
            <tr style={{ borderBottom: `1px solid ${theme.border}` }}>
              {["Account ID", "Name", "Risk Score", "Score Bar", "Transactions", "Flagged", "Risk Level"].map((h) => (
                <th key={h} style={{ color: theme.subtext, textAlign: "left", padding: "10px 12px", fontWeight: "500" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {highRiskAccounts.map((acc) => (
              <tr key={acc.id} style={{ borderBottom: `1px solid ${theme.border}` }}>
                <td style={{ padding: "14px 12px", color: "#38bdf8" }}>{acc.id}</td>
                <td style={{ padding: "14px 12px", color: theme.text }}>{acc.name}</td>
                <td style={{ padding: "14px 12px", color: acc.riskScore >= 80 ? "#f87171" : "#fb923c", fontWeight: "700", fontSize: "16px" }}>{acc.riskScore}</td>
                <td style={{ padding: "14px 12px", minWidth: "140px" }}><ScoreBar score={acc.riskScore} /></td>
                <td style={{ padding: "14px 12px", color: theme.text }}>{acc.transactions}</td>
                <td style={{ padding: "14px 12px", color: "#f87171", fontWeight: "600" }}>{acc.flagged}</td>
                <td style={{ padding: "14px 12px" }}><RiskLevelBadge score={acc.riskScore} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </PageLayout>
  );
}

export default RiskScoring;