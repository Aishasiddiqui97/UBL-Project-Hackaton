import { useState } from "react";
import apiService from "../../services/api";

const CreateTransactionModal = ({ isOpen, onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    transaction_type: 'DEBIT',
    amount: '',
    account_number: '',
    description: '',
    location: 'Karachi'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [fraudAlert, setFraudAlert] = useState(null);

    const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setFraudAlert(null);
    
    if (!formData.amount || !formData.account_number || !formData.description) {
      setError('Please fill in all required fields');
      return;
    }
    
    if (parseFloat(formData.amount) < 0.01) {
      setError('Amount must be at least PKR 0.01');
      return;
    }

    setLoading(true);
    
    try {
      console.log('Creating transaction:', formData);
      const response = await apiService.createTransaction(formData);
      console.log('Transaction created:', response);
      
      // Check for fraud alert in response
      const transaction = response.data || response;
      if (transaction.fraud_reason) {
        setFraudAlert({
          reference: transaction.reference,
          amount: transaction.amount,
          reason: transaction.fraud_reason.details || transaction.fraud_reason.alert_type,
          probability: transaction.fraud_reason.probability
        });
      }
      
      // Reset form
      setFormData({
        transaction_type: 'DEBIT',
        amount: '',
        account_number: '',
        description: '',
        location: 'Karachi'
      });
      
      onSuccess();
      if (!fraudAlert) {
        onClose();
      }
    } catch (error) {
      console.error('Failed to create transaction:', error);
      setError(error.message || 'Failed to create transaction');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  if (!isOpen) return null;

  const modalStyle = {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    zIndex: 1000
  };

  const contentStyle = {
    background: '#1e293b',
    borderRadius: '12px',
    padding: '24px',
    width: '100%',
    maxWidth: '500px',
    border: '1px solid #334155'
  };

  const inputStyle = {
    width: '100%',
    padding: '12px',
    border: '1px solid #334155',
    borderRadius: '8px',
    background: '#0f172a',
    color: 'white',
    fontSize: '14px',
    outline: 'none',
    boxSizing: 'border-box'
  };

  const buttonStyle = {
    padding: '12px 24px',
    borderRadius: '8px',
    fontSize: '14px',
    fontWeight: '600',
    cursor: 'pointer',
    border: 'none'
  };

  return (
    <div style={modalStyle} onClick={onClose}>
      <div style={contentStyle} onClick={e => e.stopPropagation()}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h3 style={{ color: 'white', fontSize: '18px', margin: 0 }}>Create New Transaction</h3>
          <button 
            onClick={onClose}
            style={{ background: 'none', border: 'none', color: '#94a3b8', fontSize: '20px', cursor: 'pointer' }}
          >
            ×
          </button>
        </div>

        {error && (
          <div style={{ 
            background: 'rgba(239,68,68,0.1)', 
            border: '1px solid rgba(239,68,68,0.3)', 
            borderRadius: '8px', 
            padding: '12px', 
            marginBottom: '16px',
            color: '#f87171',
            fontSize: '14px'
          }}>
            {error}
          </div>
        )}

        {fraudAlert && (
          <div style={{ 
            background: 'rgba(239,68,68,0.15)', 
            border: '1px solid #ef4444', 
            borderRadius: '8px', 
            padding: '16px', 
            marginBottom: '16px',
            color: '#f87171'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <span style={{ fontSize: '20px' }}>🚨</span>
              <h4 style={{ margin: 0, fontSize: '16px', fontWeight: '700', color: '#ef4444' }}>FRAUD DETECTED!</h4>
            </div>
            <div style={{ fontSize: '14px', marginBottom: '8px', lineHeight: '1.5' }}>
              {fraudAlert.reason}
            </div>
            <div style={{ display: 'flex', gap: '16px', fontSize: '13px', color: '#fca5a5' }}>
              <span><strong>Reference ID:</strong> {fraudAlert.reference}</span>
              <span><strong>Amount:</strong> PKR {parseFloat(fraudAlert.amount).toLocaleString()}</span>
            </div>
            <div style={{ marginTop: '8px', fontSize: '12px', color: '#fca5a5' }}>
              Fraud Probability: {fraudAlert.probability}%
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', color: '#94a3b8', fontSize: '13px', marginBottom: '6px' }}>
              Transaction Type *
            </label>
            <select
              name="transaction_type"
              value={formData.transaction_type}
              onChange={handleChange}
              style={inputStyle}
            >
              <option value="DEBIT">Debit</option>
              <option value="CREDIT">Credit</option>
              <option value="TRANSFER">Transfer</option>
              <option value="PAYMENT">Payment</option>
            </select>
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', color: '#94a3b8', fontSize: '13px', marginBottom: '6px' }}>
              Amount (PKR) *
            </label>
            <input
              type="number"
              name="amount"
              value={formData.amount}
              onChange={handleChange}
              placeholder="Enter amount"
              min="0.01"
              step="0.01"
              style={inputStyle}
            />
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', color: '#94a3b8', fontSize: '13px', marginBottom: '6px' }}>
              Account Number *
            </label>
            <input
              type="text"
              name="account_number"
              value={formData.account_number}
              onChange={handleChange}
              placeholder="ACC-12345678"
              style={inputStyle}
            />
          </div>

          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', color: '#94a3b8', fontSize: '13px', marginBottom: '6px' }}>
              Location
            </label>
            <select
              name="location"
              value={formData.location}
              onChange={handleChange}
              style={inputStyle}
            >
              <option value="Karachi">Karachi</option>
              <option value="Lahore">Lahore</option>
              <option value="Islamabad">Islamabad</option>
              <option value="Faisalabad">Faisalabad</option>
              <option value="Rawalpindi">Rawalpindi</option>
              <option value="Peshawar">Peshawar</option>
              <option value="Quetta">Quetta</option>
            </select>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', color: '#94a3b8', fontSize: '13px', marginBottom: '6px' }}>
              Description *
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Enter transaction description"
              rows={3}
              style={inputStyle}
            />
          </div>

          <div style={{ display: 'flex', gap: '12px', justifyContent: 'flex-end' }}>
            <button
              type="button"
              onClick={onClose}
              style={{
                ...buttonStyle,
                background: '#334155',
                color: '#94a3b8'
              }}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              style={{
                ...buttonStyle,
                background: loading ? '#1e3a5f' : 'linear-gradient(135deg, #2563eb, #0891b2)',
                color: 'white'
              }}
            >
              {loading ? 'Creating...' : 'Create Transaction'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateTransactionModal;