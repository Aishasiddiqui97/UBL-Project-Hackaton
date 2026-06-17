import { NavLink, useNavigate } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";
import {
  LayoutDashboard, ArrowLeftRight, ShieldAlert,
  Target, Bell, FolderOpen, FileText, Settings, LogOut, Shield,
} from "lucide-react";

const navItems = [
  { path: "/dashboard",    label: "Dashboard",          icon: LayoutDashboard },
  { path: "/transactions", label: "Transactions",        icon: ArrowLeftRight },
  { path: "/fraud-detection", label: "Fraud Detection", icon: ShieldAlert },
  { path: "/risk-scoring", label: "Risk Scoring",        icon: Target },
  { path: "/alerts",       label: "Alerts",              icon: Bell },
  { path: "/cases",        label: "Case Management",     icon: FolderOpen },
  { path: "/reports",      label: "Reports",             icon: FileText },
  { path: "/settings",     label: "Settings",            icon: Settings },
];

const Sidebar = ({ onClose }) => {
  const navigate = useNavigate();
  const { navBg, surface, border, text, subtext, accent, isDark } = useTheme();

  const handleLogout = () => {
    localStorage.removeItem("isAuthenticated");
    navigate("/login");
  };

  const handleNav = () => {
    if (onClose) onClose();
  };

  return (
    <div style={{
      width: "220px",
      minHeight: "100vh",
      background: navBg,
      display: "flex",
      flexDirection: "column",
      borderRight: `1px solid ${border}`,
      position: "sticky",
      top: 0,
      height: "100vh",
      transition: "all 0.3s",
      zIndex: 200,
    }}>

      {/* Logo */}
      <div style={{
        padding: "20px 18px",
        borderBottom: `1px solid ${border}`,
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <div style={{
            background: "#38bdf820",
            borderRadius: "8px",
            padding: "6px",
            display: "flex",
            alignItems: "center",
          }}>
            <Shield size={18} color="#38bdf8" />
          </div>
          <div>
            <div style={{ color: "#38bdf8", fontWeight: "700", fontSize: "16px", letterSpacing: "1px" }}>AFCIP</div>
            <div style={{ color: subtext, fontSize: "10px", marginTop: "1px", letterSpacing: "0.05em" }}>INTELLIGENCE PLATFORM</div>
          </div>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            style={{ background: "none", border: "none", color: subtext, cursor: "pointer", fontSize: "18px", padding: "4px" }}
          >✕</button>
        )}
      </div>

      {/* Section label */}
      <div style={{ padding: "16px 18px 4px", fontSize: "11px", color: subtext, fontWeight: "600", letterSpacing: "0.08em", textTransform: "uppercase" }}>
        Navigation
      </div>

      {/* Nav Links */}
      <nav style={{ flex: 1, paddingTop: "4px", overflowY: "auto" }}>
        {navItems.map(({ path, label, icon: Icon }) => (
          <NavLink
            key={path}
            to={path}
            onClick={handleNav}
            style={({ isActive }) => ({
              display: "flex",
              alignItems: "center",
              gap: "10px",
              padding: "10px 18px",
              fontSize: "13px",
              textDecoration: "none",
              color: isActive ? "#ffffff" : subtext,
              background: isActive ? "#38bdf815" : "transparent",
              borderLeft: isActive ? "3px solid #38bdf8" : "3px solid transparent",
              transition: "all 0.15s",
              margin: "1px 0",
            })}
            onMouseEnter={e => {
              if (!e.currentTarget.style.borderLeftColor.includes("38bdf8")) {
                e.currentTarget.style.background = isDark ? "#ffffff08" : "#00000008";
                e.currentTarget.style.color = text;
              }
            }}
            onMouseLeave={e => {
              const isActive = e.currentTarget.getAttribute("aria-current") === "page";
              if (!isActive) {
                e.currentTarget.style.background = "transparent";
                e.currentTarget.style.color = subtext;
              }
            }}
          >
            <Icon size={15} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Logout */}
      <div style={{ padding: "16px 18px", borderTop: `1px solid ${border}` }}>
        <button
          onClick={handleLogout}
          style={{
            background: "none",
            border: `1px solid ${isDark ? "#334155" : "#fca5a5"}`,
            borderRadius: "8px",
            color: "#ef4444",
            fontSize: "13px",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            gap: "8px",
            width: "100%",
            padding: "9px 12px",
            transition: "all 0.15s",
          }}
          onMouseEnter={e => e.currentTarget.style.background = "#ef444415"}
          onMouseLeave={e => e.currentTarget.style.background = "none"}
        >
          <LogOut size={14} />
          Logout
        </button>
      </div>
    </div>
  );
};

export default Sidebar;