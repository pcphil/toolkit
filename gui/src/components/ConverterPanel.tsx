import { useState } from "react";
import { convertFile } from "../api";

const FORMATS = ["csv", "json", "yaml"] as const;
type Fmt = (typeof FORMATS)[number];

const SUPPORTED = new Set([
  "csv→json", "json→csv",
  "json→yaml", "yaml→json",
  "csv→yaml", "yaml→csv",
]);

const EXT: Record<Fmt, string> = { csv: "csv", json: "json", yaml: "yaml" };

export default function ConverterPanel() {
  const [file, setFile] = useState<File | null>(null);
  const [fromFmt, setFromFmt] = useState<Fmt>("csv");
  const [toFmt, setToFmt] = useState<Fmt>("json");
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const pair = `${fromFmt}→${toFmt}`;
  const valid = fromFmt !== toFmt && SUPPORTED.has(pair);

  const run = async () => {
    if (!file || !valid) return;
    setError("");
    setLoading(true);
    try {
      setOutput(await convertFile(file, fromFmt, toFmt));
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  };

  const download = () => {
    const blob = new Blob([output], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `converted.${EXT[toFmt]}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="panel">
      <div className="field">
        <label>File</label>
        <input
          type="file"
          onChange={(e) => {
            setFile(e.target.files?.[0] ?? null);
            setOutput("");
          }}
        />
      </div>

      <div className="format-row">
        <div className="field">
          <label>From</label>
          <select value={fromFmt} onChange={(e) => setFromFmt(e.target.value as Fmt)}>
            {FORMATS.map((f) => <option key={f}>{f}</option>)}
          </select>
        </div>
        <span className="arrow">→</span>
        <div className="field">
          <label>To</label>
          <select value={toFmt} onChange={(e) => setToFmt(e.target.value as Fmt)}>
            {FORMATS.map((f) => <option key={f}>{f}</option>)}
          </select>
        </div>
      </div>

      {fromFmt === toFmt && <p className="warn">Source and target formats must differ.</p>}
      {fromFmt !== toFmt && !valid && <p className="warn">Unsupported pair: {pair}</p>}

      <div className="actions">
        <button onClick={run} disabled={!file || !valid || loading}>
          Convert
        </button>
        {output && (
          <>
            <button className="secondary" onClick={() => navigator.clipboard.writeText(output)}>
              Copy
            </button>
            <button className="secondary" onClick={download}>
              Download .{EXT[toFmt]}
            </button>
          </>
        )}
      </div>

      {error && <p className="error">{error}</p>}

      {output && (
        <div className="field">
          <label>Output</label>
          <textarea value={output} readOnly rows={10} />
        </div>
      )}
    </div>
  );
}
