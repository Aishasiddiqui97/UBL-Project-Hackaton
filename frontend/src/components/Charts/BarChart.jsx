import { useTheme } from "../../context/ThemeContext";
import { BarChart as ReBarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid } from "recharts";

const BarChart = ({ data, bars = [], title, height = 220 }) => {
  const theme = useTheme();
  return (
    <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
      {title && <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "20px" }}>{title}</h3>}
      <ResponsiveContainer width="100%" height={height}>
        <ReBarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke={theme.border} />
          <XAxis dataKey="name" stroke={theme.subtext} fontSize={12} />
          <YAxis stroke={theme.subtext} fontSize={12} />
          <Tooltip contentStyle={{ background: theme.surface, border: `1px solid ${theme.border}`, color: theme.text }} />
          <Legend wrapperStyle={{ color: theme.subtext, fontSize: "13px" }} />
          {bars.map((bar, i) => (
            <Bar key={i} dataKey={bar.key} fill={bar.color || "#38bdf8"} radius={[4,4,0,0]} name={bar.label || bar.key} />
          ))}
        </ReBarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BarChart;