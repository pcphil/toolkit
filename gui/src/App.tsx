import { useState, useEffect } from "react";
import Base64Panel from "./components/Base64Panel";
import HasherPanel from "./components/HasherPanel";
import ConverterPanel from "./components/ConverterPanel";
import "./App.css";

const TABS = ["Base64", "Hash File", "Convert"] as const;
type Tab = (typeof TABS)[number];

export default function App() {
  const [tab, setTab] = useState<Tab>("Base64");
  const [serverOk, setServerOk] = useState<boolean | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/health")
      .then((r) => setServerOk(r.ok))
      .catch(() => setServerOk(false));
  }, []);

  return (
    <div className="app">
      <header className="app-header">
        <span className="app-title">Toolkit</span>
        <span
          className={`server-dot ${serverOk === true ? "ok" : serverOk === false ? "err" : "pending"}`}
          title={serverOk ? "Server online" : serverOk === false ? "Server offline" : "Connecting…"}
        />
      </header>

      <nav className="tabs">
        {TABS.map((t) => (
          <button
            key={t}
            className={`tab ${t === tab ? "active" : ""}`}
            onClick={() => setTab(t)}
          >
            {t}
          </button>
        ))}
      </nav>

      <main className="content">
        {tab === "Base64" && <Base64Panel />}
        {tab === "Hash File" && <HasherPanel />}
        {tab === "Convert" && <ConverterPanel />}
      </main>
    </div>
  );
}
