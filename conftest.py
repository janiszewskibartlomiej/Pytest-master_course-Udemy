import pytest


def pytest_runtest_setup():
    print("<-- strating test")

@pytest.fixture(autouse=True)
def no_requests(monkeypatch):  # monkeypatch to argument do napisywyania, wyłącznia danycch funkcjonalności
    monkeypatch.delattr('requests.sessions.Session.request')  # tu wskazujey atrybut ktory chcemy wylaczyc z dzialania


@pytest.fixture()
def backend(tmpdir):  # tmpdir to funkcja ktora zapisuje do tymczasowego pliku gdzies na dysku
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file