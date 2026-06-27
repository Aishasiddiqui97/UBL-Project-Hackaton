import { useState, useEffect } from 'react';
import PageLayout from "../components/layout/PageLayout";
import { useTheme } from "../context/ThemeContext";
import apiService from "../services/api";
import { FileCheck, AlertTriangle, CheckCircle, Clock, RefreshCw, Plus, Eye } from 'lucide-react';

const ComplianceCenter = () => {
  const { surface, border, text, subtext, accent, isDark } = useTheme();
  const [complianceData, setComplianceData] = useState({
    rules: [],
    checks: [],
    reports: [],
    stats: {
      totalChecks: 0,
      passed: 0,
      failed: 0,
      pending: 0,
    }
  });
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchComplianceData();
  }, []);

  const fetchComplianceData = async () => {
    try {
      setLoading(true);
      const [rulesRes, checksRes, reportsRes] = await Promise.allSettled([
        apiService.apiCall('/compliance/rules/'),
        apiService.apiCall('/compliance/checks/'),
        apiService.apiCall('/compliance/reports/'),
      ]);

      const rules = rulesRes.status === 'fulfilled' ? (rulesRes.value?.data || rulesRes.value || []) : [];
      const checks = checksRes.status === 'fulfilled' ? (checksRes.value?.data || checksRes.value || []) : [];
      const reports = reportsRes.status === 'fulfilled' ? (reportsRes.value?.data || reportsRes.value || []) : [];

      const checksArray = Array.isArray(checks) ? checks : [];
      const passedChecks = checksArray.filter(c => c.passed === true).length;
      const failedChecks = checksArray.filter(c => c.passed === false).length;
      const pendingChecks = checksArray.filter(c => c.status === 'PENDING_REVIEW').length;

      setComplianceData({
        rules: Array.isArray(rules) ? rules : [],
        checks: checksArray,
        reports: Array.isArray(reports) ? reports : [],
        stats: {
          totalChecks: checksArray.length,
          passed: passedChecks,
          failed: failedChecks,
          pending: pendingChecks,
        }
      });
    } catch (err) {
      console.error('Failed to fetch compliance data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getCheckStatusColor = (status) => {
    const colors = {
      COMPLIANT: '#22c55e',
      NON_COMPLIANT: '#ef4444',
      PENDING_REVIEW: '#f59e0b',
      EXEMPTED: '#64748b',
    };
    return colors[status] || '#64748b';
  };

  const getReportStatusColor = (status) => {
    const colors = {
      DRAFT: '#64748b',
      PENDING_APPROVAL: '#f59e0b',
      APPROVED: '#22c55e',
      FILED: '#38bdf8',
      REJECTED: '#ef4444',
    };
    return colors[status] || '#64748b';
  };

  return (
    <PageLayout title="Compliance Center" subtitle="Regulatory compliance management and monitoring">
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
            <FileCheck size={24} color="#38bdf8" />
          </div>
          <div>
            <div style={{ color: subtext, fontSize: '12px', marginBottom: '4px' }}>Total Checks</div>
            <div style={{ color: text, fontSize: '24px', fontWeight: '700' }}>{complianceData.stats.totalChecks}</div>
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
            <CheckCircle size={24} color="#22c55e" />
          </div>
          <div>
            <div style={{ color: subtext, fontSize: '12px', marginBottom: '4px' }}>Passed</div>
            <div style={{ color: text, fontSize: '24px', fontWeight: '700' }}>{complianceData.stats.passed}</div>
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
            <AlertTriangle size={24} color="#ef4444" />
          </div>
          <div>
            <div style={{ color: subtext, fontSize: '12px', marginBottom: '4px' }}>Failed</div>
            <div style={{ color: text, fontSize: '24px', fontWeight: '700' }}>{complianceData.stats.failed}</div>
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
          <div style={{ background: '#f59e0b18', borderRadius: '10px', padding: '12px' }}>
            <Clock size={24} color="#f59e0b" />
          </div>
          <div>
            <div style={{ color: subtext, fontSize: '12px', marginBottom: '4px' }}>Pending Review</div>
            <div style={{ color: text, fontSize: '24px', fontWeight: '700' }}>{complianceData.stats.pending}</div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{
        display: 'flex',
        gap: '8px',
        marginBottom: '20px',
        borderBottom: `1px solid ${border}`,
        paddingBottom: '12px',
      }}>
        {['overview', 'rules', 'checks', 'reports'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              background: activeTab === tab ? accent : 'transparent',
              color: activeTab === tab ? '#fff' : text,
              border: `1px solid ${activeTab === tab ? accent : border}`,
              borderRadius: '8px',
              padding: '8px 16px',
              fontSize: '13px',
              fontWeight: '500',
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {tab}
          </button>
        ))}
        <button
          onClick={fetchComplianceData}
          style={{
            marginLeft: 'auto',
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
          <RefreshCw size={14} />
          Refresh
        </button>
      </div>

      {/* Content */}
      {loading ? (
        <div style={{ padding: '40px', textAlign: 'center', color: subtext }}>Loading compliance data...</div>
      ) : (
        <>
          {activeTab === 'overview' && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              {/* Compliance Rules */}
              <div style={{
                background: surface,
                border: `1px solid ${border}`,
                borderRadius: '12px',
                padding: '20px',
              }}>
                <h3 style={{ color: text, fontSize: '16px', fontWeight: '600', marginBottom: '16px' }}>Active Rules</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {complianceData.rules.slice(0, 5).map(rule => (
                    <div key={rule.id} style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '12px',
                      background: isDark ? '#1e293b' : '#f8fafc',
                      borderRadius: '8px',
                    }}>
                      <div>
                        <div style={{ color: text, fontSize: '14px', fontWeight: '500' }}>{rule.name}</div>
                        <div style={{ color: subtext, fontSize: '12px' }}>{rule.code}</div>
                      </div>
                      <span style={{
                        background: rule.severity === 'HIGH' ? '#ef444418' : rule.severity === 'MEDIUM' ? '#f59e0b18' : '#22c55e18',
                        color: rule.severity === 'HIGH' ? '#ef4444' : rule.severity === 'MEDIUM' ? '#f59e0b' : '#22c55e',
                        padding: '4px 10px',
                        borderRadius: '6px',
                        fontSize: '12px',
                        fontWeight: '600',
                      }}>
                        {rule.severity}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recent Reports */}
              <div style={{
                background: surface,
                border: `1px solid ${border}`,
                borderRadius: '12px',
                padding: '20px',
              }}>
                <h3 style={{ color: text, fontSize: '16px', fontWeight: '600', marginBottom: '16px' }}>Recent Reports</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  {complianceData.reports.slice(0, 5).map(report => (
                    <div key={report.id} style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '12px',
                      background: isDark ? '#1e293b' : '#f8fafc',
                      borderRadius: '8px',
                    }}>
                      <div>
                        <div style={{ color: text, fontSize: '14px', fontWeight: '500' }}>{report.title}</div>
                        <div style={{ color: subtext, fontSize: '12px' }}>{report.report_number}</div>
                      </div>
                      <span style={{
                        background: `${getReportStatusColor(report.status)}18`,
                        color: getReportStatusColor(report.status),
                        padding: '4px 10px',
                        borderRadius: '6px',
                        fontSize: '12px',
                        fontWeight: '600',
                      }}>
                        {report.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'rules' && (
            <div style={{
              background: surface,
              border: `1px solid ${border}`,
              borderRadius: '12px',
              overflow: 'hidden',
            }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ borderBottom: `1px solid ${border}` }}>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Code</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Name</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Type</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Severity</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {complianceData.rules.map(rule => (
                    <tr key={rule.id} style={{ borderBottom: `1px solid ${border}` }}>
                      <td style={{ padding: '14px 16px', color: text, fontSize: '13px', fontWeight: '500' }}>{rule.code}</td>
                      <td style={{ padding: '14px 16px', color: text, fontSize: '13px' }}>{rule.name}</td>
                      <td style={{ padding: '14px 16px', color: subtext, fontSize: '13px' }}>{rule.regulation_type}</td>
                      <td style={{ padding: '14px 16px' }}>
                        <span style={{
                          background: rule.severity === 'HIGH' ? '#ef444418' : rule.severity === 'MEDIUM' ? '#f59e0b18' : '#22c55e18',
                          color: rule.severity === 'HIGH' ? '#ef4444' : rule.severity === 'MEDIUM' ? '#f59e0b' : '#22c55e',
                          padding: '4px 10px',
                          borderRadius: '6px',
                          fontSize: '12px',
                          fontWeight: '600',
                        }}>
                          {rule.severity}
                        </span>
                      </td>
                      <td style={{ padding: '14px 16px' }}>
                        <span style={{
                          background: rule.is_active ? '#22c55e18' : '#64748b18',
                          color: rule.is_active ? '#22c55e' : '#64748b',
                          padding: '4px 10px',
                          borderRadius: '6px',
                          fontSize: '12px',
                          fontWeight: '600',
                        }}>
                          {rule.is_active ? 'Active' : 'Inactive'}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === 'checks' && (
            <div style={{
              background: surface,
              border: `1px solid ${border}`,
              borderRadius: '12px',
              overflow: 'hidden',
            }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ borderBottom: `1px solid ${border}` }}>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>ID</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Transaction</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Rule</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Status</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Score</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {complianceData.checks.map(check => (
                    <tr key={check.id} style={{ borderBottom: `1px solid ${border}` }}>
                      <td style={{ padding: '14px 16px', color: text, fontSize: '13px', fontWeight: '500' }}>#{check.id}</td>
                      <td style={{ padding: '14px 16px', color: text, fontSize: '13px' }}>{check.transaction_id || '-'}</td>
                      <td style={{ padding: '14px 16px', color: subtext, fontSize: '13px' }}>{check.rule_code || check.rule}</td>
                      <td style={{ padding: '14px 16px' }}>
                        <span style={{
                          background: `${getCheckStatusColor(check.status)}18`,
                          color: getCheckStatusColor(check.status),
                          padding: '4px 10px',
                          borderRadius: '6px',
                          fontSize: '12px',
                          fontWeight: '600',
                        }}>
                          {check.status}
                        </span>
                      </td>
                      <td style={{ padding: '14px 16px', color: text, fontSize: '13px' }}>{check.score}%</td>
                      <td style={{ padding: '14px 16px', color: subtext, fontSize: '13px' }}>
                        {new Date(check.checked_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === 'reports' && (
            <div style={{
              background: surface,
              border: `1px solid ${border}`,
              borderRadius: '12px',
              overflow: 'hidden',
            }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ borderBottom: `1px solid ${border}` }}>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Report #</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Title</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Type</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Period</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Status</th>
                    <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {complianceData.reports.map(report => (
                    <tr key={report.id} style={{ borderBottom: `1px solid ${border}` }}>
                      <td style={{ padding: '14px 16px', color: text, fontSize: '13px', fontWeight: '500' }}>{report.report_number}</td>
                      <td style={{ padding: '14px 16px', color: text, fontSize: '13px' }}>{report.title}</td>
                      <td style={{ padding: '14px 16px', color: subtext, fontSize: '13px' }}>{report.report_type}</td>
                      <td style={{ padding: '14px 16px', color: subtext, fontSize: '13px' }}>
                        {report.period_start} - {report.period_end}
                      </td>
                      <td style={{ padding: '14px 16px' }}>
                        <span style={{
                          background: `${getReportStatusColor(report.status)}18`,
                          color: getReportStatusColor(report.status),
                          padding: '4px 10px',
                          borderRadius: '6px',
                          fontSize: '12px',
                          fontWeight: '600',
                        }}>
                          {report.status}
                        </span>
                      </td>
                      <td style={{ padding: '14px 16px' }}>
                        <button style={{
                          background: 'transparent',
                          border: `1px solid ${border}`,
                          borderRadius: '6px',
                          padding: '6px 10px',
                          color: text,
                          fontSize: '12px',
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '4px',
                        }}>
                          <Eye size={12} />
                          View
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </PageLayout>
  );
};

export default ComplianceCenter;
