import time
from pathlib import Path

import requests

from scripts.config import (
    CONNECT_TIMEOUT,
    READ_TIMEOUT,
    MAX_RETRIES,
    REQUEST_DELAY,
)

from .validator import CSVValidator


class NSEDownloader:

    def __init__(self):

        self.create_session()

    def create_session(self):

        self.session = requests.Session()

        self.session.headers.update({

            "User-Agent":
                "Mozilla/5.0",

            "Referer":
                "https://www.nseindia.com/",

            "Accept":
                "text/csv,*/*"

        })

    def download(
        self,
        url,
        destination: Path
    ):

        if destination.exists():

            return "EXISTS"

        for attempt in range(MAX_RETRIES):

            try:

                response = self.session.get(

                    url,

                    timeout=(
                        CONNECT_TIMEOUT,
                        READ_TIMEOUT
                    )

                )

                if response.status_code == 200:

                    destination.write_bytes(
                        response.content
                    )

                    if CSVValidator.validate(destination):

                        time.sleep(
                            REQUEST_DELAY
                        )

                        return "DOWNLOADED"

                    destination.unlink(
                        missing_ok=True
                    )

                elif response.status_code == 404:

                    return "HOLIDAY"

                elif response.status_code == 403:

                    self.create_session()

            except requests.RequestException as e:
                print(f"\nRequest Error: {type(e).__name__}")
                print(e)

            time.sleep(
                2 ** attempt
            )

        return "FAILED"