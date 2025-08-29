import { useState } from "react";
import "./App.css";
import Loader from "./components/Loader";
import ShadowScanTitle from "./components/Title";

function App() {
  const [targets, setTargets] = useState("");
  const [profile, setProfile] = useState("quick");
  const [udp, setUdp] = useState(false);
  const [verbose, setVerbose] = useState(false);
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleScan = async () => {
    setLoading(true);
    setResults({});
    setError("");
    try {
      const response = await fetch("http://127.0.0.1:8000/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          targets: targets.split(",").map((t) => t.trim()),
          profile,
          udp,
          verbose,
        }),
      });

      if (!response.ok) throw new Error("Failed to fetch");

      const data = await response.json();
      setResults(data.results);
    } catch (err) {
      console.error(err);
      setError("Something went wrong while scanning.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App" style={{fontFamily: "Arial" }}>
    <div className="header">
      {/* <h1 className="title">🔍 PortProbe Scanner</h1> */}
      <ShadowScanTitle/>

      <div style={{ marginBottom: "10px" }}>
        <input
         className="userinput"
          type="text"
          placeholder="Targets (comma-separated)"
          value={targets}
          onChange={(e) => setTargets(e.target.value)}
          
        />
        </div >
        <div className="boxes" style={{ marginTop: "10px" }}>
        <select value={profile} onChange={(e) => setProfile(e.target.value)}>
          <option value="quick">Quick</option>
          <option value="full">Full</option>
        </select>
        <label style={{ marginLeft: "10px" }}>
          <input
            type="checkbox"
            checked={udp}
            onChange={(e) => setUdp(e.target.checked)}
          />
          Enable UDP
        </label> 
        <label style={{ marginLeft: "10px" }}>
          <input
            type="checkbox"
            checked={verbose}
            onChange={(e) => setVerbose(e.target.checked)}
          />
          Verbose
        </label>
        {/* <button onClick={handleScan} style={{ marginLeft: "10px" }}>
          Scan
        </button> */}
        <button onClick={handleScan} disabled={loading}>
        {loading ? "Scanning..." : "Start Scan"}
      </button>
      </div>
      </div>

       {/* Show Loader while scanning */}
      {loading && <Loader />}
      {error && <p style={{ color: "red" }}>❌ {error}</p>}

      {Object.keys(results).map((target) => (
        <div className="result" key={target} style={{ marginBottom: "20px" }}>
          <h3>📍 Target: {target}</h3>
          {results[target][0].status === "no open ports found" ? (
            <p>No open ports found</p>
          ) : (
            <table border="1" cellPadding="5" cellSpacing="0">
              <thead>
                <tr>
                  <th>IP</th>
                  <th>Port</th>
                  <th>Protocol</th>
                  <th>Status</th>
                  <th>Service</th>
                  <th>Banner</th>
                </tr>
              </thead>
              <tbody>
                {results[target].map((res, idx) => (
                  <tr key={idx}>
                    <td>{res.ip}</td>
                    <td>{res.port}</td>
                    <td>{res.protocol}</td>
                    <td>{res.status}</td>
                    <td>{res.service || "N/A"}</td>
                    <td>{res.banner || "N/A"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      ))}

      {/* Bottom tagline */}
      <div className="app-footer">
        <p className="tagline">Silent scanning, full control.</p>
      </div>
    </div>
  );
}

export default App;
