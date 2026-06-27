import { useState, useEffect } from 'react';
import PageLayout from "../components/layout/PageLayout";
import { useTheme } from "../context/ThemeContext";
import apiService from "../services/api";
import { Shield, Clock, User, FileText, Filter, Download, RefreshCw } from 'lucide-react';

const AuditTrail = () => {
  const { surface, border, text, subtext, accent, isDark } = useTheme();
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    action: '',
    resource_type: '',
    status: '',
  });

  useEffect(() => {
    fetchAuditLogs();
  }, []);

  const fetchAuditLogs = async () => {
    try {
      setLoading(true);
      const response = await apiService.apiCall('/audit-trail/');
      setAuditLogs(response.data || response || []);
      setError(null);
    } catch (err) {
      console.error('Failed to fetch audit logs:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const getActionColor = (action) => {
    const colors = {
      CREATE: '#22c55e',
      READ: '#38bdf8',
      UPDATE: '#f59e0b',
      DELETE: '#ef4444',
      LOGIN: '#a78bfa',
      LOGOUT: '#64748b',
      FAILED_LOGIN: '#ef4444',
      EXPORT: '#38bdf8',
      APPROVE: '#22c55e',
      REJECT: '#ef4444',
      ESCALATE: '#fb923c',
      ASSIGN: '#a78bfa',
      RESOLVE: '#22c55e',
    };
    return colors[action] || '#64748b';
  };

  const getStatusColor = (status) => {
    return status === 'SUCCESS' ? '#22c55e' : '#ef4444';
  };

  const filteredLogs = auditLogs.filter(log => {
    if (filters.action && log.action !== filters.action) return false;
    if (filters.resource_type && log.resource_type !== filters.resource_type) return false;
    if (filters.status && log.status !== filters.status) return false;
    return true;
  });

  return (
    <PageLayout title="Audit Trail" subtitle="System activity and security monitoring">
      {/* Stats Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
        <div style={{
          background: surface,
          border: `1px solid ${border}`,
          borderRadius: '12px',
          padding: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
        }}>
          <div style={{ background: '#38bdf818', borderRadius: '10px', padding: '12px' }}>
            <Shield size={24} color="#38bdf8" />
          </div>
          <div>
            <div style={{ color: subtext, fontSize: '12px', marginBottom: '4px' }}>Total Events</div>
            <div style={{ color: text, fontSize: '24px', fontWeight: '700' }}>{auditLogs.length}</div>
          </div>
        </div>

        <div style={{
          background: surface,
          border: `1px solid ${border}`,
          borderRadius: '12px',
          padding: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
        }}>
          <div style={{ background: '#22c55e18', borderRadius: '10px', padding: '12px' }}>
            <Clock size={24} color="#22c55e" />
          </div>
          <div>
            <div style={{ color: subtext, fontSize: '12px', marginBottom: '4px' }}>Today</div>
            <div style={{ color: text, fontSize: '24px', fontWeight: '700' }}>
              {auditLogs.filter(l => new Date(l.created_at).toDateString() === new Date().toDateString()).length}
            </div>
          </div>
        </div>

        <div style={{
          background: surface,
          border: `1px solid ${border}`,
          borderRadius: '12px',
          padding: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
        }}>
          <div style={{ background: '#ef444418', borderRadius: '10px', padding: '12px' }}>
            <User size={24} color="#ef4444" />
          </div>
          <div>
            <div style={{ color: subtext, fontSize: '12px', marginBottom: '4px' }}>Failed Actions</div>
            <div style={{ color: text, fontSize: '24px', fontWeight: '700' }}>
              {auditLogs.filter(l => l.status === 'FAILED').length}
            </div>
          </div>
        </div>

        <div style={{
          background: surface,
          border: `1px solid ${border}`,
          borderRadius: '12px',
          padding: '20px',
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
        }}>
          <div style={{ background: '#a78bfa18', borderRadius: '10px', padding: '12px' }}>
            <FileText size={24} color="#a78bfa" />
          </div>
          <div>
            <div style={{ color: subtext, fontSize: '12px', marginBottom: '4px' }}>Unique Users</div>
            <div style={{ color: text, fontSize: '24px', fontWeight: '700' }}>
              {new Set(auditLogs.map(l => l.user_email)).size}
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div style={{
        background: surface,
        border: `1px solid ${border}`,
        borderRadius: '12px',
        padding: '16px 20px',
        marginBottom: '20px',
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
      }}>
        <Filter size={18} color={subtext} />
        <select
          value={filters.action}
          onChange={(e) => setFilters({ ...filters, action: e.target.value })}
          style={{
            background: isDark ? '#1e293b' : '#f8fafc',
            border: `1px solid ${border}`,
            borderRadius: '8px',
            padding: '8px 12px',
            color: text,
            fontSize: '13px',
            outline: 'none',
          }}
        >
          <option value="">All Actions</option>
          <option value="CREATE">Create</option>
          <option value="READ">Read</option>
          <option value="UPDATE">Update</option>
          <option value="DELETE">Delete</option>
          <option value="LOGIN">Login</option>
          <option value="LOGOUT">Logout</option>
          <option value="FAILED_LOGIN">Failed Login</option>
          <option value="APPROVE">Approve</option>
          <option value="REJECT">Reject</option>
        </select>

        <select
          value={filters.resource_type}
          onChange={(e) => setFilters({ ...filters, resource_type: e.target.value })}
          style={{
            background: isDark ? '#1e293b' : '#f8fafc',
            border: `1px solid ${border}`,
            borderRadius: '8px',
            padding: '8px 12px',
            color: text,
            fontSize: '13px',
            outline: 'none',
          }}
        >
          <option value="">All Resources</option>
          <option value="Transaction">Transaction</option>
          <option value="User">User</option>
          <option value="KYCProfile">KYC Profile</option>
          <option value="Case">Case</option>
          <option value="FraudAlert">Fraud Alert</option>
        </select>

        <select
          value={filters.status}
          onChange={(e) => setFilters({ ...filters, status: e.target.value })}
          style={{
            background: isDark ? '#1e293b' : '#f8fafc',
            border: `1px solid ${border}`,
            borderRadius: '8px',
            padding: '8px 12px',
            color: text,
            fontSize: '13px',
            outline: 'none',
          }}
        >
          <option value="">All Status</option>
          <option value="SUCCESS">Success</option>
          <option value="FAILED">Failed</option>
        </select>

        <button
          onClick={fetchAuditLogs}
          style={{
            marginLeft: 'auto',
            background: accent,
            border: 'none',
            borderRadius: '8px',
            padding: '8px 16px',
            color: '#fff',
            fontSize: '13px',
            fontWeight: '500',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
          }}
        >
          <RefreshCw size={14} />
          Refresh
        </button>

        <button
          onClick={() => window.open('/api/audit-trail/export/', '_blank')}
          style={{
            background: isDark ? '#334155' : '#e2e8f0',
            border: 'none',
            borderRadius: '8px',
            padding: '8px 16px',
            color: text,
            fontSize: '13px',
            fontWeight: '500',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
          }}
        >
          <Download size={14} />
          Export
        </button>
      </div>

      {/* Audit Log Table */}
      <div style={{
        background: surface,
        border: `1px solid ${border}`,
        borderRadius: '12px',
        overflow: 'hidden',
      }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: `1px solid ${border}` }}>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Timestamp</th>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>User</th>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Action</th>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Resource</th>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Description</th>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="6" style={{ padding: '40px', textAlign: 'center', color: subtext }}>Loading audit logs...</td>
              </tr>
            ) : error ? (
              <tr>
                <td colSpan="6" style={{ padding: '40px', textAlign: 'center', color: '#ef4444' }}>Error: {error}</td>
              </tr>
            ) : filteredLogs.length === 0 ? (
              <tr>
                <td colSpan="6" style={{ padding: '40px', textAlign: 'center', color: subtext }}>No audit logs found</td>
              </tr>
            ) : (
              filteredLogs.map((log) => (
                <tr key={log.id} style={{ borderBottom: `1px solid ${border}` }}>
                  <td style={{ padding: '14px 16px', color: subtext, fontSize: '13px' }}>
                    {new Date(log.created_at).toLocaleString()}
                  </td>
                  <td style={{ padding: '14px 16px', color: text, fontSize: '13px', fontWeight: '500' }}>
                    {log.user_email || 'System'}
                  </td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{
                      background: `${getActionColor(log.action)}18`,
                      color: getActionColor(log.action),
                      padding: '4px 10px',
                      borderRadius: '6px',
                      fontSize: '12px',
                      fontWeight: '600',
                    }}>
                      {log.action}
                    </span>
                  </td>
                  <td style={{ padding: '14px 16px', color: text, fontSize: '13px' }}>
                    {log.resource_type}
                    {log.resource_id && <span style={{ color: subtext }}> #{log.resource_id}</span>}
                  </td>
                  <td style={{ padding: '14px 16px', color: text, fontSize: '13px', maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {log.description}
                  </td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{
                      background: `${getStatusColor(log.status)}18`,
                      color: getStatusColor(log.status),
                      padding: '4px 10px',
                      borderRadius: '6px',
                      fontSize: '12px',
                      fontWeight: '600',
                    }}>
                      {log.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </PageLayout>
  );
};

export default AuditTrail;
