import os

import pytest

"""funkcja pytest.mark.skip powoduje że dany test odekorowany nie bedzie wykonany,
druga opcja to ...skipif czyli warunkowe wykonanie testu,
ponizej przykład że test nie zostanie wywolany jezeli zmienna srodowiskowa no_summing bedzie rowna 1
reason to jest powod ominiecia tego testu
deklaracja zmiennej no_summin moze odpbywac sie jako przypisanie przed wywolaniem w jednej lini lub jako zmienna globalna
1. sposób NO_SUMMING=1 pytest my_custom_test.py
2. sposób export NO_SUMMING=1
w celu sprawdzenia mozna wyprintowac zmienna printenv NO_SUMMING
"""

@pytest.mark.skipif(os.environ.get('NO_SUMMING') == '1', reason='NO_SUMMING set to 1')
def test_sum():
    assert 2 + 2 == 4


"""zaznaczamy je @ jako expect faild"""
@pytest.mark.xfail
def test_get_element_list():
    custom_list = ['test']
    assert custom_list[0] == 'faild'


"""to są przykładowe definicje do sprawdzenia odpalania testów, run możemy dodac sciezke calaego katalogu zamiast pliku
 wtedy wykonakja si ewszytskie testy z katalogu.
 
 *możemy odpalic test tylko danej metody -> pytest test_example_with_JSON_file.py::test_tweet_single_message
 
 * mozemy rowniez odpalic testy wszystkich fukcji ktore w nazwie np hashtag
 pytest -k hashtag 
 
 *wygodnijest uzywac flagi -k do wywolania testow na danej metodzie poniewaz nie musimy podawac calej sciezki
 wiec np wpisujemy pytest -k test_get_element
 """
