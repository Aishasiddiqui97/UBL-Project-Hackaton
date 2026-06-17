// src/data/mockData.js

export const stats = {
  totalTransactions: 10482,
  fraudAlerts: 143,
  highRiskAccounts: 57,
  openCases: 28,
};

export const recentTransactions = [
  { id: "TXN001", account: "AC-4821", amount: 15000, type: "Transfer", status: "Flagged", risk: "High", date: "2026-06-16" },
  { id: "TXN002", account: "AC-3302", amount: 500, type: "Deposit", status: "Clear", risk: "Low", date: "2026-06-16" },
  { id: "TXN003", account: "AC-9910", amount: 87000, type: "Withdrawal", status: "Flagged", risk: "High", date: "2026-06-15" },
  { id: "TXN004", account: "AC-1145", amount: 2300, type: "Transfer", status: "Under Review", risk: "Medium", date: "2026-06-15" },
  { id: "TXN005", account: "AC-7723", amount: 430, type: "Deposit", status: "Clear", risk: "Low", date: "2026-06-14" },
  { id: "TXN006", account: "AC-5581", amount: 62000, type: "Withdrawal", status: "Flagged", risk: "High", date: "2026-06-14" },
  { id: "TXN007", account: "AC-2290", amount: 1200, type: "Transfer", status: "Clear", risk: "Low", date: "2026-06-13" },
  { id: "TXN008", account: "AC-8834", amount: 34000, type: "Transfer", status: "Under Review", risk: "Medium", date: "2026-06-13" },
  { id: "TXN009", account: "AC-6612", amount: 9500, type: "Withdrawal", status: "Flagged", risk: "High", date: "2026-06-12" },
  { id: "TXN010", account: "AC-1190", amount: 750, type: "Deposit", status: "Clear", risk: "Low", date: "2026-06-12" },
  { id: "TXN011", account: "AC-3341", amount: 120000, type: "Transfer", status: "Flagged", risk: "High", date: "2026-06-11" },
  { id: "TXN012", account: "AC-7712", amount: 3300, type: "Transfer", status: "Under Review", risk: "Medium", date: "2026-06-11" },
];

export const fraudAlerts = [
  { id: "ALT001", account: "AC-4821", type: "Unusual Transfer", probability: 94, status: "Open", date: "2026-06-16" },
  { id: "ALT002", account: "AC-9910", type: "Large Withdrawal", probability: 88, status: "Open", date: "2026-06-15" },
  { id: "ALT003", account: "AC-5581", type: "Multiple Transfers", probability: 76, status: "In Progress", date: "2026-06-14" },
  { id: "ALT004", account: "AC-3341", type: "Suspicious Login", probability: 65, status: "Resolved", date: "2026-06-13" },
  { id: "ALT005", account: "AC-7712", type: "High Frequency", probability: 81, status: "Open", date: "2026-06-12" },
  { id: "ALT006", account: "AC-6612", type: "Night Transactions", probability: 72, status: "In Progress", date: "2026-06-12" },
  { id: "ALT007", account: "AC-1190", type: "Identity Mismatch", probability: 90, status: "Open", date: "2026-06-11" },
];

export const highRiskAccounts = [
  { id: "AC-4821", name: "John Mercer", riskScore: 92, transactions: 34, flagged: 8 },
  { id: "AC-9910", name: "Sara Malik", riskScore: 88, transactions: 21, flagged: 5 },
  { id: "AC-5581", name: "David Osei", riskScore: 81, transactions: 47, flagged: 6 },
  { id: "AC-7712", name: "Lena Kovac", riskScore: 78, transactions: 19, flagged: 4 },
  { id: "AC-3341", name: "Omar Farooq", riskScore: 74, transactions: 28, flagged: 3 },
  { id: "AC-6612", name: "Aisha Raza", riskScore: 85, transactions: 39, flagged: 7 },
  { id: "AC-1190", name: "Carlos Vega", riskScore: 91, transactions: 52, flagged: 9 },
];

export const openCases = [
  { id: "CASE001", title: "Large Fund Movement", account: "AC-4821", status: "Open", priority: "High", date: "2026-06-16" },
  { id: "CASE002", title: "Repeated Micro Transfers", account: "AC-9910", status: "In Progress", priority: "Medium", date: "2026-06-15" },
  { id: "CASE003", title: "Suspicious Withdrawal Pattern", account: "AC-5581", status: "Open", priority: "High", date: "2026-06-14" },
  { id: "CASE004", title: "Multiple Account Access", account: "AC-3341", status: "In Progress", priority: "Low", date: "2026-06-13" },
  { id: "CASE005", title: "Identity Fraud Suspected", account: "AC-1190", status: "Open", priority: "High", date: "2026-06-12" },
  { id: "CASE006", title: "Night Activity Pattern", account: "AC-6612", status: "In Progress", priority: "Medium", date: "2026-06-11" },
];

export const weeklyTransactions = [
  { day: "Mon", transactions: 1200, flagged: 18 },
  { day: "Tue", transactions: 1850, flagged: 24 },
  { day: "Wed", transactions: 1400, flagged: 15 },
  { day: "Thu", transactions: 2100, flagged: 32 },
  { day: "Fri", transactions: 1750, flagged: 27 },
  { day: "Sat", transactions: 980, flagged: 12 },
  { day: "Sun", transactions: 620, flagged: 8 },
];

export const monthlyTrends = [
  { month: "Jan", transactions: 8200, fraud: 98 },
  { month: "Feb", transactions: 7800, fraud: 85 },
  { month: "Mar", transactions: 9100, fraud: 112 },
  { month: "Apr", transactions: 9800, fraud: 120 },
  { month: "May", transactions: 10200, fraud: 135 },
  { month: "Jun", transactions: 10482, fraud: 143 },
];

export const riskDistribution = [
  { name: "Low Risk", value: 62 },
  { name: "Medium Risk", value: 25 },
  { name: "High Risk", value: 13 },
];

export const investigationNotes = [
  { id: 1, case: "CASE001", author: "Agent Harris", note: "Initial review completed. Flagging for senior analyst.", date: "2026-06-16" },
  { id: 2, case: "CASE001", author: "Sr. Analyst Khan", note: "Confirmed suspicious pattern. Escalating to investigation team.", date: "2026-06-16" },
  { id: 3, case: "CASE002", author: "Agent Harris", note: "Micro transfer pattern identified across 6 accounts.", date: "2026-06-15" },
  { id: 4, case: "CASE003", author: "Agent Reyes", note: "Withdrawal pattern flagged. Reviewing last 30 days.", date: "2026-06-14" },
  { id: 5, case: "CASE005", author: "Sr. Analyst Khan", note: "ID documents submitted don't match account holder.", date: "2026-06-12" },
];