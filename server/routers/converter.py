import csv
import io
import json

import yaml
from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import PlainTextResponse

SUPPORTED_PAIRS = {
    ("csv", "json"),
    ("json", "csv"),
    ("json", "yaml"),
    ("yaml", "json"),
    ("csv", "yaml"),
    ("yaml", "csv"),
}

router = APIRouter(prefix="/api/convert", tags=["convert"])


def _load(content: str, fmt: str):
    if fmt == "json":
        return json.loads(content)
    if fmt == "yaml":
        return yaml.safe_load(content)
    if fmt == "csv":
        return list(csv.DictReader(io.StringIO(content)))
    raise ValueError(f"Unknown format: {fmt}")


def _dump(data, fmt: str) -> str:
    if fmt == "json":
        return json.dumps(data, indent=2, ensure_ascii=False)
    if fmt == "yaml":
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)
    if fmt == "csv":
        if not isinstance(data, list) or not data:
            raise ValueError("CSV output requires a non-empty array of objects")
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return buf.getvalue()
    raise ValueError(f"Unknown format: {fmt}")


@router.post("/", response_class=PlainTextResponse)
async def convert(
    file: UploadFile = File(...),
    from_fmt: str = Query(..., description="Source format: csv | json | yaml"),
    to_fmt: str = Query(..., description="Target format: csv | json | yaml"),
):
    if (from_fmt, to_fmt) not in SUPPORTED_PAIRS:
        raise HTTPException(
            status_code=400,
            detail=f"Conversion {from_fmt} → {to_fmt} is not supported.",
        )

    content = (await file.read()).decode("utf-8")

    try:
        data = _load(content, from_fmt)
        result = _dump(data, to_fmt)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    media_map = {"json": "application/json", "yaml": "text/yaml", "csv": "text/csv"}
    return PlainTextResponse(content=result, media_type=media_map[to_fmt])
