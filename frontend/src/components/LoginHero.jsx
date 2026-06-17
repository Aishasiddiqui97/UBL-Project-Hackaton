import { useEffect, useRef, useState } from "react";

// Animated counter hook
function useCounter(target, duration = 2000) {
  const [count, setCount] = useState(0);
  useEffect(() => {
    let start = 0;
    const step = target / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= target) { setCount(target); clearInterval(timer); }
      else setCount(Math.floor(start));
    }, 16);
    return () => clearInterval(timer);
  }, [target, duration]);
  return count;
}

// Typing animation hook
function useTyping(texts, speed = 60, pause = 1800) {
  const [display, setDisplay] = useState("");
  const [textIdx, setTextIdx] = useState(0);
  const [charIdx, setCharIdx] = useState(0);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const current = texts[textIdx];
    const timeout = setTimeout(() => {
      if (!deleting) {
        setDisplay(current.slice(0, charIdx + 1));
        if (charIdx + 1 === current.length) {
          setTimeout(() => setDeleting(true), pause);
        } else {
          setCharIdx(c => c + 1);
        }
      } else {
        setDisplay(current.slice(0, charIdx - 1));
        if (charIdx - 1 === 0) {
          setDeleting(false);
          setCharIdx(0);
          setTextIdx(i => (i + 1) % texts.length);
        } else {
          setCharIdx(c => c - 1);
        }
      }
    }, deleting ? speed / 2 : speed);
    return () => clearTimeout(timeout);
  }, [charIdx, deleting, textIdx, texts, speed, pause]);

  return display;
}

// Canvas grid/pulse background
function GridCanvas() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    let animId;
    let time = 0;

    const resize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    // Particles
    const particles = Array.from({ length: 40 }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      size: Math.random() * 1.5 + 0.5,
      opacity: Math.random() * 0.5 + 0.2,
    }));

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      time += 0.008;

      // Grid lines
      ctx.strokeStyle = "rgba(56, 189, 248, 0.04)";
      ctx.lineWidth = 1;
      const gridSize = 60;
      for (let x = 0; x < canvas.width; x += gridSize) {
        ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
      }
      for (let y = 0; y < canvas.height; y += gridSize) {
        ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
      }

      // Pulse rings from center-left
      const px = canvas.width * 0.35;
      const py = canvas.height * 0.5;
      for (let i = 0; i < 4; i++) {
        const r = ((time * 60 + i * 80) % 320);
        const alpha = Math.max(0, 0.15 - r / 2000);
        ctx.beginPath();
        ctx.arc(px, py, r, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(56, 189, 248, ${alpha})`;
        ctx.lineWidth = 1.5;
        ctx.stroke();
      }

      // Particles
      particles.forEach(p => {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0) p.x = canvas.width;
        if (p.x > canvas.width) p.x = 0;
        if (p.y < 0) p.y = canvas.height;
        if (p.y > canvas.height) p.y = 0;

        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(56, 189, 248, ${p.opacity})`;
        ctx.fill();
      });

      // Connect nearby particles
      particles.forEach((a, i) => {
        particles.slice(i + 1).forEach(b => {
          const dist = Math.hypot(a.x - b.x, a.y - b.y);
          if (dist < 100) {
            ctx.beginPath();
            ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
            ctx.strokeStyle = `rgba(56, 189, 248, ${0.08 * (1 - dist / 100)})`;
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        });
      });

      // Scanline sweep
      const scanY = (time * 80) % canvas.height;
      const grad = ctx.createLinearGradient(0, scanY - 40, 0, scanY + 40);
      grad.addColorStop(0, "rgba(56,189,248,0)");
      grad.addColorStop(0.5, "rgba(56,189,248,0.04)");
      grad.addColorStop(1, "rgba(56,189,248,0)");
      ctx.fillStyle = grad;
      ctx.fillRect(0, scanY - 40, canvas.width, 80);

      animId = requestAnimationFrame(draw);
    };

    draw();
    return () => { cancelAnimationFrame(animId); window.removeEventListener("resize", resize); };
  }, []);

  return (
    <canvas ref={canvasRef} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", pointerEvents: "none" }} />
  );
}

function LoginHero() {
  const txCount = useCounter(10482);
  const alertCount = useCounter(143);
  const caseCount = useCounter(28);
  const typedText = useTyping([
    "Detecting Financial Crime",
    "Monitoring Transactions",
    "Scoring Risk in Real Time",
    "Protecting the Financial System",
  ], 55, 2000);

  const features = [
    { icon: "⚡", text: "Real-Time Fraud Detection" },
    { icon: "📊", text: "Transaction Monitoring" },
    { icon: "◎", text: "AI Risk Scoring Engine" },
    { icon: "📁", text: "Investigation Management" },
  ];

  return (
    <div style={{ flex: 1, position: "relative", overflow: "hidden", background: "#0a1628", display: "flex", flexDirection: "column", justifyContent: "center", padding: "48px 72px" }}>

      {/* Animated background */}
      <GridCanvas />

      {/* Gradient overlays */}
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 30% 50%, rgba(37,99,235,0.12) 0%, transparent 60%)", pointerEvents: "none" }} />
      <div style={{ position: "absolute", inset: 0, background: "radial-gradient(ellipse at 80% 20%, rgba(56,189,248,0.06) 0%, transparent 50%)", pointerEvents: "none" }} />

      {/* Content */}
      <div style={{ position: "relative", zIndex: 1 }}>

        {/* Logo */}
        <div style={{ display: "flex", alignItems: "center", gap: "12px", marginBottom: "40px" }}>
          <div style={{ position: "relative" }}>
            <div style={{ width: "44px", height: "44px", background: "linear-gradient(135deg, #1d4ed8, #0891b2)", borderRadius: "10px", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "22px", boxShadow: "0 0 20px rgba(56,189,248,0.3)" }}>
              🛡️
            </div>
            <div style={{ position: "absolute", inset: 0, borderRadius: "10px", border: "1px solid rgba(56,189,248,0.4)", animation: "pulse-border 2s ease-in-out infinite" }} />
          </div>
          <div>
            <div style={{ color: "#38bdf8", fontWeight: "800", fontSize: "22px", letterSpacing: "3px" }}>AFCIP</div>
            <div style={{ color: "#475569", fontSize: "11px", letterSpacing: "1px" }}>SECURE INTELLIGENCE PLATFORM</div>
          </div>
        </div>

        {/* Headline with typing */}
        <div style={{ marginBottom: "12px" }}>
          <div style={{ color: "#64748b", fontSize: "13px", letterSpacing: "2px", textTransform: "uppercase", marginBottom: "16px" }}>Advanced Financial Crime Intelligence</div>
          <h1 style={{ fontSize: "52px", fontWeight: "800", lineHeight: 1.1, color: "white", marginBottom: "8px", maxWidth: "600px" }}>
            {typedText}
            <span style={{ color: "#38bdf8", animation: "blink 1s step-end infinite" }}>|</span>
          </h1>
        </div>

        <p style={{ color: "#94a3b8", fontSize: "16px", maxWidth: "500px", lineHeight: 1.7, marginBottom: "40px" }}>
          AI-powered platform for financial institutions to detect, investigate and prevent fraud with real-time precision.
        </p>

        {/* Feature list */}
        <div style={{ display: "flex", flexDirection: "column", gap: "12px", marginBottom: "48px" }}>
          {features.map((f, i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: "12px" }}>
              <div style={{ width: "28px", height: "28px", background: "rgba(56,189,248,0.1)", border: "1px solid rgba(56,189,248,0.2)", borderRadius: "6px", display: "flex", alignItems: "center", justifyContent: "center", fontSize: "13px", flexShrink: 0 }}>
                {f.icon}
              </div>
              <span style={{ color: "#cbd5e1", fontSize: "14px" }}>{f.text}</span>
            </div>
          ))}
        </div>

        {/* Live stats */}
        <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
          {[
            { label: "Transactions Monitored", value: txCount.toLocaleString(), suffix: "", color: "#38bdf8" },
            { label: "Fraud Alerts", value: alertCount, suffix: "", color: "#f87171" },
            { label: "Open Cases", value: caseCount, suffix: "", color: "#a78bfa" },
          ].map((s, i) => (
            <div key={i} style={{ background: "rgba(30,41,59,0.6)", border: "1px solid rgba(56,189,248,0.15)", borderRadius: "12px", padding: "16px 20px", backdropFilter: "blur(8px)", minWidth: "130px" }}>
              <div style={{ color: s.color, fontSize: "26px", fontWeight: "800", fontVariantNumeric: "tabular-nums" }}>{s.value}{s.suffix}</div>
              <div style={{ color: "#64748b", fontSize: "11px", marginTop: "4px", letterSpacing: "0.5px" }}>{s.label}</div>
              <div style={{ display: "flex", alignItems: "center", gap: "4px", marginTop: "6px" }}>
                <div style={{ width: "6px", height: "6px", background: "#22c55e", borderRadius: "50%", animation: "live-pulse 1.5s ease-in-out infinite" }} />
                <span style={{ color: "#22c55e", fontSize: "10px", fontWeight: "600" }}>LIVE</span>
              </div>
            </div>
          ))}
        </div>

        {/* Bottom badge */}
        <div style={{ marginTop: "40px", display: "flex", alignItems: "center", gap: "8px" }}>
          <div style={{ width: "8px", height: "8px", background: "#22c55e", borderRadius: "50%", animation: "live-pulse 1.5s ease-in-out infinite" }} />
          <span style={{ color: "#475569", fontSize: "12px" }}>All systems operational · 99.9% uptime · SBP Compliant</span>
        </div>

      </div>

      <style>{`
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyframes live-pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.8)} }
        @keyframes pulse-border { 0%,100%{opacity:0.4;transform:scale(1)} 50%{opacity:1;transform:scale(1.08)} }
      `}</style>
    </div>
  );
}

export default LoginHero;