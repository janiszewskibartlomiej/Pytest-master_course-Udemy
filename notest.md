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

@property
def tweets(self):
    return self._tweets  _tweets - to atrybut prywatny
    
ten dekorator powoduje ze mozmey sie odwoalc do tej metody podobnie jak poprzednio czyli twitter.tweets

Fixture umożliwia uruchomienie funkcji z roznymi parametrami zadeklarowanymi np:
@pytest.fixture(params=["chrome", "firefox", "ie"]) spowoduje uruchomienie 3 roznych przegladarek.

zadeklarowanie w definicji request powoduje ze mamy dostep do np danych z jakiego miejsca został wywowalny test.

w takiej sytuacji:

@pytest.fixture(params=[None, 'python'], name ="twitter")
def username(request):
    return request.param

mamy dostep do wartosci zadeklarowanych poprzez .param
fixture przyjmuje rónież atrybut name aby zmieni nazwę pod którą beziemy przekazywac nasza fixue

@pytest.fixture(autouse=True)  > użycie autouse powoduje że ta fixtura jest wykonanan przed każdym testem i nie trzeba jej przekazywac. 
ta funkcjonalnosc uwazana jest za niebezpieczna praktyke

@pytest.fixture()
def backend(tmpdir):  # tmpdir to funkcja ktora zapisuje do tymczasowego pliku gdzies na dysku
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file  # to zostaje wydzielone do conftest ponieważ nie jest uzywany tyko do testow twitter
    
      
7. monkeypatch:

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):  # monkeypatch to wbudowana funkcja w pytest  >> mozemy argument napisywa, wyłącznia danycch funkcjonalności
    monkeypatch.delattr('requests.sessions.Session.request')  # tu wskazujey atrybut ktory chcemy wylaczyc z dzialania
    
  @pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, username, request, monkeypatch):
    if request.param == 'list':
        twitter = Twitter(username=username)
    elif request.param == 'backend':
        twitter = Twitter(backend=backend, username=username)

    def monkey_return(url):
         return "test"
     
    monkeypatch.setattr(twitter, 'get_user_avatar', monkey_return) # setattr przyjmuje obiekt który chcemy paczowac, metode do paczowania oraz 
    funkcje ktora zostanie wywowalana zamiast naszej metody get_ueser_avatar
    # funkcja monkey_return zostanie wywolana zamiast metody get_user... w obiekcie twitter

    return twitter  
    
    pytest.skip()  >> to nie bedzie wykonane
    
    8. mock from unittest:
    
    from unittest.mock import patch
    
    # pocztkowo kozystamy z funkcji path ktora jest czescioa unittest.mock, natomiast może to być kłopotliwe
    # poniewaz trzeba dodać pełna ścieżkę do metody i co ma zwrucic; dlatego druga wersja kozysta z patch.object
    with patch('twitter.Twitter.get_user_avatar', return_value='test'):
    # druga wersja kożysta z obiektu, przyjmuje obiekt, metode i co ma zwucic:
    with patch.object(Twitter, 'get_user_avatar', return_value='test'):

    # jezeli ni echcemy kozystac z blocku with mozna przekazac moka dekoratoerm @path.object
    @patch.object(Twitter, 'get_user_avatar', return_value='test')
def test_tweet_single_message(avatar_mock, twitter):  # avatar_mock - pod tą zmienną bedzie przekazany wynik dekoratora
    # i musi być wrzucony w tym miejscu poniewaz inaczej nie bedzie do niegfo dostepu
    twitter.tweet('Test message')
    assert twitter.tweet_messages == ['Test message']

    mock daje nam dostep do paru metod m.in
    
    avatar_mock.assert_called()  >> sprawdzamy czy zostala wywowalna nasza metoda >> get_user_avatar
    
mozemy rowniez zamokowac biblioteke request:
@patch.object(requests, 'get', return_value=ResponseGetMock())  >> mokujemy biblioteke requests o metodzie get i dostajemy return ResponseGetMock() 
def test_tweet_single_message(avatar_mock, twitter): 
....

class ResponseGetMock(object):
    def json(self):
        return {'avatar_url': 'test'}
        
9. obiekt Mock()

@patch.object(requests, 'get', return_value=ResponseGetMock())
def test_tweet_with_hashtag_mock(avatar_mock, twitter):
    twitter.find_hashtags = Mock()  # to jest obiekt Mock z unittest
    twitter.find_hashtags.return_value = ['first']  # przekazujemy wartosc "first" - napisujemy to co będzie w hashtagu 
    twitter.tweet('Test #second')
    assert twitter.tweets[0]['hashtags'] == ['first']  >> sprawdzamy czy pierszy elemnt listy to "first"
    twitter.find_hashtags.assert_called_with('Test #second')  >> sprawdzamy czy to zostalo wywolane z parametrem "Test #second"
    
 żeby nadpisa metody dunder np __eq__ trzeba uzyc mocka >> MagicMock()
    
def test_twitter_version(twitter):
    twitter.version = MagicMock()
    # uwaga MOck nie wspiera używania metod __naza__ dunder dlatego trzeba użyć MacicMock
    twitter.version.__eq__.return_value = '2.0'
    assert twitter.version == '2.0'
    
10. conftest:

Globalny plik konfiguracyjny, w ktorym zemy miec np hookie np 
    def pytest_runtest_setup():
    print("<-- strating test")
    
 trzymamy tam np funkcje ktore bedziemy uzwywac wielu miejscach
    
    
 11. coverage >> pip install pytest-cov
 
 uruchomienie pytest --cov twitter  >> nazwa modułu do testów czyli pliku
 
 mozemy wygenerowac raport z pokrycia cov poprzez >>  pytest --cov twitter --cov-report annotate  wygeneruje plik twitter.py,cover
 znak ">" to == ze jest pokrycie testami
 a tam gdzie jest znak "!" to nie przetestowae linijki kodu
 
 
 12. debugowanie
 
 import pdb
 pdb.set_trace() >>> jak umiescimy ten kod w danym miejscu to sie tu zatrzyma i bedziemy mieli dostep do zmiennych zadeklarowanych w tym miejscu.
 odpali sie konsola i bedzimey mogli wpisac np url i dostaneimy info jaka jest wartosc url. Możemy zobaczyc np czym jest requests.get  >> ze to jest MagicMock
 mozemy rozniez >> requests.get(url); mozna rowniez przypisac do zmiennych np ur = "test"
aby kontynuowac wystarczy wisac "c" i enter
pdb nie jest zbyt czytelne

lepiej pip install wdb  + pip install wdb.server

w kodzie trzeba umiescic wdb.set_trace() i musimy odpalic server  wdb.server.py

jak uruchomimy nasz kod to w przegladarce zstanie uruchomiona interaktywana sesja debugera webowego
wpisujac np self mam info na temat obiektu + wszytskie informacje jakie metody, wersja itd
wpisujac requests.get tez mamy wszelkie informacje. mozemy przesc do np resp  w naszej mtodzie >> __call__  >> self i co zwruci __return__

wszytskie slowa kluczowe w wdb zaczynamy od kropiki .c >> przejdzeimy do kolejnego wywoalanie wdb
 
 
    
    
    
    
```
