# import os
import re


class Twitter(object):
    version = '1.0'

    def __init__(self, backend=None, username=None):
        self.backend = backend
        self._tweets = []

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
            # with open(self.backend) as twitter_file:
            self._tweets = [line.rstrip('\n') for line in self.backend.readlines()]
        return self._tweets

    def tweet(self, message):
        if len(message) > 160:
            raise Exception("Message too long")
        self.tweets.append(message)
        if self.backend:
            # with open(self.backend, mode='w') as twitter_file:
            # twitter_file.write("\n".join(self.tweets))
            self.backend.write("\n".join(self.tweets))

    def find_hashtags(self, message):
        return [m.lower() for m in re.findall("#(\w+)", message)]


if __name__ == '__main__':
    twitter = Twitter()
    twitter.tweet('test wiadomosci')
    print(twitter.tweets)
