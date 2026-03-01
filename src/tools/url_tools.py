import requests


class UrlTools:

    @staticmethod
    def expand_url(short_url):
        """Follow redirects and return the final URL."""
        resp = requests.head(short_url, allow_redirects=True, timeout=10)
        final_url = resp.url
        print(f"Expanded: {short_url} -> {final_url}")
        return final_url

    @staticmethod
    def shorten_url(long_url, service="tinyurl"):
        """Shorten a URL using TinyURL's free API (no auth needed)."""
        if service != "tinyurl":
            raise ValueError(f"Unsupported service '{service}'. Currently only 'tinyurl' is supported.")

        api_url = f"https://tinyurl.com/api-create.php?url={long_url}"
        resp = requests.get(api_url, timeout=10)
        resp.raise_for_status()
        short_url = resp.text.strip()
        print(f"Shortened: {long_url} -> {short_url}")
        return short_url
