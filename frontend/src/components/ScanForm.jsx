import React, { useState } from "react";

function ScanForm() {
  const [targets, setTargets] = useState("localhost");
  const [results, setResults] = useState(null);

  // const handleSubmit = async (e) => {
  //   e.preventDefault();

  //   try {
  //     const response = await fetch("http://127.0.0.1:8000/scan", {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //       body: JSON.stringify({
  //         targets: targets.split(","),
  //         profile: "quick",
  //         udp: false,
  //       }),
  //     });

  //     const data = await response.json();
  //     setResults(data.results); // ✅ use .results
  //   } catch (error) {
  //     console.error("Error:", error);
  //   }
  // };

  const handleSubmit = async (e) => {
  e.preventDefault();

  try {
    const response = await fetch("http://127.0.0.1:8000/scan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        targets: targets.split(","),
        profile: "quick",
        udp: false,
      }),
    });

    const data = await response.json();
    console.log("SCAN RESPONSE:", data);


    // ✅ Handle both cases: { results: [...] } or just [...]
    if (Array.isArray(data)) {
      setResults(data);
    } else if (data.results) {
      setResults(data.results);
    } else {
      setResults([]); // fallback
    }
  } catch (error) {
    console.error("Error:", error);
  }
};


  return (
    <div style={{ padding: "20px" }}>
      <h2>PortProbe Scanner</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={targets}
          onChange={(e) => setTargets(e.target.value)}
          placeholder="Enter target(s), comma-separated"
        />
        <button type="submit">Scan</button>
      </form>

      {results && (
        <table border="1" cellPadding="8" style={{ marginTop: "20px" }}>
          <thead>
            <tr>
              <th>IP</th>
              <th>Port</th>
              <th>Protocol</th>
              <th>Service</th>
              <th>Banner</th>
            </tr>
          </thead>
          <tbody>
            {results.map((r, idx) => (
              <tr key={idx}>
                <td>{r.ip}</td>
                <td>{r.port}</td>
                <td>{r.protocol}</td>
                <td>{r.service}</td>
                <td>{r.banner || "N/A"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ScanForm;
