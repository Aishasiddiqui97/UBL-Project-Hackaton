import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./components/auth/ProtectedRoute";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import TransactionMonitoring from "./pages/TransactionMonitoring";
import FraudDetection from "./pages/FraudDetection";
import RiskScoring from "./pages/RiskScoring";
import AlertsManagement from "./pages/AlertsManagement";
import CaseManagement from "./pages/CaseManagement";
import Reports from "./pages/Reports";
import Settings from "./pages/Settings";
import NotFound from "./pages/NotFound";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/transactions" element={<ProtectedRoute><TransactionMonitoring /></ProtectedRoute>} />
        <Route path="/fraud-detection" element={<ProtectedRoute><FraudDetection /></ProtectedRoute>} />
        <Route path="/risk-scoring" element={<ProtectedRoute><RiskScoring /></ProtectedRoute>} />
        <Route path="/alerts" element={<ProtectedRoute><AlertsManagement /></ProtectedRoute>} />
        <Route path="/cases" element={<ProtectedRoute><CaseManagement /></ProtectedRoute>} />
        <Route path="/reports" element={<ProtectedRoute><Reports /></ProtectedRoute>} />
        <Route path="/settings" element={<ProtectedRoute><Settings /></ProtectedRoute>} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
};

export default App;