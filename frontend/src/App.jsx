import { useEffect, useState } from "react";

const apiUrl = import.meta.env.VITE_API_URL || "";

export default function App() {
  const [message, setMessage] = useState("Loading backend message...");

  useEffect(() => {
    fetch(`${apiUrl}/api/hello`)
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage("Backend unavailable"));
  }, []);

  return (
    <main className="app-shell">
      <section className="card" data-testid="app-card">
        <p className="eyebrow">React Frontend</p>
        <h1>Hello, world!</h1>
        <p>This React app is running on port 8566.</p>
        <p className="api-message" data-testid="api-message">
          {message}
        </p>
      </section>
    </main>
  );
}
