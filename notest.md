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



```
