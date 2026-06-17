import { useTheme } from "../../context/ThemeContext";
import { PieChart as RePieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from "recharts";

const COLORS = ["#22c55e", "#f59e0b", "#ef4444", "#38bdf8", "#a78bfa", "#fb923c"];

const PieChart = ({ data, title, height = 220 }) => {
  const theme = useTheme();
  return (
    <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
      {title && <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "20px" }}>{title}</h3>}
      <ResponsiveContainer width="100%" height={height}>
        <RePieChart>
          <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label={({ value }) => `${value}%`}>
            {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
          </Pie>
          <Tooltip contentStyle={{ background: theme.surface, border: `1px solid ${theme.border}`, color: theme.text }} />
          <Legend wrapperStyle={{ color: theme.subtext, fontSize: "13px" }} />
        </RePieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PieChart;