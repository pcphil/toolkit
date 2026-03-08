const API = "http://localhost:8000";

async function check(r: Response) {
  if (!r.ok) throw new Error(await r.text());
  return r;
}

export async function base64Encode(text: string): Promise<string> {
  const r = await check(
    await fetch(`${API}/api/base64/encode`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    })
  );
  return (await r.json()).result;
}

export async function base64Decode(text: string): Promise<string> {
  const r = await check(
    await fetch(`${API}/api/base64/decode`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    })
  );
  return (await r.json()).result;
}

export interface HashResult {
  filename: string;
  algorithm: string;
  digest: string;
}

export async function hashFile(file: File, algorithm: string): Promise<HashResult> {
  const fd = new FormData();
  fd.append("file", file);
  fd.append("algorithm", algorithm);
  const r = await check(await fetch(`${API}/api/hash/`, { method: "POST", body: fd }));
  return r.json();
}

export async function convertFile(file: File, fromFmt: string, toFmt: string): Promise<string> {
  const fd = new FormData();
  fd.append("file", file);
  const r = await check(
    await fetch(`${API}/api/convert/?from_fmt=${fromFmt}&to_fmt=${toFmt}`, {
      method: "POST",
      body: fd,
    })
  );
  return r.text();
}
