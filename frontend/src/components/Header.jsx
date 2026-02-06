const Header = () => {
  return (
    <header className="header">
      <div>
        <p className="header-title">India Post Internal Dashboard</p>
        <p className="header-subtitle">Weather-Based Post Delay Prediction and SMS Notification System</p>
      </div>
      <div className="header-actions">
        <span className="badge">Admin Control Center</span>
        <button className="primary-button">Sync Weather</button>
      </div>
    </header>
  );
};

export default Header;
