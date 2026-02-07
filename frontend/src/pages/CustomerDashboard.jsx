const CustomerDashboard = () => {
  const posts = [
    {
      postId: "INP-DEL-2045",
      route: "New Delhi GPO → Kolkata GPO",
      status: "In Transit",
      delay: "2 days (Pending approval)",
      updated: "10 Sep 2024, 09:30"
    },
    {
      postId: "INP-MUM-3872",
      route: "Mumbai GPO → Chennai GPO",
      status: "Dispatched",
      delay: "No delay predicted",
      updated: "10 Sep 2024, 08:20"
    }
  ];

  return (
    <div>
      <div className="panel-header">
        <h3>Customer Dashboard</h3>
        <div className="filters">
          <input placeholder="Search Post ID" />
          <select>
            <option>All Status</option>
            <option>Booked</option>
            <option>In Transit</option>
            <option>Delivered</option>
          </select>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th>Post ID</th>
            <th>Route</th>
            <th>Current Status</th>
            <th>Delay Status</th>
            <th>Last Update</th>
          </tr>
        </thead>
        <tbody>
          {posts.map((post) => (
            <tr key={post.postId}>
              <td>{post.postId}</td>
              <td>{post.route}</td>
              <td>{post.status}</td>
              <td>{post.delay}</td>
              <td>{post.updated}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CustomerDashboard;
