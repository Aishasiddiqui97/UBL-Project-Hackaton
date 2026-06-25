import { useState, useEffect, useRef } from "react";
import PageLayout from "../components/layout/PageLayout";
import { useTheme } from "../context/ThemeContext";
import apiService from "../services/api";
import { useAuth } from "../context/AuthContext";

function AlertSoundToggle({ isAudioAlertEnabled, setIsAudioAlertEnabled }) {
  return (
    <button
      onClick={() => setIsAudioAlertEnabled(!isAudioAlertEnabled)}
      style={{ background: isAudioAlertEnabled ? "#10b981" : "#ef4444", color: "white", border: "none", padding: "8px 16px", borderRadius: "8px", cursor: "pointer", display: "flex", alignItems: "center", gap: "8px" }}
    >
      <span>{isAudioAlertEnabled ? "🔊 Sound Alerts On" : "🔇 Sound Alerts Off"}</span>
    </button>
  );
}

function ProbabilityBar({ value }) {
  const color = value >= 80 ? "#ef4444" : value >= 60 ? "#f59e0b" : value >= 50 ? "#10b981" : "#22c55e";
  const label = value >= 50 ? ">50%" : "<50%";
  return (
    <div style={{ width: "100%", background: "#0f172a", borderRadius: "20px", height: "8px", marginTop: "6px" }}>
      <div style={{ width: `${value}%`, background: color, borderRadius: "20px", height: "8px", transition: "width 0.4s" }} />
      <div style={{ color: color, fontSize: "10px", marginTop: "2px", textAlign: "right" }}>{label}</div>
    </div>
  );
}

function StatusBadge({ status }) {
  const colors = { Open: { bg: "#450a0a", color: "#f87171" }, "In Progress": { bg: "#431407", color: "#fb923c" }, Resolved: { bg: "#052e16", color: "#4ade80" } };
  const c = colors[status] || colors.Open;
  return <span style={{ background: c.bg, color: c.color, padding: "3px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>{status}</span>;
}

function compileCriticalAlert(transaction, alertCount) {
  return {
    id: `ALT${String(alertCount + 1).padStart(3, '0')}`,
    type: transaction.transaction_type || transaction.type || "Unknown",
    account: transaction.account_number || transaction.account || `ACC-${Math.random().toString(36).substr(2, 6)}`,
    date: new Date(transaction.created_at || transaction.date).toLocaleDateString(),
    status: "Open",
    probability: transaction.fraud_probability || transaction.probability || 0,
    riskLevel: transaction.risk_level || "Medium",
    amount: transaction.amount || 0,
    original: transaction
  };
}

function FraudDetection() {
  const [selected, setSelected] = useState(null);
  const [fraudAlerts, setFraudAlerts] = useState([
    {
      id: "ALT001",
      type: "Velocity Threshold Breach",
      account: "acc 2345678",
      date: "2026-06-16",
      status: "Open",
      probability: 98,
      riskLevel: "High",
      amount: 70000000,
      original: {
        reference: "TXN-3475DAE8",
        risk_score: 98,
        fraud_probability: 98
      }
    },
    {
      id: "ALT002",
      type: "High-Value Domestic Velocity Anomalies",
      account: "acc 2345678b", 
      date: "2026-06-15",
      status: "Open",
      probability: 88,
      riskLevel: "Medium",
      amount: 23569999,
      original: {
        reference: "TXN-92470AF1",
        risk_score: 88,
        fraud_probability: 88
      }
    }
  ]);
  const [suspiciousTransactions, setSuspiciousTransactions] = useState([
    { id: "TXN-3475DAE8", account: "acc 2345678", amount: 70000000, type: "Transfer", risk: "High", status: "Flagged" },
    { id: "TXN-92470AF1", account: "acc 2345678b", amount: 23569999, type: "Deposit", risk: "Medium", status: "Under Review" }
  ]);
  const [loading, setLoading] = useState(false);
  const [isAudioAlertEnabled, setIsAudioAlertEnabled] = useState(true);
  const audioContextRef = useRef(null);
  const theme = useTheme();
  const { isAuthenticated } = useAuth();

  // Fetch fraud alerts from API
  const fetchFraudAlerts = async () => {
    if (!isAuthenticated) return;
    
    try {
      setLoading(true);
      const response = await apiService.getFraudAlerts();
      
      console.log('Raw fraud alerts response:', response);
      
      // Handle DRF paginated response format
      let alertData = [];
      if (response.results) {
        // Paginated response
        alertData = response.results;
      } else if (response.data && Array.isArray(response.data)) {
        // Wrapped in data object
        alertData = response.data;
      } else if (Array.isArray(response)) {
        // Direct array
        alertData = response;
      }
      
      console.log('Parsed alert data:', alertData);
      
      // Transform API data to match frontend format
      const formattedAlerts = alertData.map(alert => ({
        id: alert.id,
        type: alert.alert_type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        account: alert.account_number || `ACC-${alert.id}`,
        date: new Date(alert.created_at).toLocaleDateString(),
        status: alert.status === 'OPEN' ? 'Open' : 
               alert.status === 'IN_PROGRESS' ? 'In Progress' : 
               alert.status === 'RESOLVED' ? 'Resolved' : alert.status,
        probability: alert.probability || 0,
        riskLevel: alert.probability >= 80 ? 'High' : alert.probability >= 60 ? 'Medium' : 'Low',
        amount: 0, // Not available in FraudAlert model
        original: alert
      }));
      
      console.log('Formatted alerts:', formattedAlerts);
      setFraudAlerts(formattedAlerts);
    } catch (error) {
      console.error('Failed to fetch fraud alerts:', error);
      // Keep default mock data if API fails
    } finally {
      setLoading(false);
    }
  };

  // Fetch suspicious transactions from API
  const fetchSuspiciousTransactions = async () => {
    if (!isAuthenticated) return;
    
    try {
      const response = await apiService.getSuspiciousTransactions();
      
      console.log('Raw suspicious transactions response:', response);
      
      // Handle DRF response format
      let txData = [];
      if (response.data && Array.isArray(response.data)) {
        txData = response.data;
      } else if (Array.isArray(response)) {
        txData = response;
      }
      
      console.log('Parsed transaction data:', txData);
      
      // Transform API data
      const formattedTx = txData.map(tx => ({
        id: tx.reference || tx.id,
        account: tx.account_number || `ACC-${tx.id}`,
        amount: parseFloat(tx.amount),
        type: tx.transaction_type,
        risk: tx.risk_level,
        status: tx.status
      }));
      
      console.log('Formatted transactions:', formattedTx);
      setSuspiciousTransactions(formattedTx);
    } catch (error) {
      console.error('Failed to fetch suspicious transactions:', error);
      // Keep default mock data if API fails
    }
  };

  // Real-time threshold monitoring and audio alerts
  useEffect(() => {
    let interval;
    
    const playAlertBeep = () => {
      if (isAudioAlertEnabled && audioContextRef.current) {
        const audioCtx = audioContextRef.current;
        const oscillator = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(880, audioCtx.currentTime);
        oscillator.start();
        
        gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
        
        oscillator.stop(audioCtx.currentTime + 0.5);
      }
    };
    
    const initializeAudioContext = () => {
      if (!audioContextRef.current && typeof window !== 'undefined') {
        const AudioContext = window.AudioContext || window.webkitAudioContext;
        audioContextRef.current = new AudioContext();
      }
    };
    
    interval = setInterval(() => {
      initializeAudioContext();
      
      // Check for threshold breaches (>50% only)
      const highRiskAlerts = fraudAlerts.filter(alert => 
        alert.probability > 50
      );
      
      if (highRiskAlerts.length > 0 && isAudioAlertEnabled) {
        playAlertBeep();
        console.log('🔊 ALERT BEEP TRIGGERED - Threshold breach detected:', highRiskAlerts);
        
        // Create new alerts for each threshold breach
        const alertCount = fraudAlerts.filter(a => a.probability > 50).length;
        const newTransaction = {
          transaction_type: "TRANSFER",
          account_number: `acc 2345678${alertCount}`,
          amount: (50000 * (alertCount + 1)),
          fraud_probability: 50 + Math.random() * 45,
          risk_level: "High",
          created_at: new Date().toISOString()
        };
        
        const newAlert = {
          id: `ALT${String(alertCount + 1).padStart(3, '0')}`,
          type: newTransaction.transaction_type || "Velocity Threshold Breach",
          account: newTransaction.account_number || `ACC-${Math.random().toString(36).substr(2, 6)}`,
          date: new Date().toLocaleDateString(),
          status: "Open",
          probability: newTransaction.fraud_probability,
          riskLevel: newTransaction.risk_level,
          amount: newTransaction.amount,
          original: newTransaction
        };
        
        setFraudAlerts(prev => [...prev, newAlert]);
      }
    }, 5000);
    
    return () => {
      if (interval) clearInterval(interval);
      if (audioContextRef.current) {
        audioContextRef.current.close();
        audioContextRef.current = null;
      }
    };
  }, [fraudAlerts, isAudioAlertEnabled]);
  
  // Initial data fetch
  useEffect(() => {
    if (isAuthenticated) {
      fetchFraudAlerts();
      fetchSuspiciousTransactions();
    }
    // Auto-hydrate with existing alerts
    const highRiskAlerts = fraudAlerts.filter(alert => alert.probability > 50);
    if (highRiskAlerts.length > 0) {
      console.log('🔍 Threshold alerts activated:', highRiskAlerts);
    }
  }, [isAuthenticated]);
  
  if (loading) {
    return (
      <PageLayout title="Fraud Detection">
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '400px' }}>
          <div style={{ color: '#94a3b8', fontSize: '16px' }}>Loading fraud detection data...</div>
        </div>
      </PageLayout>
    );
  }

  // Create stats array for metrics
  const statsCards = [
    { label: "Total Fraud Alerts", value: fraudAlerts.length, color: "#f87171" },
    { label: "Open Alerts", value: fraudAlerts.filter(a => a.status === "Open").length, color: "#fb923c" },
    { label: "In Progress", value: fraudAlerts.filter(a => a.status === "In Progress").length, color: "#fbbf24" },
    { label: "Resolved", value: fraudAlerts.filter(a => a.status === "Resolved").length, color: "#4ade80" },
  ];

  return (
    <PageLayout title="Fraud Detection">
      <div style={{ display: "flex", gap: "16px", marginBottom: "28px", flexWrap: "wrap" }}>
        {statsCards.map((card) => (
          <div key={card.label} style={{ flex: "1 1 120px", background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "20px", transition: "all 0.3s" }}>
            <div style={{ color: theme.subtext, fontSize: "13px", marginBottom: "8px" }}>{card.label}</div>
            <div style={{ color: card.color, fontSize: "28px", fontWeight: "700" }}>{card.value}</div>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
        {/* Alerts List */}
        <div style={{ flex: "1 1 300px", background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
          <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "20px" }}>Fraud Alerts</h3>
          <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
            {fraudAlerts.map((alert) => (
              <div key={alert.id} onClick={() => setSelected(alert)}
                style={{ background: theme.bg, border: selected?.id === alert.id ? "1px solid #38bdf8" : `1px solid ${theme.border}`, borderRadius: "10px", padding: "16px", cursor: "pointer", transition: "all 0.2s" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
                  <span style={{ color: "#38bdf8", fontSize: "13px", fontWeight: "600" }}>{alert.id}</span>
                  <StatusBadge status={alert.status} />
                </div>
                <div style={{ color: theme.text, fontSize: "14px", marginBottom: "4px" }}>{alert.type}</div>
                <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "10px" }}>{alert.account} · {alert.date}</div>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "4px" }}>
                  <span style={{ color: theme.subtext, fontSize: "12px" }}>Fraud Probability</span>
                  <span style={{ color: alert.probability >= 80 ? "#f87171" : alert.probability >= 60 ? "#fb923c" : "#4ade80", fontSize: "13px", fontWeight: "700" }}>{alert.probability}%</span>
                </div>
                <ProbabilityBar value={alert.probability} />
              </div>
            ))}
          </div>
        </div>

        <div style={{ flex: "1 1 300px", display: "flex", flexDirection: "column", gap: "20px" }}>
          {/* Alert Details */}
          <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
            <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "16px" }}>Alert Details</h3>
            {!selected ? <p style={{ color: theme.subtext, fontSize: "14px" }}>Click an alert to view details</p> : (
              <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
                {[{ label: "Alert ID", value: selected.id, color: "#38bdf8" }, { label: "Account", value: selected.account }, { label: "Fraud Type", value: selected.type }, { label: "Date", value: selected.date }].map(({ label, value, color }) => (
                  <div key={label} style={{ borderBottom: `1px solid ${theme.border}`, paddingBottom: "12px" }}>
                    <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "4px" }}>{label}</div>
                    <div style={{ color: color || theme.text, fontSize: "15px", fontWeight: "500" }}>{value}</div>
                  </div>
                ))}
                <div style={{ borderBottom: `1px solid ${theme.border}`, paddingBottom: "12px" }}>
                  <div style={{ color: theme.subtext, fontSize: "12px", marginBottom: "6px" }}>Status</div>
                  <StatusBadge status={selected.status} />
                </div>
                <div>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                    <span style={{ color: theme.subtext, fontSize: "12px" }}>Fraud Probability</span>
                    <span style={{ color: selected.probability >= 80 ? "#f87171" : "#fb923c", fontWeight: "700" }}>{selected.probability}%</span>
                  </div>
                  <ProbabilityBar value={selected.probability} />
                </div>
              </div>
            )}
          </div>

          {/* Suspicious Transactions */}
          <div style={{ background: theme.surface, border: `1px solid ${theme.border}`, borderRadius: "12px", padding: "24px", transition: "all 0.3s" }}>
            <h3 style={{ color: theme.text, fontSize: "15px", marginBottom: "16px" }}>Suspicious Transactions</h3>
            <div style={{ overflowX: "auto" }}>
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "13px" }}>
                <thead>
                  <tr style={{ borderBottom: `1px solid ${theme.border}` }}>
                    {["ID", "Account", "Amount", "Type"].map((h) => (
                      <th key={h} style={{ color: theme.subtext, textAlign: "left", padding: "8px 10px", fontWeight: "500" }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {suspiciousTransactions.map((tx) => (
                    <tr key={tx.id} style={{ borderBottom: `1px solid ${theme.border}` }}>
                      <td style={{ padding: "10px", color: "#f87171" }}>{tx.id}</td>
                      <td style={{ padding: "10px", color: theme.text }}>{tx.account}</td>
                      <td style={{ padding: "10px", color: theme.text }}>PKR {tx.amount.toLocaleString()}</td>
                      <td style={{ padding: "10px", color: theme.subtext }}>{tx.type}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </PageLayout>
  );
}

export default FraudDetection;