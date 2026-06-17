import { useTheme } from "../../context/ThemeContext";

const Card = ({ title, children, className = "", style = {} }) => {
  const theme = useTheme();
  return (
    <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s", ...style }}>
      {title && (
        <h3 style={{ color: theme.text, fontSize: "15px", fontWeight: "600", marginBottom: "16px", paddingBottom: "12px", borderBottom: `1px solid ${theme.border}` }}>
          {title}
        </h3>
      )}
      {children}
    </div>
  );
};

export default Card;