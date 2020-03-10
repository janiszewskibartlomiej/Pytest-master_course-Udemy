import pytest
import requests

from twitter_example_with_JSON_file import Twitter


class ResponseGetMock(object):
    def json(self):
        return {'avatar_url': 'test'}


# @pytest.fixture(autouse=True)  # bedzie wykonana przed każym testem nie zaleznie czy go potrzebuje czy nie
# - uwazana za niezpieczna

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):  # monkeypatch to argument do napisywyania, wyłącznia danycch funkcjonalności
    monkeypatch.delattr('requests.sessions.Session.request')  # tu wskazujey atrybut ktory chcemy wylaczyc z dzialania


@pytest.fixture()
def backend(tmpdir):  # tmpdir to funkcja ktora zapisuje do tymczasowego pliku gdzies na dysku
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file


@pytest.fixture(params=[None, 'python'])
def username(request):
    return request.param


@pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, username, request, monkeypatch):
    if request.param == 'list':
        twitter = Twitter(username=username)
    elif request.param == 'backend':
        twitter = Twitter(backend=backend, username=username)

    def monkey_return(url):
        return ResponseGetMock()

    monkeypatch.setattr(requests, 'get', monkey_return)

    #monkeypatch.setattr(twitter, 'get_user_avatar', monkey_return)
    # funkcja monkey_return zostanie wywolana zamiast metody get_user... w obiekcie twitter

    return twitter


def test_twitter_init(twitter):
    assert twitter


def test_tweet_message(twitter):
    twitter.tweet('Test message')
    assert twitter.tweet_messages == ['Test message']


# ten @ powoduje wywolanie poniższej
# definicji w kazdej funkcji ktora ma przekazywany parametr twitter
# w ten sposob eliminujemy dubluwanie kodu, ktory za kazdym razem tworzył
# kalse Twitter. zastosowanie "params" powoduje wywolanie definicji
# z parametrami zawartymi w liście - w tym wypadku wywoluje 2 razy -> z None
# oraz z text.txt


# twitter.delete()  <- tmpdir dba o usuwanie po tescie pliku wiec metoda del nie jest potrzebna
# print("\n", request.function, request.module)


def test_long_tweet(twitter):
    # tweeter = Twitter()
    with pytest.raises(Exception):
        twitter.tweet("test" * 41)
    assert twitter.tweet_messages == []


def test_init_twitt_class(backend):
    twitter1 = Twitter(backend=backend)
    twitter2 = Twitter(backend=backend)

    twitter1.tweet('Test 1')
    twitter2.tweet('Test 2')

    assert twitter2.tweet_messages == ['Test 1', 'Test 2']


@pytest.mark.parametrize("message, expected", [
    ("Test #first message", ["first"]),
    ("#first Test message", ["first"]),
    ("#FIRST Test message", ["first"]),
    ("Test message #first", ["first"]),
    ("Test message #first #second", ["first", "second"])
])  # ważne aby dodadwac parametry w postaci listy dziekii temu
# dane w wydruku sa indexowane i widoczne w print testach

def test_tweet_hashtag(message, expected, twitter):
    assert twitter.find_hashtags(message) == expected  # ta odekorowana definicja robi to samo co 3 def na dole,
    # dekorator 3 razy wywoluje def z innymi parametrami


def test_tweet_with_username(twitter):
    if not twitter.username:
        pytest.skip()
        # pomija w testach jezeli nie ma username

    twitter.tweet('Test message')
    assert twitter.tweets == [{'message': 'Test message', 'avatar': 'test'}]

# def test_tweer_with_hashtag():
#     tweeter = Twitter()
#     message = "Test #first message"
#     # tweeter.tweet(message)
#     print("\n", "-------------------\n", tweeter.find_hashtags(message))  # < moja inwencja
#     assert 'first' in tweeter.find_hashtags(message)
#
#
# def test_tweer_with_hashtag_on_beginning():
#     tweeter = Twitter()
#     message = "#first Test message"
#     # tweeter.tweet(message)
#     assert 'first' in tweeter.find_hashtags(message)
#
#
# def test_tweer_with_hashtag_uppercase():
#     tweeter = Twitter()
#     message = "#FIRST Test message"
#     # tweeter.tweet(message)  < to jest zbedene
#     assert 'FIRST' in tweeter.find_hashtags(message)
