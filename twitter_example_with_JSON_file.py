import json
import re
from urllib.parse import urljoin

import requests

USERS_API = "https://api.github.com/users/"


class Twitter(object):
    version = '1.0'

    def __init__(self, backend=None, username=None):
        self.backend = backend
        self._tweets = []
        self.username = username
        # if self.backend and not os.path.exists(self.backend):
        #     with open(self.backend, mode="w") as file:
        #         pass  <-- ten if został przeniesiony do fixture backend

    # def delete(self):
    #     print("It's the end")
    #     if self.backend:
    #         os.remove(self.backend)
    # ta metoda nie jest potrzebna bo funkcja tmpdir dba o del po zakończeniu

    @property  # ustawia dzialnie getera, setera oraz del
    # przy wywoalnia ponizszej funkcji
    def tweets(self):
        if self.backend and not self._tweets:
            backend_text = self.backend.read()
            if backend_text:
                # with open(self.backend) as twitter_file:
                self._tweets = json.loads(backend_text)
        return self._tweets

    @property
    def tweet_messages(self):
        return [tweet['message'] for tweet in self.tweets]

    def get_user_avatar(self):
        if not self.username:
            return None
        url = urljoin(USERS_API, self.username)
        # urljoin to metoda biblioteki urllib parse
        # print(url)
        response = requests.get(url)
        return response.json()['avatar_url']

    def tweet(self, message):
        if len(message) > 160:
            raise Exception("Message too long")
        self.tweets.append({'message': message,
                            'avatar': self.get_user_avatar()
                            })
        if self.backend:
            # with open(self.backend, mode='w') as twitter_file:
            # twitter_file.write("\n".join(self.tweets))
            self.backend.write(json.dumps(self.tweets))

    def find_hashtags(self, message):
        return [m.lower() for m in re.findall("#(\w+)", message)]


if __name__ == '__main__':
    twitter = Twitter()
    twitter.tweet('test wiadomosci')
    print(twitter.tweets)
