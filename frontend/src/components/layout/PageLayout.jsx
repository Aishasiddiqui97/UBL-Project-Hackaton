// src/components/layout/PageLayout.jsx
import { useState } from "react";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";
import { useTheme } from "../../context/ThemeContext";

const PageLayout = ({ children, title }) => {
  const { bg, text, border, navBg } = useTheme();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div style={{ display: "flex", minHeight: "100vh", background: bg, color: text, transition: "all 0.3s" }}>

      {/* Desktop Sidebar */}
      <div style={{ display: "none" }} className="desktop-sidebar">
        <Sidebar />
      </div>

      {/* Sidebar - desktop always visible, mobile via overlay */}
      <>
        {/* Mobile Overlay */}
        {mobileOpen && (
          <div
            onClick={() => setMobileOpen(false)}
            style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)", zIndex: 150 }}
          />
        )}

        {/* Sidebar wrapper */}
        <div style={{
          position: "sticky",
          top: 0,
          height: "100vh",
          flexShrink: 0,
          display: "flex",
        }}
          className="sidebar-wrapper"
        >
          <style>{`
            @media (max-width: 768px) {
              .sidebar-wrapper {
                position: fixed !important;
                left: ${mobileOpen ? "0" : "-220px"} !important;
                top: 0 !important;
                height: 100vh !important;
                z-index: 200 !important;
                transition: left 0.3s ease !important;
              }
            }
          `}</style>
          <Sidebar onClose={() => setMobileOpen(false)} />
        </div>
      </>

      <div style={{ flex: 1, display: "flex", flexDirection: "column", minWidth: 0 }}>
        <Navbar title={title} onMenuClick={() => setMobileOpen(true)} />
        <main style={{ flex: 1, padding: "24px", overflowY: "auto", overflowX: "hidden" }}>
          {children}
        </main>
      </div>
    </div>
  );
};

export default PageLayout;