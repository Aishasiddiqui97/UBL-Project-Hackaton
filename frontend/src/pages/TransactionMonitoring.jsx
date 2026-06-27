import { useState, useEffect } from "react";
import PageLayout from "../components/layout/PageLayout";
import { exportToCSV } from "../utils/exportCSV";
import apiService from "../services/api";
import { useAuth } from "../context/AuthContext";
import CreateTransactionModal from "../components/transaction/CreateTransactionModal";

function RiskBadge({ risk }) {
  const colors = { High: { bg: "#450a0a", color: "#f87171" }, Medium: { bg: "#431407", color: "#fb923c" }, Low: { bg: "#052e16", color: "#4ade80" } };
  const c = colors[risk] || colors.Low;
  return <span style={{ background: c.bg, color: c.color, padding: "3px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>{risk}</span>;
}

function StatusBadge({ status }) {
  const colors = { Flagged: { bg: "#450a0a", color: "#f87171" }, "Under Review": { bg: "#431407", color: "#fb923c" }, Clear: { bg: "#052e16", color: "#4ade80" } };
  const c = colors[status] || colors.Clear;
  return <span style={{ background: c.bg, color: c.color, padding: "3px 10px", borderRadius: "20px", fontSize: "12px", fontWeight: "600" }}>{status}</span>;
}

function TransactionMonitoring() {
  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState("All");
  const [filterRisk, setFilterRisk] = useState("All");
  const [selected, setSelected] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const { isAuthenticated } = useAuth();

  // Fetch transactions from API
  const fetchTransactions = async () => {
    if (!isAuthenticated) return;
    
    try {
      const response = await apiService.getTransactions();
      console.log('Transactions API response:', response);
      
      // Handle DRF pagination format
      let transactionData = [];
      
      if (response.results) {
        // Paginated response format
        transactionData = response.results;
      } else if (response.data && Array.isArray(response.data)) {
        // Wrapped array format
        transactionData = response.data;
      } else if (Array.isArray(response)) {
        // Direct array format
        transactionData = response;
      } else if (response.data && response.data.results) {
        // Nested paginated format
        transactionData = response.data.results;
      }
      
      console.log('Parsed transaction data:', transactionData);
      
      // Transform API data to match frontend format
      const formattedTransactions = transactionData.map(tx => ({
        id: tx.reference || tx.id,
        account: tx.account_number || `ACC-${tx.id}`,
        amount: parseFloat(tx.amount),
        type: tx.transaction_type,
        status: tx.status === 'CLEAR' ? 'Clear' : 
               tx.status === 'FLAGGED' ? 'Flagged' : 
               tx.status === 'UNDER_REVIEW' ? 'Under Review' : tx.status,
        risk: tx.risk_level === 'LOW' ? 'Low' : 
              tx.risk_level === 'MEDIUM' ? 'Medium' : 
              tx.risk_level === 'HIGH' ? 'High' : 'Low',
        date: new Date(tx.created_at).toLocaleDateString(),
        fraud_probability: tx.fraud_probability || 0,
        fraud_reason: tx.fraud_reason ? (tx.fraud_reason.details || tx.fraud_reason.alert_type) : null,
        original: tx // Keep original data for details
      }));
      
      console.log('Final formatted transactions:', formattedTransactions);
      setTransactions(formattedTransactions);
    } catch (error) {
      console.error('Failed to fetch transactions:', error);
      // Fallback to empty array if API fails
      setTransactions([]);
    } finally {
      setLoading(false);
    }
  };

  // Fetch fraud statistics
  const fetchStats = async () => {
    if (!isAuthenticated) return;
    
    try {
      const response = await apiService.getFraudStats();
      console.log('Fraud stats response:', response);
      setStats(response.data || response);
    } catch (error) {
      console.error('Failed to fetch fraud stats:', error);
    }
  };

  // Initial data fetch
  useEffect(() => {
    fetchTransactions();
    fetchStats();
  }, [isAuthenticated]);

  // Handle successful transaction creation
  const handleTransactionCreated = () => {
    // Refresh data
    fetchTransactions();
    fetchStats();
  };

  // Auto refresh every 30 seconds
  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(() => {
      setLastUpdated(new Date());
      fetchTransactions();
      fetchStats();
    }, 30000);
    return () => clearInterval(interval);
  }, [autoRefresh, isAuthenticated]);

  const filtered = transactions.filter((tx) => {
    const matchSearch = tx.id.toLowerCase().includes(search.toLowerCase()) || tx.account.toLowerCase().includes(search.toLowerCase());
    const matchStatus = filterStatus === "All" || tx.status === filterStatus;
    const matchRisk = filterRisk === "All" || tx.risk === filterRisk;
    return matchSearch && matchStatus && matchRisk;
  });

  const inputStyle = {
    background: "#0f172a", border: "1px solid #334155", borderRadius: "8px",
    color: "white", padding: "10px 14px", fontSize: "14px", outline: "none"
  };

  // Calculate stats from actual data or use API stats
  const getStats = () => {
    if (stats) {
      return [
        { label: "Total", value: stats.total_transactions, color: "#38bdf8" },
        { label: "Flagged", value: stats.status_breakdown?.flagged || 0, color: "#f87171" },
        { label: "Under Review", value: stats.status_breakdown?.under_review || 0, color: "#fb923c" },
        { label: "Clear", value: stats.status_breakdown?.clear || 0, color: "#4ade80" },
      ];
    }
    
    // Fallback to calculated stats
    return [
      { label: "Total", value: transactions.length, color: "#38bdf8" },
      { label: "Flagged", value: transactions.filter(t => t.status === "Flagged").length, color: "#f87171" },
      { label: "Under Review", value: transactions.filter(t => t.status === "Under Review").length, color: "#fb923c" },
      { label: "Clear", value: transactions.filter(t => t.status === "Clear").length, color: "#4ade80" },
    ];
  };

  if (loading) {
    return (
      <PageLayout title="Transaction Monitoring">
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '400px' }}>
          <div style={{ color: '#94a3b8', fontSize: '16px' }}>Loading transactions...</div>
        </div>
      </PageLayout>
    );
  }

  return (
    <PageLayout title="Transaction Monitoring">

      {/* Stats Row */}
      <div style={{ display: "flex", gap: "16px", marginBottom: "24px" }}>
        {getStats().map(card => (
          <div key={card.label} style={{ flex: 1, background: "#1e293b", border: "1px solid #334155", borderRadius: "12px", padding: "16px 20px" }}>
            <div style={{ color: "#94a3b8", fontSize: "13px", marginBottom: "6px" }}>{card.label}</div>
            <div style={{ color: card.color, fontSize: "26px", fontWeight: "700" }}>{card.value}</div>
          </div>
        ))}
      </div>

      {/* Filters Row */}
      <div style={{ display: "flex", gap: "12px", marginBottom: "20px", flexWrap: "wrap", alignItems: "center" }}>
        <div style={{ position: "relative", flex: 1, minWidth: "200px" }}>
          <span style={{ position: "absolute", left: "10px", top: "50%", transform: "translateY(-50%)", color: "#64748b" }}>🔍</span>
          <input
            style={{ ...inputStyle, width: "100%", paddingLeft: "32px", boxSizing: "border-box" }}
            placeholder="Search by ID or Account..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <select style={inputStyle} value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
          <option value="All">All Status</option>
          <option value="Clear">Clear</option>
          <option value="Flagged">Flagged</option>
          <option value="Under Review">Under Review</option>
        </select>
        <select style={inputStyle} value={filterRisk} onChange={(e) => setFilterRisk(e.target.value)}>
          <option value="All">All Risk</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
        <button onClick={() => { setSearch(""); setFilterStatus("All"); setFilterRisk("All"); }}
          style={{ ...inputStyle, cursor: "pointer", color: "#f87171", borderColor: "#f87171" }}>
          Clear Filters
        </button>
        <button onClick={() => exportToCSV(filtered, "transactions.csv")}
          style={{ background: "#16a34a", border: "none", borderRadius: "8px", padding: "10px 16px", color: "white", fontSize: "13px", fontWeight: "600", cursor: "pointer" }}>
          ⬇️ Export CSV
        </button>
        <button onClick={() => setShowCreateModal(true)}
          style={{ background: "#2563eb", border: "none", borderRadius: "8px", padding: "10px 16px", color: "white", fontSize: "13px", fontWeight: "600", cursor: "pointer" }}>
          ➕ New Transaction
        </button>
        <button onClick={() => { setAutoRefresh(p => !p); }}
          style={{ background: autoRefresh ? "#1e3a5f" : "#1e293b", border: `1px solid ${autoRefresh ? "#38bdf8" : "#334155"}`, borderRadius: "8px", padding: "10px 14px", color: autoRefresh ? "#38bdf8" : "#94a3b8", fontSize: "13px", cursor: "pointer" }}>
          {autoRefresh ? "🔄 Auto ON" : "⏸ Auto OFF"}
        </button>
      </div>

      {/* Last Updated */}
      <div style={{ color: "#475569", fontSize: "12px", marginBottom: "12px" }}>
        Last updated: {lastUpdated.toLocaleTimeString()}
      </div>

      <div style={{ display: "flex", gap: "20px" }}>
        {/* Table */}
        <div style={{ flex: 2, background: "#1e293b", border: "1px solid #334155", borderRadius: "12px", padding: "24px" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
            <h3 style={{ color: "white", fontSize: "15px" }}>All Transactions</h3>
            <span style={{ color: "#94a3b8", fontSize: "13px" }}>{filtered.length} records</span>
          </div>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "14px" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid #334155" }}>
                {["ID", "Account", "Amount", "Type", "Status", "Risk", "Fraud %", "Date"].map(h => (
                  <th key={h} style={{ color: "#94a3b8", textAlign: "left", padding: "10px 12px", fontWeight: "500" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 ? (
                <tr><td colSpan={8} style={{ color: "#94a3b8", textAlign: "center", padding: "32px" }}>
                  {loading ? "Loading transactions..." : 
                   transactions.length === 0 ? "No transactions found. Click 'New Transaction' to create one." :
                   "No transactions match your filters. Try clearing filters."}
                </td></tr>
              ) : (
                filtered.map((tx) => (
                  <tr key={tx.id} onClick={() => setSelected(tx)}
                    style={{ borderBottom: "1px solid #0f172a", cursor: "pointer", background: selected?.id === tx.id ? "#0f172a" : "transparent" }}
                    onMouseEnter={e => { if (selected?.id !== tx.id) e.currentTarget.style.background = "#162032"; }}
                    onMouseLeave={e => { if (selected?.id !== tx.id) e.currentTarget.style.background = "transparent"; }}>
                    <td style={{ padding: "12px", color: "#38bdf8" }}>{tx.id}</td>
                    <td style={{ padding: "12px", color: "white" }}>{tx.account}</td>
                    <td style={{ padding: "12px", color: "white" }}>PKR {tx.amount.toLocaleString()}</td>
                    <td style={{ padding: "12px", color: "#94a3b8" }}>{tx.type}</td>
                    <td style={{ padding: "12px" }}>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                        <StatusBadge status={tx.status} />
                        {tx.status === 'Flagged' && tx.fraud_reason && (
                          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: '#f87171', fontSize: '11px', fontWeight: '500' }}>
                            <span>⚠</span>
                            <span>{tx.fraud_reason}</span>
                          </div>
                        )}
                      </div>
                    </td>
                    <td style={{ padding: "12px" }}><RiskBadge risk={tx.risk} /></td>
                    <td style={{ padding: "12px" }}>
                      <span style={{ 
                        color: tx.fraud_probability >= 80 ? '#ef4444' : 
                               tx.fraud_probability >= 50 ? '#f59e0b' : '#22c55e',
                        fontWeight: '600',
                        fontSize: '13px'
                      }}>
                        {tx.fraud_probability ? `${tx.fraud_probability.toFixed(0)}%` : '0%'}
                      </span>
                    </td>
                    <td style={{ padding: "12px", color: "#94a3b8" }}>{tx.date}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Details Panel */}
        <div style={{ flex: 1, background: "#1e293b", border: "1px solid #334155", borderRadius: "12px", padding: "24px", alignSelf: "flex-start" }}>
          <h3 style={{ color: "white", fontSize: "15px", marginBottom: "20px" }}>
            {selected ? "Transaction & Fraud Details" : "Transaction Details"}
          </h3>
          {!selected ? (
            <p style={{ color: "#94a3b8", fontSize: "14px" }}>Click a transaction to view details</p>
          ) : (
            <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              {/* Basic Info */}
              <div style={{ borderBottom: "1px solid #334155", paddingBottom: "12px" }}>
                <div style={{ color: "#94a3b8", fontSize: "11px", marginBottom: "8px", textTransform: "uppercase", letterSpacing: "1px" }}>Transaction Info</div>
              </div>
              
              {[
                { label: "Transaction ID", value: selected.id, color: "#38bdf8" },
                { label: "Account", value: selected.account },
                { label: "Amount", value: `PKR ${selected.amount.toLocaleString()}` },
                { label: "Type", value: selected.type },
                { label: "Date", value: selected.date },
              ].map(({ label, value, color }) => (
                <div key={label} style={{ borderBottom: "1px solid #334155", paddingBottom: "12px" }}>
                  <div style={{ color: "#94a3b8", fontSize: "12px", marginBottom: "4px" }}>{label}</div>
                  <div style={{ color: color || "white", fontSize: "15px", fontWeight: "500" }}>{value}</div>
                </div>
              ))}
              
              {/* Fraud Detection Section */}
              <div style={{ borderBottom: "1px solid #334155", paddingBottom: "12px", marginTop: "8px" }}>
                <div style={{ color: "#94a3b8", fontSize: "11px", marginBottom: "8px", textTransform: "uppercase", letterSpacing: "1px" }}>🔍 Fraud Detection</div>
              </div>
              
              {/* Status Badge */}
              <div style={{ borderBottom: "1px solid #334155", paddingBottom: "12px" }}>
                <div style={{ color: "#94a3b8", fontSize: "12px", marginBottom: "6px" }}>Status</div>
                <StatusBadge status={selected.status} />
              </div>
              
              {/* Risk Level */}
              <div style={{ borderBottom: "1px solid #334155", paddingBottom: "12px" }}>
                <div style={{ color: "#94a3b8", fontSize: "12px", marginBottom: "6px" }}>Risk Level</div>
                <RiskBadge risk={selected.risk} />
              </div>
              
              {/* Fraud Probability Bar */}
              <div style={{ borderBottom: "1px solid #334155", paddingBottom: "12px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "8px" }}>
                  <span style={{ color: "#94a3b8", fontSize: "12px" }}>Fraud Probability</span>
                  <span style={{ 
                    color: selected.fraud_probability >= 80 ? '#ef4444' : 
                           selected.fraud_probability >= 50 ? '#f59e0b' : '#22c55e',
                    fontSize: "14px", 
                    fontWeight: "700" 
                  }}>
                    {selected.fraud_probability ? `${selected.fraud_probability.toFixed(0)}%` : '0%'}
                  </span>
                </div>
                <div style={{ width: "100%", background: "#0f172a", borderRadius: "20px", height: "8px", overflow: "hidden" }}>
                  <div style={{ 
                    width: `${selected.fraud_probability || 0}%`, 
                    background: selected.fraud_probability >= 80 ? '#ef4444' : 
                               selected.fraud_probability >= 50 ? '#f59e0b' : '#22c55e',
                    borderRadius: "20px", 
                    height: "8px", 
                    transition: "width 0.4s" 
                  }} />
                </div>
              </div>
              
              {/* Fraud Indicators */}
              <div style={{ background: "#0f172a", borderRadius: "8px", padding: "12px", border: "1px solid #334155" }}>
                <div style={{ color: "#94a3b8", fontSize: "11px", marginBottom: "8px", textTransform: "uppercase", letterSpacing: "1px" }}>Risk Indicators</div>
                <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
                  {/* Amount Risk */}
                  {selected.amount > 100000 && (
                    <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                      <span style={{ color: "#f59e0b", fontSize: "14px" }}>⚠️</span>
                      <span style={{ color: "#94a3b8", fontSize: "12px" }}>High Amount ({'>'}100K)</span>
                    </div>
                  )}
                  {selected.amount > 50000 && selected.amount <= 100000 && (
                    <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                      <span style={{ color: "#fbbf24", fontSize: "14px" }}>⚡</span>
                      <span style={{ color: "#94a3b8", fontSize: "12px" }}>Medium Amount (50-100K)</span>
                    </div>
                  )}
                  
                  {/* Risk Level Indicator */}
                  {selected.risk === "High" && (
                    <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                      <span style={{ color: "#ef4444", fontSize: "14px" }}>🚨</span>
                      <span style={{ color: "#ef4444", fontSize: "12px" }}>High Risk Transaction</span>
                    </div>
                  )}
                  {selected.risk === "Medium" && (
                    <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                      <span style={{ color: "#f59e0b", fontSize: "14px" }}>⚠️</span>
                      <span style={{ color: "#f59e0b", fontSize: "12px" }}>Medium Risk Transaction</span>
                    </div>
                  )}
                  {selected.risk === "Low" && (
                    <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                      <span style={{ color: "#22c55e", fontSize: "14px" }}>✓</span>
                      <span style={{ color: "#22c55e", fontSize: "12px" }}>Low Risk Transaction</span>
                    </div>
                  )}
                  
                  {/* If no indicators */}
                  {selected.amount <= 50000 && selected.risk === "Low" && (
                    <div style={{ color: "#64748b", fontSize: "12px", fontStyle: "italic" }}>No risk indicators detected</div>
                  )}
                </div>
              </div>
              
              {/* Action Buttons */}
              <div style={{ display: "flex", flexDirection: "column", gap: "8px", marginTop: "8px" }}>
                <button onClick={() => exportToCSV([selected], `${selected.id}.csv`)}
                  style={{ background: "#16a34a", border: "none", borderRadius: "8px", padding: "10px", color: "white", fontSize: "13px", fontWeight: "600", cursor: "pointer" }}>
                  ⬇️ Export This Transaction
                </button>
                {(selected.status === "Flagged" || selected.status === "Under Review") && (
                  <button 
                    onClick={() => alert(`Review transaction ${selected.id} for fraud`)}
                    style={{ background: "#dc2626", border: "none", borderRadius: "8px", padding: "10px", color: "white", fontSize: "13px", fontWeight: "600", cursor: "pointer" }}>
                    🔍 Review for Fraud
                  </button>
                )}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Create Transaction Modal */}
      <CreateTransactionModal 
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSuccess={handleTransactionCreated}
      />
    </PageLayout>
  );
}

export default TransactionMonitoring;