import { useTheme } from "../../context/ThemeContext";

const Badge = ({ text, type }) => {
  const { isDark } = useTheme();
  const styles = {
    High:           { bg: "#450a0a", color: "#f87171" },
    Critical:       { bg: "#450a0a", color: "#f87171" },
    Blocked:        { bg: "#450a0a", color: "#f87171" },
    Suspended:      { bg: "#450a0a", color: "#f87171" },
    Flagged:        { bg: "#431407", color: "#fb923c" },
    Medium:         { bg: "#431407", color: "#fb923c" },
    "Under Review": { bg: "#431407", color: "#fb923c" },
    Low:            { bg: "#052e16", color: "#4ade80" },
    Clear:          { bg: "#052e16", color: "#4ade80" },
    Monitored:      { bg: "#1e3a5f", color: "#93c5fd" },
    "In Progress":  { bg: "#1e3a5f", color: "#93c5fd" },
    Open:           { bg: "#3b1f5e", color: "#c4b5fd" },
  };
  const s = styles[text] || { bg: "#1e293b", color: "#94a3b8" };
  return (
    <span style={{ background: s.bg, color: s.color, padding: "3px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "600", display: "inline-block" }}>
      {text}
    </span>
  );
};

export default Badge;