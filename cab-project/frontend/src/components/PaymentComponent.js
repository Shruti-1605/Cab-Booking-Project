import React, { useState, useEffect } from 'react';
import { paymentAPI } from '../services/api';

const PaymentComponent = ({ rideId, amount, onPaymentSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [paymentMethods, setPaymentMethods] = useState([
    { id: 'card', name: 'Credit/Debit Card', icon: '💳' },
    { id: 'upi', name: 'UPI', icon: '📱' },
    { id: 'wallet', name: 'Wallet', icon: '💰' },
    { id: 'cash', name: 'Cash', icon: '💵' }
  ]);
  const [selectedMethod, setSelectedMethod] = useState('card');
  const [cardDetails, setCardDetails] = useState({
    number: '',
    expiry: '',
    cvv: '',
    name: ''
  });

  const handlePayment = async () => {
    setLoading(true);
    try {
      if (selectedMethod === 'cash') {
        // For cash payment, just mark as pending
        setTimeout(() => {
          onPaymentSuccess({ method: 'cash', status: 'pending' });
        }, 1000);
        return;
      }

      // For demo - simulate payment processing without API call
      setTimeout(() => {
        onPaymentSuccess({ 
          method: selectedMethod, 
          status: 'completed',
          transaction_id: `txn_${Date.now()}`
        });
      }, 2000);

    } catch (error) {
      alert('Payment failed: ' + (error.response?.data?.detail || 'Unknown error'));
    }
    setLoading(false);
  };

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-bold mb-4">Payment</h3>
      
      <div className="mb-4 p-3 bg-gray-50 rounded">
        <p className="text-lg font-semibold">Amount: ₹{amount}</p>
      </div>

      <div className="mb-4">
        <h4 className="font-medium mb-2">Select Payment Method</h4>
        <div className="space-y-2">
          {paymentMethods.map(method => (
            <label key={method.id} className="flex items-center p-3 border rounded cursor-pointer hover:bg-gray-50">
              <input
                type="radio"
                name="paymentMethod"
                value={method.id}
                checked={selectedMethod === method.id}
                onChange={(e) => setSelectedMethod(e.target.value)}
                className="mr-3"
              />
              <span className="mr-2">{method.icon}</span>
              <span>{method.name}</span>
            </label>
          ))}
        </div>
      </div>

      {selectedMethod === 'card' && (
        <div className="mb-4 space-y-3">
          <input
            type="text"
            placeholder="Card Number"
            className="w-full p-3 border rounded"
            value={cardDetails.number}
            onChange={(e) => setCardDetails({...cardDetails, number: e.target.value})}
          />
          <div className="grid grid-cols-2 gap-3">
            <input
              type="text"
              placeholder="MM/YY"
              className="p-3 border rounded"
              value={cardDetails.expiry}
              onChange={(e) => setCardDetails({...cardDetails, expiry: e.target.value})}
            />
            <input
              type="text"
              placeholder="CVV"
              className="p-3 border rounded"
              value={cardDetails.cvv}
              onChange={(e) => setCardDetails({...cardDetails, cvv: e.target.value})}
            />
          </div>
          <input
            type="text"
            placeholder="Cardholder Name"
            className="w-full p-3 border rounded"
            value={cardDetails.name}
            onChange={(e) => setCardDetails({...cardDetails, name: e.target.value})}
          />
        </div>
      )}

      {selectedMethod === 'upi' && (
        <div className="mb-4">
          <input
            type="text"
            placeholder="UPI ID (e.g., user@paytm)"
            className="w-full p-3 border rounded"
          />
        </div>
      )}

      <button
        onClick={handlePayment}
        disabled={loading}
        className="w-full bg-green-500 text-white p-3 rounded hover:bg-green-600 disabled:bg-gray-400"
      >
        {loading ? 'Processing...' : `Pay ₹${amount}`}
      </button>
    </div>
  );
};

export default PaymentComponent;