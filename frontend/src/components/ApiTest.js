import React, { useEffect, useState } from "react";
import axios from "axios";

const ApiTest = () => {
  const [status, setStatus] = useState("Testing API connection...");
  const [error, setError] = useState(null);

  useEffect(() => {
    const testApi = async () => {
      // Try multiple ports
      const ports = [5000, 4000, 3001];

      for (const port of ports) {
        try {
          setStatus(
            `Trying to connect to http://localhost:${port}/api/test...`
          );

          // Test the API endpoint
          const response = await axios.get(
            `http://localhost:${port}/api/test`,
            {
              withCredentials: true,
              timeout: 3000, // Add timeout to avoid long waits
            }
          );

          setStatus(
            `Success! Connected to port ${port}. Response: ${JSON.stringify(
              response.data
            )}`
          );

          // Update axios default baseURL if we found a working port
          if (axios.defaults.baseURL !== `http://localhost:${port}`) {
            console.log(`Updating axios baseURL to http://localhost:${port}`);
            axios.defaults.baseURL = `http://localhost:${port}`;
          }

          return; // Exit the loop if successful
        } catch (err) {
          console.error(`Failed to connect to port ${port}:`, err.message);
          // Continue to next port
        }
      }

      // If we get here, all ports failed
      setError(
        `Failed to connect to backend on ports ${ports.join(
          ", "
        )}. Please check if your backend server is running.`
      );
    };

    testApi();
  }, []);

  return (
    <div style={{ margin: "20px", padding: "20px", border: "1px solid #ccc" }}>
      <h2>API Connection Test</h2>
      <div style={{ whiteSpace: "pre-wrap" }}>
        <strong>Status:</strong> {status}
      </div>
      {error && (
        <div
          style={{ color: "red", marginTop: "10px", whiteSpace: "pre-wrap" }}
        >
          {error}
        </div>
      )}
    </div>
  );
};

export default ApiTest;
