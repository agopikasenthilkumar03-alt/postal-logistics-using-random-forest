import Header from "./components/Header.jsx";
import Sidebar from "./components/Sidebar.jsx";
import CustomerDashboard from "./pages/CustomerDashboard.jsx";
import StaffDashboard from "./pages/StaffDashboard.jsx";
import AdminDashboard from "./pages/AdminDashboard.jsx";

const App = () => {
  return (
    <div className="app-shell">
      <Header />
      <div className="content-wrapper">
        <Sidebar />
        <main className="main-content">
          <section className="panel">
            <CustomerDashboard />
          </section>
          <section className="panel">
            <StaffDashboard />
          </section>
          <section className="panel">
            <AdminDashboard />
          </section>
        </main>
      </div>
    </div>
  );
};

export default App;
