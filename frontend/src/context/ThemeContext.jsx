import { createContext, useContext, useState } from "react";

const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [isDark, setIsDark] = useState(true);
  const toggle = () => setIsDark(prev => !prev);

  const theme = {
    isDark,
    bg: isDark ? "#0f172a" : "#f1f5f9",
    surface: isDark ? "#1e293b" : "#ffffff",
    border: isDark ? "#334155" : "#e2e8f0",
    text: isDark ? "#ffffff" : "#0f172a",
    subtext: isDark ? "#94a3b8" : "#64748b",
    navBg: isDark ? "#0f172a" : "#ffffff",
    accent: "#38bdf8",
  };

  return (
    <ThemeContext.Provider value={{ ...theme, toggle }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);