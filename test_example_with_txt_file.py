import pytest

from twitter_example_with_txt_file import Twitter


# @pytest.fixture(autouse=True)  # bedzie wykonana przed każym testem nie zaleznie czy go potrzebuje czy nie
# - uwazana za niezpieczna

@pytest.fixture()
def backend(tmpdir):  # tmpdir to funkcja ktora zapisuje do tymczasowego pliku gdzies na dysku
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file


@pytest.fixture(scope="function", params=['list', 'backend'], name='twitter')
# ten @ powoduje wywolanie poniższej
# definicji w kazdej funkcji ktora ma przekazywany parametr twitter
# w ten sposob eliminujemy dubluwanie kodu, ktory za kazdym razem tworzył
# kalse Twitter. zastosowanie "params" powoduje wywolanie definicji
# z parametrami zawartymi w liście - w tym wypadku wywoluje 2 razy -> z None
# oraz z text.txt
def fixture_twitter(backend, request):  # do tej def przekazujemy fixture backend
    if request.param == 'list':
        twitter = Twitter()
    elif request.param == 'backend':
        twitter = Twitter(backend=backend)
    yield twitter
    # twitter.delete()  <- tmpdir dba o usuwanie po tescie pliku wiec metoda del nie jest potrzebna
    print("\n", request.function, request.module)


def test_twitter_init(twitter):
    assert twitter


def test_tweet_message(twitter):
    # twitter = Twitter()
    twitter.tweet('test message')
    print("\n-------------\n", twitter.tweets)
    assert twitter.tweets == ['test message']


def test_long_tweet(twitter):
    # tweeter = Twitter()
    with pytest.raises(Exception):
        twitter.tweet("test" * 41)
    assert twitter.tweets == []


def test_init_twitt_class(backend):
    twitter1 = Twitter(backend=backend)
    twitter2 = Twitter(backend=backend)

    twitter1.tweet('Test 1')
    twitter2.tweet('Test 2')

    assert twitter2.tweets == ['Test 1', 'Test 2']


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
