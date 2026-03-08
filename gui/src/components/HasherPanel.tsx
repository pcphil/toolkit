import { useState } from "react";
import { hashFile, HashResult } from "../api";

const ALGORITHMS = ["md5", "sha1", "sha256", "sha512"];

export default function HasherPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [algo, setAlgo] = useState("sha256");
  const [result, setResult] = useState<HashResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const run = async () => {
    if (!file) return;
    setError("");
    setLoading(true);
    try {
      setResult(await hashFile(file, algo));
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <div className="field">
        <label>File</label>
        <input
          type="file"
          onChange={(e) => {
            setFile(e.target.files?.[0] ?? null);
            setResult(null);
          }}
        />
      </div>

      <div className="field">
        <label>Algorithm</label>
        <select value={algo} onChange={(e) => setAlgo(e.target.value)}>
          {ALGORITHMS.map((a) => (
            <option key={a} value={a}>
              {a.toUpperCase()}
            </option>
          ))}
        </select>
      </div>

      <div className="actions">
        <button onClick={run} disabled={!file || loading}>
          Hash file
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result-block">
          <div className="result-row">
            <span className="rl">File</span>
            <span>{result.filename}</span>
          </div>
          <div className="result-row">
            <span className="rl">Algorithm</span>
            <span>{result.algorithm.toUpperCase()}</span>
          </div>
          <div className="result-row digest-row">
            <span className="rl">Digest</span>
            <code>{result.digest}</code>
            <button
              className="secondary small"
              onClick={() => navigator.clipboard.writeText(result.digest)}
            >
              Copy
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
