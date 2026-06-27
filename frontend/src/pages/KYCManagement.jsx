import { useState, useEffect } from 'react';
import PageLayout from "../components/layout/PageLayout";
import { useTheme } from "../context/ThemeContext";
import apiService from "../services/api";
import { Users, FileCheck, AlertTriangle, CheckCircle, Clock, Search, Filter, Eye, Check, X } from 'lucide-react';

const KYCManagement = () => {
  const { surface, border, text, subtext, accent, isDark } = useTheme();
  const [kycProfiles, setKycProfiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalProfiles: 0,
    pendingReview: 0,
    approved: 0,
    rejected: 0,
  });
  const [filters, setFilters] = useState({
    status: '',
    risk_rating: '',
  });
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchKYCData();
  }, []);

  const fetchKYCData = async () => {
    try {
      setLoading(true);
      const [profilesRes, statsRes] = await Promise.allSettled([
        apiService.apiCall('/kyc/profiles/'),
        apiService.apiCall('/kyc/profiles/stats/'),
      ]);

      const profiles = profilesRes.status === 'fulfilled' ? (profilesRes.value?.data || profilesRes.value || []) : [];
      const statsData = statsRes.status === 'fulfilled' ? (statsRes.value?.data || statsRes.value || {}) : {};

      setKycProfiles(Array.isArray(profiles) ? profiles : []);
      setStats({
        totalProfiles: statsData.total_profiles || profiles.length || 0,
        pendingReview: statsData.pending_review || 0,
        approved: statsData.approved || 0,
        rejected: statsData.rejected || 0,
      });
    } catch (err) {
      console.error('Failed to fetch KYC data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    const colors = {
      NOT_STARTED: '#64748b',
      IN_PROGRESS: '#38bdf8',
      PENDING_REVIEW: '#f59e0b',
      APPROVED: '#22c55e',
      REJECTED: '#ef4444',
      EXPIRED: '#fb923c',
      REQUIRES_UPDATE: '#a78bfa',
    };
    return colors[status] || '#64748b';
  };

  const getRiskColor = (risk) => {
    const colors = {
      LOW: '#22c55e',
      MEDIUM: '#f59e0b',
      HIGH: '#ef4444',
      PROHIBITED: '#dc2626',
    };
    return colors[risk] || '#64748b';
  };

  const handleApprove = async (profileId) => {
    try {
      await apiService.apiCall(`/kyc/profiles/${profileId}/review/`, {
        method: 'POST',
        body: JSON.stringify({
          status: 'APPROVED',
          review_notes: 'Approved via admin panel',
        }),
      });
      fetchKYCData();
    } catch (err) {
      console.error('Failed to approve profile:', err);
    }
  };

  const handleReject = async (profileId) => {
    try {
      await apiService.apiCall(`/kyc/profiles/${profileId}/review/`, {
        method: 'POST',
        body: JSON.stringify({
          status: 'REJECTED',
          rejection_reason: 'Does not meet KYC requirements',
        }),
      });
      fetchKYCData();
    } catch (err) {
      console.error('Failed to reject profile:', err);
    }
  };

  const filteredProfiles = kycProfiles.filter(profile => {
    if (filters.status && profile.status !== filters.status) return false;
    if (filters.risk_rating && profile.risk_rating !== filters.risk_rating) return false;
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      return (
        (profile.user_email && profile.user_email.toLowerCase().includes(searchLower)) ||
        (profile.full_name && profile.full_name.toLowerCase().includes(searchLower)) ||
        (profile.id_document_number && profile.id_document_number.toLowerCase().includes(searchLower))
      );
    }
    return true;
  });

  return (
    <PageLayout title="KYC Management" subtitle="Know Your Customer verification and compliance">
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
            <Users size={24} color="#38bdf8" />
          </div>
          <div>
            <div style={{ color: subtext, fontSize: '12px', marginBottom: '4px' }}>Total Profiles</div>
            <div style={{ color: text, fontSize: '24px', fontWeight: '700' }}>{stats.totalProfiles}</div>
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
            <div style={{ color: text, fontSize: '24px', fontWeight: '700' }}>{stats.pendingReview}</div>
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
            <div style={{ color: subtext, fontSize: '12px', marginBottom: '4px' }}>Approved</div>
            <div style={{ color: text, fontSize: '24px', fontWeight: '700' }}>{stats.approved}</div>
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
            <div style={{ color: subtext, fontSize: '12px', marginBottom: '4px' }}>Rejected</div>
            <div style={{ color: text, fontSize: '24px', fontWeight: '700' }}>{stats.rejected}</div>
          </div>
        </div>
      </div>

      {/* Search and Filters */}
      <div style={{
        display: 'flex',
        gap: '12px',
        marginBottom: '20px',
        alignItems: 'center',
      }}>
        <div style={{
          flex: 1,
          position: 'relative',
        }}>
          <Search size={18} color={subtext} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
          <input
            type="text"
            placeholder="Search by name, email, or document number..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              width: '100%',
              background: isDark ? '#1e293b' : '#f8fafc',
              border: `1px solid ${border}`,
              borderRadius: '8px',
              padding: '10px 12px 10px 40px',
              color: text,
              fontSize: '13px',
              outline: 'none',
            }}
          />
        </div>

        <select
          value={filters.status}
          onChange={(e) => setFilters({ ...filters, status: e.target.value })}
          style={{
            background: isDark ? '#1e293b' : '#f8fafc',
            border: `1px solid ${border}`,
            borderRadius: '8px',
            padding: '10px 12px',
            color: text,
            fontSize: '13px',
            outline: 'none',
          }}
        >
          <option value="">All Status</option>
          <option value="NOT_STARTED">Not Started</option>
          <option value="IN_PROGRESS">In Progress</option>
          <option value="PENDING_REVIEW">Pending Review</option>
          <option value="APPROVED">Approved</option>
          <option value="REJECTED">Rejected</option>
        </select>

        <select
          value={filters.risk_rating}
          onChange={(e) => setFilters({ ...filters, risk_rating: e.target.value })}
          style={{
            background: isDark ? '#1e293b' : '#f8fafc',
            border: `1px solid ${border}`,
            borderRadius: '8px',
            padding: '10px 12px',
            color: text,
            fontSize: '13px',
            outline: 'none',
          }}
        >
          <option value="">All Risk Levels</option>
          <option value="LOW">Low Risk</option>
          <option value="MEDIUM">Medium Risk</option>
          <option value="HIGH">High Risk</option>
          <option value="PROHIBITED">Prohibited</option>
        </select>
      </div>

      {/* KYC Profiles Table */}
      <div style={{
        background: surface,
        border: `1px solid ${border}`,
        borderRadius: '12px',
        overflow: 'hidden',
      }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ borderBottom: `1px solid ${border}` }}>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>User</th>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Full Name</th>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Nationality</th>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Status</th>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Risk Rating</th>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Documents</th>
              <th style={{ padding: '14px 16px', textAlign: 'left', color: subtext, fontSize: '12px', fontWeight: '600', textTransform: 'uppercase' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan="7" style={{ padding: '40px', textAlign: 'center', color: subtext }}>Loading KYC profiles...</td>
              </tr>
            ) : filteredProfiles.length === 0 ? (
              <tr>
                <td colSpan="7" style={{ padding: '40px', textAlign: 'center', color: subtext }}>No KYC profiles found</td>
              </tr>
            ) : (
              filteredProfiles.map((profile) => (
                <tr key={profile.id} style={{ borderBottom: `1px solid ${border}` }}>
                  <td style={{ padding: '14px 16px', color: text, fontSize: '13px', fontWeight: '500' }}>
                    {profile.user_email}
                  </td>
                  <td style={{ padding: '14px 16px', color: text, fontSize: '13px' }}>
                    {profile.full_name || '-'}
                  </td>
                  <td style={{ padding: '14px 16px', color: subtext, fontSize: '13px' }}>
                    {profile.nationality || '-'}
                  </td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{
                      background: `${getStatusColor(profile.status)}18`,
                      color: getStatusColor(profile.status),
                      padding: '4px 10px',
                      borderRadius: '6px',
                      fontSize: '12px',
                      fontWeight: '600',
                    }}>
                      {profile.status_display || profile.status}
                    </span>
                  </td>
                  <td style={{ padding: '14px 16px' }}>
                    <span style={{
                      background: `${getRiskColor(profile.risk_rating)}18`,
                      color: getRiskColor(profile.risk_rating),
                      padding: '4px 10px',
                      borderRadius: '6px',
                      fontSize: '12px',
                      fontWeight: '600',
                    }}>
                      {profile.risk_rating_display || profile.risk_rating}
                    </span>
                  </td>
                  <td style={{ padding: '14px 16px', color: text, fontSize: '13px' }}>
                    {profile.document_count || 0} files
                  </td>
                  <td style={{ padding: '14px 16px' }}>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <button
                        onClick={() => window.open(`/kyc/${profile.id}`, '_blank')}
                        style={{
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
                        }}
                      >
                        <Eye size={12} />
                        View
                      </button>
                      {profile.status === 'PENDING_REVIEW' && (
                        <>
                          <button
                            onClick={() => handleApprove(profile.id)}
                            style={{
                              background: '#22c55e18',
                              border: 'none',
                              borderRadius: '6px',
                              padding: '6px 10px',
                              color: '#22c55e',
                              fontSize: '12px',
                              cursor: 'pointer',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '4px',
                            }}
                          >
                            <Check size={12} />
                            Approve
                          </button>
                          <button
                            onClick={() => handleReject(profile.id)}
                            style={{
                              background: '#ef444418',
                              border: 'none',
                              borderRadius: '6px',
                              padding: '6px 10px',
                              color: '#ef4444',
                              fontSize: '12px',
                              cursor: 'pointer',
                              display: 'flex',
                              alignItems: 'center',
                              gap: '4px',
                            }}
                          >
                            <X size={12} />
                            Reject
                          </button>
                        </>
                      )}
                    </div>
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

export default KYCManagement;
