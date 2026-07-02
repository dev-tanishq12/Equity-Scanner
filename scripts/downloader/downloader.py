import time
from pathlib import Path
from urllib import response

import requests

from config import (
    CONNECT_TIMEOUT,
    READ_TIMEOUT,
    MAX_RETRIES,
    REQUEST_DELAY,
)


class NSEDownloader:

    def __init__(self):
        self.create_session()

    def create_session(self):
        """
        Create a fresh HTTP session.
        """

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0 Safari/537.36",

            "Referer":
                "https://www.nseindia.com/",

            "Accept":
                "text/csv,*/*",

            "Connection":
                "keep-alive"
        })

    def download(self, url: str, destination: Path):

        # Already downloaded
        if destination.exists():
            return "EXISTS"

        for attempt in range(MAX_RETRIES):

            try:

                response = self.session.get(
                    url,
                    timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
                )

                # Success
                if response.status_code == 200:

                    content_type = response.headers.get("Content-Type", "")

                    if "text/csv" not in content_type and "application" not in content_type:
                        return "FAILED"

                    destination.write_bytes(response.content)

                    time.sleep(REQUEST_DELAY)

                    return "DOWNLOADED"

                # NSE Holiday / Missing file
                elif response.status_code == 404:

                    return "HOLIDAY"

                # Forbidden
                elif response.status_code == 403:

                    # Create a fresh session
                    self.create_session()

                # Temporary server issue
                elif response.status_code >= 500:

                    pass

            except requests.exceptions.ConnectTimeout:
                pass

            except requests.exceptions.ReadTimeout:
                pass

            except requests.exceptions.ConnectionError:
                pass

            except requests.exceptions.SSLError:
                pass

            except requests.exceptions.RequestException:
                pass

            # Exponential backoff
            time.sleep(2 ** attempt)

        return "FAILED"