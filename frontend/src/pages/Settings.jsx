import { useState } from "react";
import PageLayout from "../components/layout/PageLayout";
import { useTheme } from "../context/ThemeContext";

function Settings() {
  const theme = useTheme();
  const [profile, setProfile] = useState({
    name: "Admin User", email: "admin@afcip.gov.pk",
    role: "Super Admin", department: "Financial Crime Unit",
    phone: "+92-300-1234567", location: "Karachi, Pakistan",
  });
  const [saved, setSaved] = useState(false);
  const [notifications, setNotifications] = useState({
    email: true, sms: true, autoRefresh: true,
  });

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const inputStyle = {
    width: "100%",
    background: theme.bg,
    border: `1px solid ${theme.border}`,
    borderRadius: "8px",
    color: theme.text,
    padding: "10px 14px",
    fontSize: "14px",
    outline: "none",
    boxSizing: "border-box",
    transition: "border-color 0.2s",
  };

  const cardStyle = {
    background: theme.surface,
    border: `1px solid ${theme.border}`,
    borderRadius: "12px",
    padding: "24px",
    transition: "all 0.3s",
  };

  const Toggle = ({ value, onChange }) => (
    <div
      onClick={() => onChange(!value)}
      style={{
        width: "44px", height: "24px", borderRadius: "24px",
        background: value ? "#2563eb" : theme.border,
        position: "relative", cursor: "pointer", transition: "background 0.2s", flexShrink: 0,
      }}
    >
      <div style={{
        position: "absolute", top: "3px",
        left: value ? "23px" : "3px",
        width: "18px", height: "18px", borderRadius: "50%",
        background: "white", transition: "left 0.2s",
      }} />
    </div>
  );

  return (
    <PageLayout title="Settings">
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: "20px" }}>

        {/* Profile */}
        <div style={cardStyle}>
          <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "20px" }}>👤 Profile Information</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
            {[
              { label: "Full Name", key: "name" },
              { label: "Email", key: "email" },
              { label: "Phone", key: "phone" },
              { label: "Location", key: "location" },
            ].map(({ label, key }) => (
              <div key={key}>
                <label style={{ color: theme.subtext, fontSize: "12px", marginBottom: "6px", display: "block" }}>{label}</label>
                <input
                  style={inputStyle}
                  value={profile[key]}
                  onChange={e => setProfile(prev => ({ ...prev, [key]: e.target.value }))}
                  onFocus={e => e.target.style.borderColor = "#38bdf8"}
                  onBlur={e => e.target.style.borderColor = theme.border}
                />
              </div>
            ))}
            <div>
              <label style={{ color: theme.subtext, fontSize: "12px", marginBottom: "6px", display: "block" }}>Role</label>
              <input style={{ ...inputStyle, color: theme.subtext, cursor: "not-allowed" }} value={profile.role} disabled />
            </div>
            <div>
              <label style={{ color: theme.subtext, fontSize: "12px", marginBottom: "6px", display: "block" }}>Department</label>
              <input style={{ ...inputStyle, color: theme.subtext, cursor: "not-allowed" }} value={profile.department} disabled />
            </div>
            <button onClick={handleSave} style={{
              background: saved ? "#16a34a" : "#2563eb", border: "none", borderRadius: "8px",
              padding: "12px", color: "white", fontSize: "14px", fontWeight: "600", cursor: "pointer", marginTop: "8px",
              transition: "background 0.3s",
            }}>
              {saved ? "✅ Saved!" : "Save Changes"}
            </button>
          </div>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
          {/* Security */}
          <div style={cardStyle}>
            <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "20px" }}>🔒 Security</h3>
            <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
              {["Current Password", "New Password", "Confirm Password"].map(label => (
                <div key={label}>
                  <label style={{ color: theme.subtext, fontSize: "12px", marginBottom: "6px", display: "block" }}>{label}</label>
                  <input
                    type="password"
                    placeholder="••••••••"
                    style={inputStyle}
                    onFocus={e => e.target.style.borderColor = "#38bdf8"}
                    onBlur={e => e.target.style.borderColor = theme.border}
                  />
                </div>
              ))}
              <button style={{ background: "#7c3aed", border: "none", borderRadius: "8px", padding: "12px", color: "white", fontSize: "14px", fontWeight: "600", cursor: "pointer" }}>
                Update Password
              </button>
            </div>
          </div>

          {/* Preferences */}
          <div style={cardStyle}>
            <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "20px" }}>⚙️ Preferences</h3>

            {/* Theme */}
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px", paddingBottom: "16px", borderBottom: `1px solid ${theme.border}` }}>
              <div>
                <div style={{ color: theme.text, fontSize: "14px" }}>Dark Mode</div>
                <div style={{ color: theme.subtext, fontSize: "12px" }}>Switch between dark and light theme</div>
              </div>
              <Toggle value={theme.isDark} onChange={theme.toggle} />
            </div>

            {[
              { key: "email", label: "Email Notifications", desc: "Receive fraud alerts via email" },
              { key: "sms", label: "SMS Alerts", desc: "Get SMS for high-risk transactions" },
              { key: "autoRefresh", label: "Auto Refresh", desc: "Refresh dashboard every 30 seconds" },
            ].map(({ key, label, desc }) => (
              <div key={key} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
                <div>
                  <div style={{ color: theme.text, fontSize: "14px" }}>{label}</div>
                  <div style={{ color: theme.subtext, fontSize: "12px" }}>{desc}</div>
                </div>
                <Toggle value={notifications[key]} onChange={v => setNotifications(p => ({ ...p, [key]: v }))} />
              </div>
            ))}
          </div>

          {/* System Info */}
          <div style={cardStyle}>
            <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "16px" }}>🖥️ System Information</h3>
            {[
              { label: "Version", value: "AFCIP v2.1.0" },
              { label: "Last Login", value: "2026-06-17 09:15 AM" },
              { label: "Session Expires", value: "2026-06-17 05:15 PM" },
              { label: "IP Address", value: "192.168.1.100" },
            ].map(({ label, value }) => (
              <div key={label} style={{ display: "flex", justifyContent: "space-between", marginBottom: "12px" }}>
                <span style={{ color: theme.subtext, fontSize: "13px" }}>{label}</span>
                <span style={{ color: theme.text, fontSize: "13px", fontWeight: "500" }}>{value}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </PageLayout>
  );
}

export default Settings;