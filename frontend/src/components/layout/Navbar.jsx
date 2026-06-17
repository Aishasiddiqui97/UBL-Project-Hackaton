import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTheme } from "../../context/ThemeContext";
import { Search, Bell, Sun, Moon, User, Settings, LogOut, Menu } from "lucide-react";

const Navbar = ({ title = "Dashboard", onMenuClick }) => {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");
  const [showNotif, setShowNotif] = useState(false);
  const [showUser, setShowUser] = useState(false);
  const { isDark, toggle, navBg, surface, border, text, subtext, accent } = useTheme();

  const now = new Date().toLocaleDateString("en-US", {
    weekday: "long", year: "numeric", month: "long", day: "numeric"
  });

  const notifications = [
    { id: 1, text: "High risk transaction detected", time: "2 min ago", color: "#f87171" },
    { id: 2, text: "New fraud alert: AC-4821", time: "15 min ago", color: "#fb923c" },
    { id: 3, text: "Case CS001 updated", time: "1 hr ago", color: accent },
  ];

  const handleLogout = () => {
    localStorage.removeItem("isAuthenticated");
    navigate("/login");
  };

  const btnStyle = {
    background: surface,
    border: `1px solid ${border}`,
    borderRadius: "8px",
    padding: "8px 10px",
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    transition: "all 0.2s",
    color: subtext,
  };

  return (
    <div style={{
      background: navBg,
      borderBottom: `1px solid ${border}`,
      padding: "12px 24px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      position: "sticky",
      top: 0,
      zIndex: 100,
      transition: "all 0.3s",
      gap: "12px",
    }}>
      <style>{`
        @media (max-width: 768px) {
          .hamburger-btn { display: flex !important; }
          .nav-date { display: none !important; }
          .nav-search { display: none !important; }
        }
      `}</style>

      {/* Left */}
      <div style={{ display: "flex", alignItems: "center", gap: "12px", minWidth: 0 }}>
        <button onClick={onMenuClick} style={{ ...btnStyle, display: "none" }} className="hamburger-btn">
          <Menu size={18} />
        </button>
        <div>
          <h2 style={{ color: text, fontSize: "16px", fontWeight: "600", margin: 0, whiteSpace: "nowrap" }}>{title}</h2>
          <span style={{ color: subtext, fontSize: "12px" }} className="nav-date">{now}</span>
        </div>
      </div>

      {/* Right */}
      <div style={{ display: "flex", alignItems: "center", gap: "10px", position: "relative", flexShrink: 0 }}>

        {/* Search */}
        <div style={{ position: "relative" }} className="nav-search">
          <Search size={14} style={{ position: "absolute", left: "10px", top: "50%", transform: "translateY(-50%)", color: subtext }} />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search transactions..."
            style={{
              background: surface, border: `1px solid ${border}`, borderRadius: "8px",
              color: text, padding: "8px 12px 8px 32px", fontSize: "13px",
              outline: "none", width: "200px", transition: "all 0.3s",
            }}
          />
        </div>

        {/* Theme Toggle */}
        <button onClick={toggle} title={isDark ? "Light Mode" : "Dark Mode"} style={btnStyle}>
          {isDark ? <Sun size={16} /> : <Moon size={16} />}
        </button>

        {/* Notifications */}
        <div style={{ position: "relative" }}>
          <button onClick={() => { setShowNotif(!showNotif); setShowUser(false); }}
            style={{ ...btnStyle, position: "relative" }}>
            <Bell size={16} />
            <span style={{ position: "absolute", top: "6px", right: "6px", background: "#ef4444", borderRadius: "50%", width: "7px", height: "7px", display: "block" }} />
          </button>
          {showNotif && (
            <div style={{ position: "absolute", right: 0, top: "44px", background: surface, border: `1px solid ${border}`, borderRadius: "12px", width: "280px", zIndex: 200, padding: "8px 0", boxShadow: "0 8px 32px rgba(0,0,0,0.3)" }}>
              <div style={{ padding: "10px 16px", borderBottom: `1px solid ${border}`, color: text, fontWeight: "600", fontSize: "14px" }}>Notifications</div>
              {notifications.map(n => (
                <div key={n.id} style={{ padding: "12px 16px", borderBottom: `1px solid ${border}`, cursor: "pointer" }}
                  onMouseEnter={e => e.currentTarget.style.background = isDark ? "#0f172a" : "#f8fafc"}
                  onMouseLeave={e => e.currentTarget.style.background = "transparent"}>
                  <div style={{ color: n.color, fontSize: "13px", marginBottom: "2px" }}>{n.text}</div>
                  <div style={{ color: subtext, fontSize: "11px" }}>{n.time}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* User */}
        <div style={{ position: "relative" }}>
          <div onClick={() => { setShowUser(!showUser); setShowNotif(false); }}
            style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer", background: surface, border: `1px solid ${border}`, borderRadius: "8px", padding: "6px 12px", transition: "all 0.3s" }}>
            <div style={{ width: "28px", height: "28px", background: "#2563eb", borderRadius: "50%", display: "flex", alignItems: "center", justifyContent: "center", color: "white", fontWeight: "700", fontSize: "13px" }}>A</div>
            <div className="nav-date">
              <div style={{ color: text, fontSize: "13px", fontWeight: "600" }}>Admin</div>
              <div style={{ color: subtext, fontSize: "11px" }}>Super Admin</div>
            </div>
          </div>
          {showUser && (
            <div style={{ position: "absolute", right: 0, top: "50px", background: surface, border: `1px solid ${border}`, borderRadius: "12px", width: "180px", zIndex: 200, padding: "8px 0", boxShadow: "0 8px 32px rgba(0,0,0,0.3)" }}>
              {[
                { icon: User, label: "Profile", path: "/settings" },
                { icon: Settings, label: "Settings", path: "/settings" },
              ].map(({ icon: Icon, label, path }) => (
                <div key={label} onClick={() => { navigate(path); setShowUser(false); }}
                  style={{ padding: "10px 16px", cursor: "pointer", color: subtext, fontSize: "14px", display: "flex", alignItems: "center", gap: "10px" }}
                  onMouseEnter={e => e.currentTarget.style.background = isDark ? "#0f172a" : "#f1f5f9"}
                  onMouseLeave={e => e.currentTarget.style.background = "transparent"}>
                  <Icon size={14} /> {label}
                </div>
              ))}
              <div style={{ borderTop: `1px solid ${border}`, margin: "4px 0" }} />
              <div onClick={handleLogout}
                style={{ padding: "10px 16px", cursor: "pointer", color: "#ef4444", fontSize: "14px", display: "flex", alignItems: "center", gap: "10px" }}
                onMouseEnter={e => e.currentTarget.style.background = isDark ? "#0f172a" : "#f1f5f9"}
                onMouseLeave={e => e.currentTarget.style.background = "transparent"}>
                <LogOut size={14} /> Logout
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Navbar;