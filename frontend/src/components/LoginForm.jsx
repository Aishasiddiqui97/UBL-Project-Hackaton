import { useState } from "react";
import { useNavigate } from "react-router-dom";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPass, setShowPass] = useState(false);
  const [focused, setFocused] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");
    if (!email || !password) { setError("Please fill in all fields."); return; }
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      localStorage.setItem("isAuthenticated", "true");
      navigate("/dashboard");
    }, 1400);
  };

  const inputStyle = (key) => ({
    width: "100%",
    padding: "14px 16px",
    border: `1px solid ${focused === key ? "#38bdf8" : "#1e3a5f"}`,
    background: "rgba(15,23,42,0.8)",
    color: "white",
    borderRadius: "10px",
    outline: "none",
    fontSize: "14px",
    boxSizing: "border-box",
    transition: "border-color 0.2s, box-shadow 0.2s",
    boxShadow: focused === key ? "0 0 0 3px rgba(56,189,248,0.1)" : "none",
  });

  return (
    <div style={{
      width: "440px",
      minHeight: "100vh",
      background: "rgba(15,23,42,0.95)",
      backdropFilter: "blur(20px)",
      borderLeft: "1px solid rgba(56,189,248,0.12)",
      color: "white",
      padding: "48px 44px",
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      position: "relative",
      overflow: "hidden",
    }}>

      <div style={{ position: "absolute", top: "-60px", right: "-60px", width: "200px", height: "200px", background: "radial-gradient(circle, rgba(37,99,235,0.15) 0%, transparent 70%)", pointerEvents: "none" }} />
      <div style={{ position: "absolute", bottom: "-60px", left: "-60px", width: "200px", height: "200px", background: "radial-gradient(circle, rgba(56,189,248,0.08) 0%, transparent 70%)", pointerEvents: "none" }} />

      <div style={{ position: "relative", zIndex: 1 }}>

        {/* Header */}
        <div style={{ marginBottom: "36px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "24px" }}>
            <div style={{ width: "32px", height: "2px", background: "linear-gradient(90deg, #2563eb, #38bdf8)" }} />
            <span style={{ color: "#38bdf8", fontSize: "11px", letterSpacing: "2px", fontWeight: "600" }}>SECURE ACCESS</span>
          </div>
          <h2 style={{ fontSize: "28px", fontWeight: "800", marginBottom: "8px", color: "white" }}>Welcome Back</h2>
          <p style={{ color: "#64748b", fontSize: "14px", lineHeight: 1.6 }}>Sign in to your AFCIP account to access the intelligence dashboard.</p>
        </div>

        {/* Error */}
        {error && (
          <div style={{ background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.3)", borderRadius: "8px", padding: "12px 14px", marginBottom: "16px", display: "flex", alignItems: "center", gap: "8px" }}>
            <span style={{ fontSize: "14px" }}>⚠️</span>
            <span style={{ color: "#f87171", fontSize: "13px" }}>{error}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit}>

          {/* Email Label + Input */}
          <div style={{ marginBottom: "16px" }}>
            <label style={{ display: "block", color: "#64748b", fontSize: "12px", fontWeight: "600", letterSpacing: "0.05em", marginBottom: "8px" }}>
              EMAIL ADDRESS
            </label>
            <input
              type="email"
              placeholder="admin@afcip.gov.pk"
              value={email}
              onChange={e => setEmail(e.target.value)}
              onFocus={() => setFocused("email")}
              onBlur={() => setFocused("")}
              autoComplete="username"
              style={inputStyle("email")}
            />
          </div>

          {/* Password Label + Input */}
          <div style={{ marginBottom: "8px" }}>
            <label style={{ display: "block", color: "#64748b", fontSize: "12px", fontWeight: "600", letterSpacing: "0.05em", marginBottom: "8px" }}>
              PASSWORD
            </label>
            <div style={{ position: "relative" }}>
              <input
                type={showPass ? "text" : "password"}
                placeholder="Enter your password"
                value={password}
                onChange={e => setPassword(e.target.value)}
                onFocus={() => setFocused("password")}
                onBlur={() => setFocused("")}
                autoComplete="current-password"
                style={{ ...inputStyle("password"), paddingRight: "44px" }}
              />
              <button
                type="button"
                onClick={() => setShowPass(p => !p)}
                style={{ position: "absolute", right: "14px", top: "50%", transform: "translateY(-50%)", background: "none", border: "none", cursor: "pointer", fontSize: "15px", color: "#64748b" }}
              >
                {showPass ? "🙈" : "👁️"}
              </button>
            </div>
          </div>

          {/* Forgot */}
          <div style={{ textAlign: "right", marginBottom: "24px" }}>
            <span style={{ color: "#38bdf8", fontSize: "12px", cursor: "pointer" }}>Forgot password?</span>
          </div>

          {/* Submit */}
          <button type="submit" disabled={loading} style={{
            width: "100%",
            padding: "14px",
            border: "none",
            borderRadius: "10px",
            background: loading ? "#1e3a5f" : "linear-gradient(135deg, #2563eb, #0891b2)",
            color: "white",
            fontSize: "15px",
            fontWeight: "700",
            cursor: loading ? "not-allowed" : "pointer",
            letterSpacing: "0.5px",
            transition: "all 0.3s",
            boxShadow: loading ? "none" : "0 4px 20px rgba(37,99,235,0.4)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "8px",
          }}>
            {loading ? (
              <>
                <div style={{ width: "16px", height: "16px", border: "2px solid rgba(255,255,255,0.3)", borderTop: "2px solid white", borderRadius: "50%", animation: "spin 0.7s linear infinite" }} />
                Authenticating...
              </>
            ) : (
              <> 🔐 Sign In to AFCIP </>
            )}
          </button>
        </form>

        {/* Divider */}
        <div style={{ display: "flex", alignItems: "center", gap: "12px", margin: "28px 0" }}>
          <div style={{ flex: 1, height: "1px", background: "#1e293b" }} />
          <span style={{ color: "#334155", fontSize: "12px" }}>DEMO CREDENTIALS</span>
          <div style={{ flex: 1, height: "1px", background: "#1e293b" }} />
        </div>

        {/* Demo hint */}
        <div style={{ background: "rgba(37,99,235,0.08)", border: "1px solid rgba(37,99,235,0.2)", borderRadius: "10px", padding: "14px 16px" }}>
          <div style={{ color: "#93c5fd", fontSize: "12px", marginBottom: "8px", fontWeight: "600" }}>🧪 For Demo / Hackathon</div>
          <div style={{ color: "#64748b", fontSize: "12px", lineHeight: 1.8 }}>
            Email: <span style={{ color: "#94a3b8" }}>admin@afcip.gov.pk</span><br />
            Password: <span style={{ color: "#94a3b8" }}>any value works</span>
          </div>
        </div>

        {/* Footer */}
        <div style={{ marginTop: "32px", textAlign: "center" }}>
          <span style={{ color: "#334155", fontSize: "11px" }}>🔒 256-bit SSL Encrypted · SBP Compliant · AFCIP v2.1</span>
        </div>

      </div>

      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        input::placeholder { color: #334155; }
        input:-webkit-autofill,
        input:-webkit-autofill:hover,
        input:-webkit-autofill:focus {
          -webkit-box-shadow: 0 0 0px 1000px rgba(15,23,42,0.95) inset !important;
          -webkit-text-fill-color: white !important;
          caret-color: white;
          border: 1px solid #38bdf8 !important;
        }
      `}</style>
    </div>
  );
};

export default LoginForm;