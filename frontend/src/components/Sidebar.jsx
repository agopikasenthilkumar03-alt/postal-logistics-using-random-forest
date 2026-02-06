const Sidebar = () => {
  return (
    <aside className="sidebar">
      <h2 className="sidebar-title">Navigation</h2>
      <nav>
        <ul>
          <li>Customer Tracking</li>
          <li>Postal Staff View</li>
          <li>Admin Approval</li>
          <li>Weather Monitoring</li>
          <li>SMS Notifications</li>
        </ul>
      </nav>
      <div className="sidebar-card">
        <p className="sidebar-card-title">System Status</p>
        <p className="sidebar-card-text">Forecast ingestion: Active</p>
        <p className="sidebar-card-text">ML Model: Random Forest (v1.0)</p>
      </div>
    </aside>
  );
};

export default Sidebar;
