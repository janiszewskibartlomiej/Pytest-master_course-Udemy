"""pip install pytest-watch <nasze testy wykonaja sie automatycznie po zapisaniu pliku
ptw   <komenda do wywolania watcha
"""
import pytest

from .is_anagram import is_anagram


def test_initial():
    assert is_anagram('test', 'test')

@pytest.mark.parametrize('message1, message2', (
        ('test', 'not test'),
        ('not test', 'test'),
        ('true', 'false'),
        ('test', 'tesssst')
))
def test_not_anagram(message1, message2):
    # assert not is_anagram('test', 'not test')
    assert not is_anagram(message1, message2)

# def test_not_anagram2():
    # assert not is_anagram('not test', 'test')

# def test_real_anagram():
#     assert is_anagram('test', 'tets')

@pytest.mark.parametrize('message1, message2', (
        ('test', 'tets'),
        ('cart horse', 'orchestra')
))
def test_real_anagram(message1, message2):
    assert is_anagram(message1, message2)