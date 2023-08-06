import os
from typing import Optional
import requests


class DiscordCDN:

    def __init__(self, cdn_url: str, file_name: str, file_path: Optional[str] = None, chunk_size: int = 8192):
        self.cdn_url = cdn_url
        self.chunk_size = chunk_size
        if file_path:
            self.local_path = os.path.join(file_path, file_name)
        else:
            self.local_path = file_name

    def download_file(self) -> Optional[requests.Response]:
        """Downloads the file from the given CDN URL as a stream.
                            :return: :class:`Response <Response>` object
                            :rtype: requests.Response
                         """
        response = requests.get(self.cdn_url, stream=True)
        response.raise_for_status()

        with open(self.local_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=self.chunk_size):
                if chunk:
                    file.write(chunk)

        return response
