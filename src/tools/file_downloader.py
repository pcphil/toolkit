import os
from urllib.parse import unquote, urlparse

import requests
from tqdm import tqdm


class FileDownloader:

    @staticmethod
    def _get_unique_path(path):
        if not os.path.exists(path):
            return path
        base, ext = os.path.splitext(path)
        counter = 1
        new_path = f"{base}_{counter}{ext}"
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base}_{counter}{ext}"
        return new_path

    @staticmethod
    def _detect_filename(url, response):
        """Try to get filename from Content-Disposition header, then fall back to URL path."""
        cd = response.headers.get("Content-Disposition", "")
        if "filename=" in cd:
            parts = cd.split("filename=")
            return parts[1].strip().strip('"').strip("'")

        path = urlparse(url).path
        name = os.path.basename(unquote(path))
        return name if name else "download"

    @staticmethod
    def download(url, output_path="output/", filename=None):
        """
        Download a file with a progress bar.

        Args:
            url: URL to download.
            output_path: Directory or full file path for the download.
            filename: Override the auto-detected filename.
        """
        os.makedirs(output_path if os.path.isdir(output_path) or output_path.endswith("/") else os.path.dirname(output_path) or ".", exist_ok=True)

        resp = requests.get(url, stream=True, timeout=30)
        resp.raise_for_status()

        if os.path.isdir(output_path) or output_path.endswith("/"):
            os.makedirs(output_path, exist_ok=True)
            name = filename or FileDownloader._detect_filename(url, resp)
            dest = os.path.join(output_path, name)
        else:
            dest = output_path

        dest = FileDownloader._get_unique_path(dest)
        total = int(resp.headers.get("Content-Length", 0))

        with open(dest, "wb") as f, tqdm(
            total=total, unit="B", unit_scale=True, desc=os.path.basename(dest), disable=total == 0
        ) as bar:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))

        print(f"Downloaded to '{dest}'")
        return dest

    @staticmethod
    def download_batch(urls, output_path="output/"):
        """Download multiple files sequentially."""
        results = []
        for url in urls:
            path = FileDownloader.download(url, output_path=output_path)
            results.append(path)
        return results
