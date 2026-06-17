import PageLayout from "../components/layout/PageLayout";
import { useTheme } from "../context/ThemeContext";
import { stats, recentTransactions, weeklyTransactions, riskDistribution, monthlyTrends } from "../data/mockdata";
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid } from "recharts";
import {
  ArrowLeftRight, ShieldAlert, TriangleAlert, FolderOpen,
  TrendingUp, TrendingDown, MoveUpRight
} from "lucide-react";

const COLORS = ["#22c55e", "#f59e0b", "#ef4444"];

const statCards = [
  {
    label: "Total Transactions",
    value: stats.totalTransactions.toLocaleString(),
    icon: ArrowLeftRight,
    color: "#38bdf8",
    borderColor: "#38bdf8",
    trend: "+8.2%",
    trendUp: true,
    sub: "vs last week",
  },
  {
    label: "Fraud Alerts",
    value: stats.fraudAlerts,
    icon: ShieldAlert,
    color: "#f87171",
    borderColor: "#f87171",
    trend: "+5.9%",
    trendUp: false,
    sub: "vs last week",
  },
  {
    label: "High Risk Accounts",
    value: stats.highRiskAccounts,
    icon: TriangleAlert,
    color: "#fb923c",
    borderColor: "#fb923c",
    trend: "-2.1%",
    trendUp: true,
    sub: "vs last week",
  },
  {
    label: "Open Cases",
    value: stats.openCases,
    icon: FolderOpen,
    color: "#a78bfa",
    borderColor: "#a78bfa",
    trend: "+3 new",
    trendUp: false,
    sub: "since yesterday",
  },
];

function StatCard({ label, value, icon: Icon, color, borderColor, trend, trendUp, sub, theme }) {
  return (
    <div style={{
      background: theme.surface,
      border: `1px solid ${theme.border}`,
      borderLeft: `4px solid ${borderColor}`,
      borderRadius: "12px",
      padding: "20px 24px",
      flex: 1,
      transition: "all 0.2s",
      cursor: "default",
    }}
      onMouseEnter={e => e.currentTarget.style.transform = "translateY(-2px)"}
      onMouseLeave={e => e.currentTarget.style.transform = "translateY(0)"}
    >
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: "14px" }}>
        <span style={{ color: theme.subtext, fontSize: "13px", fontWeight: "500", letterSpacing: "0.02em" }}>{label}</span>
        <div style={{ background: `${color}18`, borderRadius: "8px", padding: "6px", display: "flex", alignItems: "center" }}>
          <Icon size={16} color={color} />
        </div>
      </div>
      <div style={{ color, fontSize: "30px", fontWeight: "700", marginBottom: "10px", letterSpacing: "-0.5px" }}>
        {value}
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
        {trendUp
          ? <TrendingUp size={13} color="#22c55e" />
          : <TrendingDown size={13} color="#f87171" />
        }
        <span style={{ fontSize: "12px", color: trendUp ? "#22c55e" : "#f87171", fontWeight: "600" }}>{trend}</span>
        <span style={{ fontSize: "12px", color: theme.subtext }}>{sub}</span>
      </div>
    </div>
  );
}

function RiskBadge({ risk }) {
  const colors = {
    High: { bg: "#450a0a", color: "#f87171" },
    Medium: { bg: "#431407", color: "#fb923c" },
    Low: { bg: "#052e16", color: "#4ade80" },
  };
  const c = colors[risk] || colors.Low;
  return (
    <span style={{ background: c.bg, color: c.color, padding: "3px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>
      {risk}
    </span>
  );
}

function StatusBadge({ status }) {
  const colors = {
    Flagged: { bg: "#450a0a", color: "#f87171" },
    "Under Review": { bg: "#431407", color: "#fb923c" },
    Clear: { bg: "#052e16", color: "#4ade80" },
  };
  const c = colors[status] || colors.Clear;
  return (
    <span style={{ background: c.bg, color: c.color, padding: "3px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>
      {status}
    </span>
  );
}

function SectionHeader({ title, theme, action }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "20px" }}>
      <h3 style={{ color: theme.text, fontSize: "14px", fontWeight: "600", margin: 0, letterSpacing: "0.01em" }}>{title}</h3>
      {action && (
        <button style={{
          background: "none", border: "none", color: "#38bdf8", fontSize: "12px",
          cursor: "pointer", display: "flex", alignItems: "center", gap: "4px", padding: 0,
        }}>
          {action} <MoveUpRight size={12} />
        </button>
      )}
    </div>
  );
}

function Dashboard() {
  const theme = useTheme();

  const card = {
    background: theme.surface,
    border: `1px solid ${theme.border}`,
    borderRadius: "12px",
    padding: "24px",
    transition: "all 0.2s",
  };

  return (
    <PageLayout title="Dashboard">

      {/* Stat Cards */}
      <div style={{ display: "flex", gap: "16px", marginBottom: "24px" }}>
        {statCards.map((s) => (
          <StatCard key={s.label} {...s} theme={theme} />
        ))}
      </div>

      {/* Weekly + Risk Distribution */}
      <div style={{ display: "flex", gap: "16px", marginBottom: "16px" }}>
        <div style={{ ...card, flex: 2 }}>
          <SectionHeader title="Weekly Transactions" theme={theme} action="View all" />
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={weeklyTransactions}>
              <XAxis dataKey="day" stroke={theme.subtext} fontSize={12} axisLine={false} tickLine={false} />
              <YAxis stroke={theme.subtext} fontSize={12} axisLine={false} tickLine={false} />
              <Tooltip
                contentStyle={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "8px", color: theme.text, fontSize: "12px" }}
                cursor={{ fill: theme.border + "40" }}
              />
              <Legend wrapperStyle={{ color: theme.subtext, fontSize: "12px" }} />
              <Bar dataKey="transactions" fill="#38bdf8" radius={[4, 4, 0, 0]} name="Transactions" />
              <Bar dataKey="flagged" fill="#f87171" radius={[4, 4, 0, 0]} name="Flagged" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div style={{ ...card, flex: 1 }}>
          <SectionHeader title="Risk Distribution" theme={theme} />
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie
                data={riskDistribution}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                innerRadius={40}
                paddingAngle={3}
                label={({ value }) => `${value}%`}
              >
                {riskDistribution.map((_, i) => <Cell key={i} fill={COLORS[i]} />)}
              </Pie>
              <Tooltip contentStyle={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "8px", color: theme.text, fontSize: "12px" }} />
              <Legend wrapperStyle={{ color: theme.subtext, fontSize: "12px" }} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Monthly Trends */}
      <div style={{ ...card, marginBottom: "16px" }}>
        <SectionHeader title="Monthly Trends — 2026" theme={theme} />
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={monthlyTrends}>
            <CartesianGrid strokeDasharray="3 3" stroke={theme.border} vertical={false} />
            <XAxis dataKey="month" stroke={theme.subtext} fontSize={12} axisLine={false} tickLine={false} />
            <YAxis stroke={theme.subtext} fontSize={12} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "8px", color: theme.text, fontSize: "12px" }} />
            <Legend wrapperStyle={{ color: theme.subtext, fontSize: "12px" }} />
            <Line type="monotone" dataKey="transactions" stroke="#38bdf8" strokeWidth={2.5} dot={{ fill: "#38bdf8", r: 4 }} activeDot={{ r: 6 }} name="Transactions" />
            <Line type="monotone" dataKey="fraud" stroke="#f87171" strokeWidth={2.5} dot={{ fill: "#f87171", r: 4 }} activeDot={{ r: 6 }} name="Fraud Cases" />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Recent Transactions */}
      <div style={card}>
        <SectionHeader title="Recent Transactions" theme={theme} action="View all" />
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "13px" }}>
          <thead>
            <tr style={{ borderBottom: `1px solid ${theme.border}` }}>
              {["ID", "Account", "Amount", "Type", "Status", "Risk", "Date"].map(h => (
                <th key={h} style={{
                  color: theme.subtext, textAlign: "left", padding: "10px 12px",
                  fontWeight: "500", fontSize: "12px", textTransform: "uppercase", letterSpacing: "0.05em",
                }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {recentTransactions.slice(0, 6).map((tx, i) => (
              <tr
                key={tx.id}
                style={{ borderBottom: `1px solid ${theme.border}`, transition: "background 0.15s" }}
                onMouseEnter={e => e.currentTarget.style.background = theme.border + "30"}
                onMouseLeave={e => e.currentTarget.style.background = "transparent"}
              >
                <td style={{ padding: "13px 12px", color: "#38bdf8", fontWeight: "600", fontFamily: "monospace" }}>{tx.id}</td>
                <td style={{ padding: "13px 12px", color: theme.text }}>{tx.account}</td>
                <td style={{ padding: "13px 12px", color: theme.text, fontWeight: "500" }}>PKR {tx.amount.toLocaleString()}</td>
                <td style={{ padding: "13px 12px", color: theme.subtext }}>{tx.type}</td>
                <td style={{ padding: "13px 12px" }}><StatusBadge status={tx.status} /></td>
                <td style={{ padding: "13px 12px" }}><RiskBadge risk={tx.risk} /></td>
                <td style={{ padding: "13px 12px", color: theme.subtext }}>{tx.date}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </PageLayout>
  );
}

export default Dashboard;