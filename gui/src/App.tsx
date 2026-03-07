import { useState, useEffect } from "react";
import "./App.css";

const API = "http://localhost:8000";

type ServerStatus = "checking" | "ok" | "error";

function StatusBadge({ status }: { status: ServerStatus }) {
  const map: Record<ServerStatus, { label: string; color: string }> = {
    checking: { label: "Connecting…", color: "#888" },
    ok:       { label: "Server online", color: "#4caf50" },
    error:    { label: "Server offline", color: "#f44336" },
  };
  const { label, color } = map[status];
  return <span style={{ color, fontWeight: 600 }}>{label}</span>;
}

export default function App() {
  const [status, setStatus] = useState<ServerStatus>("checking");

  useEffect(() => {
    fetch(`${API}/health`)
      .then((r) => r.json())
      .then(() => setStatus("ok"))
      .catch(() => setStatus("error"));
  }, []);

  return (
    <main className="container">
      <h1>Toolkit</h1>
      <p className="status-line">
        <StatusBadge status={status} />
      </p>
      <p className="hint">Phase 1 — skeleton complete. Tools coming next.</p>
    </main>
  );
}
