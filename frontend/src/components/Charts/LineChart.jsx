import { useTheme } from "../../context/ThemeContext";
import { LineChart as ReLineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid } from "recharts";

const LineChart = ({ data, lines = [], title, height = 220 }) => {
  const theme = useTheme();
  return (
    <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
      {title && <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "20px" }}>{title}</h3>}
      <ResponsiveContainer width="100%" height={height}>
        <ReLineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke={theme.border} />
          <XAxis dataKey="name" stroke={theme.subtext} fontSize={12} />
          <YAxis stroke={theme.subtext} fontSize={12} />
          <Tooltip contentStyle={{ background: theme.surface, border: `1px solid ${theme.border}`, color: theme.text }} />
          <Legend wrapperStyle={{ color: theme.subtext, fontSize: "13px" }} />
          {lines.map((line, i) => (
            <Line key={i} type="monotone" dataKey={line.key} stroke={line.color || "#38bdf8"} strokeWidth={2} dot={{ fill: line.color || "#38bdf8" }} name={line.label || line.key} />
          ))}
        </ReLineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default LineChart;