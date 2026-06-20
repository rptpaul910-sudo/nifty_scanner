import React from 'react';

const Loader = ({ text = 'Loading market data...' }) => {
  return (
    <div className="loader-container">
      <div className="loader"></div>
      <p className="loader-text">{text}</p>
    </div>
  );
};

export default Loader;
