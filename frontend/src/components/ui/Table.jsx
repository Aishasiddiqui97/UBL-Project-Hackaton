import { useTheme } from "../../context/ThemeContext";

const Table = ({ columns, data }) => {
  const theme = useTheme();
  return (
    <div style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
        <thead>
          <tr style={{ borderBottom: `1px solid ${theme.border}` }}>
            {columns.map((col, i) => (
              <th key={i} style={{ color: theme.subtext, textAlign: "left", padding: "10px 12px", fontWeight: "500", whiteSpace: "nowrap" }}>
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.length === 0 ? (
            <tr><td colSpan={columns.length} style={{ color: theme.subtext, textAlign: "center", padding: "32px" }}>No data found</td></tr>
          ) : data.map((row, ri) => (
            <tr key={ri} style={{ borderBottom: `1px solid ${theme.border}` }}
              onMouseEnter={e => e.currentTarget.style.background = theme.isDark ? "#162032" : "#f8fafc"}
              onMouseLeave={e => e.currentTarget.style.background = "transparent"}>
              {columns.map((col, ci) => (
                <td key={ci} style={{ padding: "12px", color: theme.text }}>
                  {col.render ? col.render(row) : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;