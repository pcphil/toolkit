import { useState } from "react";
import { base64Encode, base64Decode } from "../api";

export default function Base64Panel() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const run = async (op: "encode" | "decode") => {
    setError("");
    setLoading(true);
    try {
      setOutput(op === "encode" ? await base64Encode(input) : await base64Decode(input));
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <div className="field">
        <label>Input</label>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Paste text or base64 string here…"
          rows={6}
        />
      </div>

      <div className="actions">
        <button onClick={() => run("encode")} disabled={loading || !input.trim()}>
          Encode →
        </button>
        <button onClick={() => run("decode")} disabled={loading || !input.trim()}>
          Decode →
        </button>
        {output && (
          <button className="secondary" onClick={() => navigator.clipboard.writeText(output)}>
            Copy result
          </button>
        )}
      </div>

      {error && <p className="error">{error}</p>}

      {output && (
        <div className="field">
          <label>Output</label>
          <textarea value={output} readOnly rows={6} />
        </div>
      )}
    </div>
  );
}
