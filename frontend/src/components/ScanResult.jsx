// src/components/ScanResult.jsx
import React from "react";

const ScanResult = ({ results }) => {
  if (!results || results.length === 0) return null;

  return (
    <div className="mt-6 p-4 bg-white rounded-2xl shadow-md">
      <h2 className="text-xl font-semibold mb-4">📋 Scan Results</h2>
      <div className="overflow-auto">
        <table className="min-w-full text-sm text-left border">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-2 border">Target</th>
              <th className="p-2 border">Port</th>
              <th className="p-2 border">Protocol</th>
              <th className="p-2 border">Status</th>
              <th className="p-2 border">Banner</th>
            </tr>
          </thead>
          <tbody>
            {results.map((res, idx) => (
              <tr key={idx} className="hover:bg-gray-50">
                <td className="p-2 border">{res.target}</td>
                <td className="p-2 border">{res.port}</td>
                <td className="p-2 border uppercase">{res.protocol}</td>
                <td className="p-2 border text-green-600 font-medium">Open</td>
                <td className="p-2 border font-mono text-xs">{res.banner || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ScanResult;
