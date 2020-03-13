def test_sum():
    assert 2+2 == 4

def test_get_element():
    custom_list = ['test']
    assert custom_list[0] == 'test'

"""to są przykładowe definicje do sprawdzenia odpalania testów, run możemy dodac sciezke calaego katalogu zamiast pliku
 wtedy wykonakja si ewszytskie testy z katalogu.
 
 *możemy odpalic test tylko danej metody -> pytest test_example_with_JSON_file.py::test_tweet_single_message
 
 * mozemy rowniez odpalic testy wszystkich fukcji ktore w nazwie np hashtag
 pytest -k hashtag 
 
 *wygodnijest uzywac flagi -k do wywolania testow na danej metodzie poniewaz nie musimy podawac calej sciezki
 wiec np wpisujemy pytest -k test_get_element
 """