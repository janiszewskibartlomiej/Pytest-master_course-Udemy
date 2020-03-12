from unittest.mock import patch, Mock, MagicMock

import pytest
import requests

from twitter_example_with_JSON_file import Twitter

"""pip install pytest-cov  <-- dodatek  do pytest - sprawdza pokrycia kodu testami, jezlei dany modol nie jest przetestowany to nam to pokaze po wywolaniu
'pytest --cov nazwa_modłu np test_example_with_JSON_file' 

możemy uzyc funkcji raportu przy testach z coverege --> generuje plik z pokryciem kodu '!' nie sa pokryte:

pytest --cov nazwa_modłu np test_example_with_JSON_file --cov-report annotate

"""

class ResponseGetMock(object):
    def json(self):
        return {'avatar_url': 'test'}


# @pytest.fixture(autouse=True)  # bedzie wykonana przed każym testem nie zaleznie czy go potrzebuje czy nie
# - uwazana za niezpieczna

"""@pytest.fixture(autouse=True)
def no_requests(monkeypatch):  # monkeypatch to argument do napisywyania, wyłącznia danycch funkcjonalności
    monkeypatch.delattr('requests.sessions.Session.request')  # tu wskazujey atrybut ktory chcemy wylaczyc z dzialania


@pytest.fixture()
def backend(tmpdir):  # tmpdir to funkcja ktora zapisuje do tymczasowego pliku gdzies na dysku
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file"""  # to zostaje wydzielone do conftest ponieważ nie jest uzywany tyko do testow twitter


@pytest.fixture(params=[None, 'python'])
def username(request):
    return request.param


@pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, username, request, monkeypatch):
    if request.param == 'list':
        twitter = Twitter(username=username)
    elif request.param == 'backend':
        twitter = Twitter(backend=backend, username=username)

    """ def monkey_return(url):
         return ResponseGetMock()
     
     monkeypatch.setattr(requests, 'get', monkey_return)"""
    # to zamienimy na mocowanie ponieważ daje nam to więcej możliwości niż monke

    # monkeypatch.setattr(twitter, 'get_user_avatar', monkey_return)
    # funkcja monkey_return zostanie wywolana zamiast metody get_user... w obiekcie twitter

    return twitter


def test_twitter_init(twitter):
    assert twitter


"""@patch.object(Twitter, 'get_user_avatar', return_value='test') """


# ta metoda pachowania nei sprawdza wszytskiego - nie sprawdzamy dzialania request dlatego zmienimy moca na nastepujacy:
@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_single_message(avatar_mock, twitter):  # avatar_mock - pod tą zmienną bedzie przekazany wynik dekoratora
    # i musi być wrzucony w tym miejscu poniewaz inaczej nie bedzie do niegfo dostepu

    # pocztkowo kozystamy z funkcji path ktora jest czescioa unittest.mock, natomiast może to być kłopotliwe
    # poniewaz trzeba dodać pełna ścieżkę do metody; dlatego druga wersja kozysta z patch.object
    """with patch('twitter.Twitter.get_user_avatar', return_value='test'):"""
    # druga wersja kożysta z obiektu:
    """with patch.object(Twitter, 'get_user_avatar', return_value='test'):"""

    # jezeli ni echcemy kozystac z blocku with mozna przekazac moka dekoratoerm @path.object
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


@pytest.mark.parametrize("message, expected", [
    ("Test #first message", ["first"]),
    ("#first Test message", ["first"]),
    ("#FIRST Test message", ["first"]),
    ("Test message #first", ["first"]),
    ("Test message #first #second", ["first", "second"])
])
def test_tweet_hashtag(message, expected, twitter):
    assert twitter.find_hashtags(message) == expected
# ważne aby dodadwac parametry w postaci listy dziekii temu
# dane w wydruku sa indexowane i widoczne w print testach

 # ta odekorowana definicja robi to samo co 3 def na dole,
    # dekorator 3 razy wywoluje def z innymi parametrami


def test_init_twitt_class(backend):
    twitter1 = Twitter(backend=backend)
    twitter2 = Twitter(backend=backend)

    twitter1.tweet('Test 1')
    twitter2.tweet('Test 2')

    assert twitter2.tweet_messages == ['Test 1', 'Test 2']


"""@patch.object(Twitter, 'get_user_avatar', return_value='test') """


# ta metoda pachowania nei sprawdza wszytskiego - nie sprawdzamy dzialania request dlatego zmienimy moca na nastepujacy:
@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_username(avatar_mock, twitter):
    if not twitter.username:
        pytest.skip()
        # pomija w testach jezeli nie ma username

    twitter.tweet('Test message')
    assert twitter.tweets == [{'message': 'Test message', 'avatar': 'test', 'hashtags': []}]
    avatar_mock.assert_called()  # to jest metoda dostepna w mock.unittest i dzieki niej mamy mozliwosc sprawdzenia
    # czy ta funkcja zostala wywowalan to jest mozyc z zastosowania mock unittest


@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_hashtag_mock(avatar_mock, twitter):
    twitter.find_hashtags = Mock()  # to jest obiekt Mock z unittest
    twitter.find_hashtags.return_value = ['first']
    twitter.tweet('Test #second')
    assert twitter.tweets[0]['hashtags'] == ['first']
    twitter.find_hashtags.assert_called_with('Test #second')

def test_twitter_version(twitter):
    twitter.version = MagicMock()
    # uwaga MOck nie wspiera używania metod __naza__ dunder dlatego trzeba użyć MacicMock
    twitter.version.__eq__.return_value = '2.0'
    assert twitter.version == '2.0'

@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_twitter_get_all_hashtags(avatar_mock, twitter):
    twitter.tweet('Test #first')
    twitter.tweet('Test #first #second')
    twitter.tweet('Test #third')
    assert twitter.get_all_hashtags() == {'first', 'second', 'third'}

@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_twitter_get_all_ashtags_not_found(avatar_mock, twitter):
    twitter.tweet('Test first')
    assert twitter.get_all_hashtags() == "No hashtags found"

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
