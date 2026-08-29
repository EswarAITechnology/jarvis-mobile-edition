import requests


def check_website(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "JARVIS-Web-Checker/1.0"
            }
        )

        return {
            "success": True,
            "url": url,
            "status_code": response.status_code,
            "status": "online" if response.ok else "error",
            "content_type": response.headers.get(
                "Content-Type",
                "unknown"
            )
        }

    except requests.RequestException as error:
        return {
            "success": False,
            "url": url,
            "status": "offline",
            "error": str(error)
        }