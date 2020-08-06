```Python
0.  Testy:

          Given << dla danej sytuacji otrzymanej [inicjalizacja]
          When << kiedy wykonamy jakąś akcje
          Then << sprawdzamy czy nasz rezultat by dobry

1. 
assert sprawdza czy coś jest True

2.
uruchomienie testów poprzez py.test w konsoli lub ustawieni uruchomienia w pycharmie z add new configuration > Python test

3. 
wywolanie wyjatku poprzez slowo raise Exception(""message) << Exc... to podstawowy wyjatek

4. with pytest.raises(Exception):     << sprawdza czy ten blok wywowal wyjatek exception jezeli tak to test bedzie pass poniewaz spodziewalismy sie tego

5. parametryzacja testow - wywolanie tego samego kodu be potrzeby powtarzania kodu:

@pytest.mark.parametrize("message, expected", (
        ("Test #first message", ["first"]),
        ("#first Test message", ["first"]),
        ("#FIRST Test message", ["first"]),
        ("Test message #first", ["first"]),
        ("Test message #first #second", ["first", "second"])
))
def test_tweet_with_hashtag(message, expected):
    twitter = Twitter()
    assert twitter.find_hashtags(message) == expected
    
    w ten sposób nie dublujemy kodu a jedynie wywowujemy poprzez parametry. dobra praktyka jest stosowanei slowa expected.
    
błędy ktory zostaną wyświtlone np test_tweet_with_hashtag[#FIRST Test message-expected2]   mowi ze w  2 elemncie  expected jest probem [index od zera] czyli 
ten przypadek ("#FIRST Test message", ["first"])

6. fixture >> przekazywanie dodatkowych danych wejsciowych bedacych czyms innym niz parametrize test.

zaoszczedza kod i otwiera nowe mozliwosci, fixture jest globalnie dostepnym kodem, mozemy go dodawac do dowolnej fukcji.
Dzięki temu podejsciu deklarujemy tylko jeden raz np klase Twitter i przakzujemy ja do danych funkcji:

@pytest.fixture
def twitter():
    twitter = Twitter()
    return twitter

def test_tweet_with_hashtag(twitter, message, expected):
    assert twitter.find_hashtags(message) == expected

@pytest.fixture przyjmuje parametry pierwszy to scope ktory mowi jakd dlugo nasz fixture ma zyc 
domyslnie scope="function" mówi że fixture jest deklarowany przed kazda funkcja i umiera zaraz po niej.

drugi (scope="module") >> fixture beedzie stworzone na jeden plik testow czylu moduł

trzeeci (scope="session") >> bedzie tworzona tylko na raz i wspoldzielona dla wszystkich testow.

ważna czescią fixture jest generator >> yield np twitter  gdzie przy wywolaniu funkcji testowej kod dochodzi do pozycji yield a po jej zakonczeniu wolana jest funkcja
__next__  np:

@pytest.fixture
def twitter():
    twitter = Twitter()
    yield twitter
    twitter.delete()

fixture domyslnie przyjmuje parametr request który ma dostęp do rożnych informacji https://docs.pytest.org/en/2.8.7/builtin.html#_pytest.python.FixtureRequest
np request.module

bardzo ciekawa funkcja jest request.addfinalizer(function) któa wykonuje fukcję po wykonaniu testu , na końcu [zastepuje nam to generator]:
add finalizer/teardown function to be called after the last test within the requesting test context finished execution.

@pytest.fixture
def twitter(request):
    twitter = Twitter()
    
    def fin():
        twitter.delete()
    request.addfinalizer(fin)    
    return twitter
    
Pytest rekomenduje uzywanie generatorów !!!




```
