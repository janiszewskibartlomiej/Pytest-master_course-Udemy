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
        """zamiast printować możemy użyć biblioteki pdb kora np poprzez 
        komende pdb.set_trace() zatrzymuje działem  i mamy dostep do wszytskich wynikow i zmiennych. 
        Żeby przejsc dalej do nastepenje metody ktora wywoluje get_user_avatar wpisujemy 'c'
        mozemy spardzic co jest np pod requests.get(url) 
        mozemy rowniez przypisac rozne wartosci do zmiennych. pdp jest malo czytelne dlatego 
        lepiej kozystac w web debug import wdb.set_trace
        musimy zainstalować poprzez pip install wdb   oraz pip install wdb.server
        odpalenie po aktywacji servera wdb.server.py + run pytest zostanie wyolany kod w przegladarce
        przejscie do nastepnego wywoalnia naszego wdb.set... komenda '.c'"""
        import pdb
        pdb.set_trace()
        response = requests.get(url)
        print(response.json()['avatar_url'])
        return response.json()['avatar_url']

    def tweet(self, message):
        if len(message) > 160:
            raise Exception("Message too long")
        self.tweets.append({'message': message,
                            'avatar': self.get_user_avatar(),
                            'hashtags': self.find_hashtags(message)
                            })
        if self.backend:
            # with open(self.backend, mode='w') as twitter_file:
            # twitter_file.write("\n".join(self.tweets))
            self.backend.write(json.dumps(self.tweets))

    def find_hashtags(self, message):
        return [m.lower() for m in re.findall("#(\w+)", message)]


    def get_all_hashtags(self):
        hashtags = []
        for message in self.tweets:
            hashtags.extend(message['hashtags'])
        if hashtags:
            return set(hashtags)
        return "No hashtags found"
