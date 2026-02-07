const AdminDashboard = () => {
  const approvals = [
    {
      id: "PRED-901",
      postId: "INP-DEL-2045",
      route: "New Delhi GPO → Kolkata GPO",
      delay: 2,
      risk: "High rainfall",
      model: "RF v1.0"
    },
    {
      id: "PRED-918",
      postId: "INP-HYD-1129",
      route: "Hyderabad GPO → Pune GPO",
      delay: 1,
      risk: "Flood risk medium",
      model: "RF v1.0"
    }
  ];

  return (
    <div>
      <div className="panel-header">
        <h3>Admin Approval Panel</h3>
        <div className="filters">
          <input placeholder="Search Prediction ID" />
          <button className="secondary-button">View Approved</button>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Prediction ID</th>
            <th>Post ID</th>
            <th>Route</th>
            <th>Predicted Delay</th>
            <th>Weather Risk</th>
            <th>Model</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {approvals.map((approval) => (
            <tr key={approval.id}>
              <td>{approval.id}</td>
              <td>{approval.postId}</td>
              <td>{approval.route}</td>
              <td>{approval.delay} days</td>
              <td>{approval.risk}</td>
              <td>{approval.model}</td>
              <td>
                <div className="action-buttons">
                  <button className="primary-button">Approve</button>
                  <button className="ghost-button">Reject</button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboard;
