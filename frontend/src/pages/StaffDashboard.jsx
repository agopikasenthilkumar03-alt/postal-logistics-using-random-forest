const StaffDashboard = () => {
  const officePosts = [
    {
      office: "Kolkata GPO",
      total: 128,
      delayed: 16,
      weather: "Heavy rain"
    },
    {
      office: "Chennai GPO",
      total: 94,
      delayed: 8,
      weather: "Moderate wind"
    },
    {
      office: "Bengaluru GPO",
      total: 77,
      delayed: 5,
      weather: "Clear"
    }
  ];

  return (
    <div>
      <div className="panel-header">
        <h3>Postal Staff Dashboard</h3>
        <div className="filters">
          <input placeholder="Filter by Post Office" />
          <select>
            <option>All Offices</option>
            <option>North Zone</option>
            <option>South Zone</option>
            <option>East Zone</option>
            <option>West Zone</option>
          </select>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Post Office</th>
            <th>Total Posts</th>
            <th>Posts with Delay Risk</th>
            <th>Weather Summary</th>
          </tr>
        </thead>
        <tbody>
          {officePosts.map((post) => (
            <tr key={post.office}>
              <td>{post.office}</td>
              <td>{post.total}</td>
              <td>{post.delayed}</td>
              <td>{post.weather}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StaffDashboard;
