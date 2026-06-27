import { useState, useEffect, useCallback } from 'react';
import apiService from '../services/api';

export const useOperationalData = (interval = 30000) => {
  const [data, setData] = useState({
    transactions: [],
    alerts: [],
    cases: [],
    stats: {
      totalTransactions: 0,
      fraudAlerts: 0,
      highRiskAccounts: 0,
      openCases: 0,
      pendingReviews: 0,
      resolvedToday: 0,
    },
    loading: true,
    error: null,
    lastUpdated: null,
  });

  const fetchOperationalData = useCallback(async () => {
    try {
      const [transactionsRes, alertsRes, casesRes, fraudStatsRes] = await Promise.allSettled([
        apiService.getTransactions(),
        apiService.getFraudAlerts(),
        apiService.getCases(),
        apiService.getFraudStats(),
      ]);

      const transactions = transactionsRes.status === 'fulfilled' ? (transactionsRes.value?.data || transactionsRes.value || []) : [];
      const alerts = alertsRes.status === 'fulfilled' ? (alertsRes.value?.data || alertsRes.value || []) : [];
      const cases = casesRes.status === 'fulfilled' ? (casesRes.value?.data || casesRes.value || []) : [];
      const fraudStats = fraudStatsRes.status === 'fulfilled' ? (fraudStatsRes.value?.data || fraudStatsRes.value || {}) : {};

      setData({
        transactions: Array.isArray(transactions) ? transactions : [],
        alerts: Array.isArray(alerts) ? alerts : [],
        cases: Array.isArray(cases) ? cases : [],
        stats: {
          totalTransactions: fraudStats.total_transactions || transactions.length || 0,
          fraudAlerts: fraudStats.status_breakdown?.flagged || alerts.filter(a => a.status === 'OPEN').length || 0,
          highRiskAccounts: fraudStats.risk_breakdown?.high_risk || 0,
          openCases: cases.filter(c => c.status !== 'CLOSED' && c.status !== 'RESOLVED').length || 0,
          pendingReviews: fraudStats.status_breakdown?.under_review || 0,
          resolvedToday: fraudStats.status_breakdown?.clear || 0,
        },
        loading: false,
        error: null,
        lastUpdated: new Date().toISOString(),
      });
    } catch (error) {
      console.error('Failed to fetch operational data:', error);
      setData(prev => ({
        ...prev,
        loading: false,
        error: error.message,
      }));
    }
  }, []);

  useEffect(() => {
    fetchOperationalData();
    const intervalId = setInterval(fetchOperationalData, interval);
    return () => clearInterval(intervalId);
  }, [fetchOperationalData, interval]);

  const refresh = useCallback(() => {
    setData(prev => ({ ...prev, loading: true }));
    fetchOperationalData();
  }, [fetchOperationalData]);

  return { ...data, refresh };
};

export default useOperationalData;
