import json
from typing import Optional
import requests


class DiscordWebhook:

    def __init__(self, webhook_url: str, default_username: Optional[str] = None,
                 default_avatar_url: Optional[str] = None):
        self.webhook_url = webhook_url
        self.default_username = default_username
        self.default_avatar_url = default_avatar_url

    def _post_request(self, data: Optional[dict] = None, files: Optional[dict] = None) -> Optional[requests.Response]:
        """Sends a POST request to the webhook with the proper parameters.
                    :param data: This is a dict used to store params for the webhook (bot username, pfp, etc).
                    :param files: (optional) This is the binary file object. Used in send_file.
                    :return: :class:`Response <Response>` object
                    :rtype: requests.Response
                 """
        if data:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(self.webhook_url, headers=headers, data=json.dumps(data))
        else:
            response = requests.post(self.webhook_url, files=files)
        response.raise_for_status()
        return response

    def send_message(self, content: str, username: Optional[str] = None, avatar_url: Optional[str] = None) -> Optional[requests.Response]:
        """Sends a message to the webhook with the proper parameters.

            :param content: The actual message you are trying to send.
            :param username: (optional) The username of the bot that will be posting the message.
            :param avatar_url: (optional) URL holding the link to the profile picture for your bot.
            :return: :class:`Response <Response>` object
            :rtype: requests.Response
         """

        data = {'content': content, 'username': username or self.default_username,
                'avatar_url': avatar_url or self.default_avatar_url}
        return self._post_request(data=data)

    def send_file(self, file_path: str, file_name: Optional[str] = None, content: Optional[str] = None,
                  username: Optional[str] = None, avatar_url: Optional[str] = None) -> Optional[requests.Response]:
        """Sends a file to the webhook with the proper parameters.
                           :param file_path: This is the path to the file (should be represented as a raw string with r')
                           :param file_name: (optional) This is the name of the file. Is used to store the filename as that is a requirement per Discord docs.
                           :param content: (optional) This is the message that you are trying to send along with the file, if any.
                           :param username: (optional) This will be the displayed username of your webhook bot or class default.
                           :param avatar_url (optional) This is the direct link to the image used for your bot's pfp or class default.
                           :return: :class:`Response <Response>` object
                           :rtype: requests.Response
                        """
        if not file_name:
            file_name = file_path.split('/')[-1]

            with open(file_path, 'rb') as file:
                form_data = {
                    'file': (file_name, file),
                    'payload_json': (None, json.dumps({
                        'content': content,
                        'username': username or self.default_username,
                        'avatar_url': avatar_url or self.default_avatar_url
                    }))
                }
                return self._post_request(files=form_data)
