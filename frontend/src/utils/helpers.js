export const formatPrice = (price) => {
  if (!price && price !== 0) return 'N/A';
  return `₹${price.toLocaleString('en-IN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
};

export const calculatePriceChange = (oldPrice, newPrice) => {
  if (!oldPrice || oldPrice === 0) return 0;
  return (((newPrice - oldPrice) / oldPrice) * 100).toFixed(2);
};

export const getPriceChangeColor = (changePercent) => {
  if (changePercent < -5) return 'text-green-600'; // Price dropped significantly
  if (changePercent < 0) return 'text-green-500'; // Small price drop
  if (changePercent > 0) return 'text-red-500'; // Price increase
  return 'text-gray-500'; // No change
};

export const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const truncateText = (text, maxLength = 50) => {
  if (!text) return '';
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
};

export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};
