import { useEffect, useState } from "react";

function ListPage() {
  const [controls, setControls] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulating API call
    setTimeout(() => {
      setControls([
        { id: 1, name: "Password Policy", status: "Active" },
        { id: 2, name: "Phishing Training", status: "Pending" }
      ]);
      setLoading(false);
    }, 2000);
  }, []);

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h1>Security Awareness Training Tracker</h1>
      <h2>Security Controls</h2>

      {controls.length === 0 ? (
        <p>No controls available</p>
      ) : (
        controls.map(control => (
          <div key={control.id}>
            <h3>{control.name}</h3>
            <p>Status: {control.status}</p>
          </div>
        ))
      )}
    </div>
  );
}

export default ListPage;