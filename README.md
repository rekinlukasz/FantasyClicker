# ⚔️ Fantasy Clicker

Prosta gra typu clicker w klimacie fantasy, napisana w Pythonie i działająca w przeglądarce dzięki [PyScript](https://pyscript.net/).

Klikaj magiczny kryształ 💎, zbieraj złoto i kupuj ulepszenia: zaklęty miecz, elfiego łucznika, krasnoluda górnika, czarodzieja i smoka.

## Wymagania

- Python 3 (tylko do uruchomienia lokalnego serwera)
- Przeglądarka internetowa z dostępem do internetu (PyScript ładuje się z `pyscript.net`)

## Uruchomienie

1. Otwórz terminal w folderze z grą.
2. Uruchom lokalny serwer:

   ```bash
   python -m http.server 8000
   ```

3. Otwórz w przeglądarce adres: http://localhost:8000
4. Poczekaj kilka sekund. Przy pierwszym uruchomieniu przeglądarka pobiera Pythona.

Serwer zatrzymasz w terminalu skrótem `Ctrl+C`.

> Samo otwarcie pliku `index.html` dwuklikiem nie zadziała, bo przeglądarka nie wczyta wtedy pliku `main.py`.

## Uruchomienie na GitHub Pages

Grę można opublikować bez własnego serwera:

1. Wypchnij repozytorium na GitHuba.
2. Wejdź w **Settings → Pages**.
3. W sekcji **Build and deployment** wybierz gałąź `main` i folder `/ (root)`, potem kliknij **Save**.
4. Po chwili gra będzie dostępna pod adresem `https://<twoja-nazwa>.github.io/FantasyClicker/`.

## Zapis gry

Postęp zapisuje się automatycznie w `localStorage` przeglądarki: co 5 sekund i po każdym zakupie. Gra nie używa ciasteczek i nie wysyła nigdzie żadnych danych. Przycisk **Zacznij od nowa** zeruje postęp.

## Pliki

- `index.html`: wygląd gry i style
- `main.py`: logika gry w Pythonie
