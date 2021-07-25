ConnectionPool() to klasa która obsługuje połączenia do bazy danych:
1. connection - obiekt polaczenia do DB
2. in_use = False - bazowy status pokazujacy ze polaczenie jest nieuzywane 
3. number - bazowa ilosc przechowywanych polaczen
4. max_conn - maksymana liczba utrzymywanych polaczen

Uruchomienie:
1. W katalogu projektu stwórz plik config.ini w poniższym szablonie.
Konfiguracja bnazy danych jest potrzebna do wykonywania testów naobiekcie poola

[DATABASE]
db_user = twoj_user
password = twoje_pass
host = twoje ip (np: localhost)
port = twoj_port
database = twoja_testowa_DB

2. pip install psycopg2

3. uruchomienie skryptu test_machine.py demonstruje wielowontkowe dzialanie poola.

DEMO:
1. https://www.youtube.com/watch?v=vuvwoNfwiio

2. https://www.youtube.com/watch?v=4zEeeKSp2xE