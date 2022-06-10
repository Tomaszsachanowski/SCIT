# SCIT
## OPIS

SCIT to metoda MTD mająca na celu zmniejszenie czasu ekspozycji systemu przechowywanego w kopiach. Założenie techniki polega na tym, że ​​system jest nieustannie atakowany. W metodzie nie wykrywamy samego ataku lecz kreujemy wizję, że taki atak miał miejsce i reagujemy na to w postaci czyszczenia systemu. To zmusza atakującego do ciągłego utrzymywania się w systemie. Dodatkowo SCIT zapewnia ochronę podczas opracowywania, testowania i stosowania łatek systemu.  W skład projektu wchodzą 3 komponenty: kontroler, maszyny serwerowe oraz maszyny klienckie symulujące korzystanie z danej usługi. Kopie systemu (maszyny serwerowe), które nie są używane, są czyszczone i przywracane do nieskazitelnego stanu. Każda maszyna serwerowa jest zaimplementowana przy pomocy środowiska wirtualnego.
Kolejnym elementem jest kontroler, który zarządza rotacją maszyn wirtualnych i czasem ich ekspozycji. Maszyny serwerowe są w jednym czterech stanów: W pierwszym stanie serwer aktywnie przetwarza usługę/zlecenia (np. HTTP) 
W drugim stanie serwer przetwarza zlecenia, które już zobowiązał się rozpatrzyć, ale nie przyjmuje nowych.
W trzecim stanie serwer jest nieaktywny. Jest on czyszczony, w tym momencie inny serwer powinien wskoczyć na jego miejsce. W ostatnim stanie serwer czeka na powrót do stanu początkowego.

Kontroler zarządza maszynami i przestrzega określonej strategii działania. Maszyny są bowiem przełączane co pewien określony kwant czasu. W każdym momencie może być kilka maszyn w każdym ze stanów. (np. 2 gotowe do pracy, 2 nieaktywne). W projekcie będziemy rozpatrywać jednofunkcyjne serwery SCIT mający jeden wirtualny serwer online, który odbiera wiadomości przychodzące, przetwarza je i wysyła wyniki. Kopie systemu zawierają mechanizm multisesji, aby dane podczas przełączania nie zginęły.

## IMPLEMENTACJA

Koncepcja SCIT będzie wdrożona i testowana na oprogramowaniu docker, które zapewni nam wirtualizację  i wiele kopii systemu. W architekturze SCIT centralnym komponentem jest kontroler,  który będzie napisany w języku Python z biblioteką docker (do zarządzania obrazami) oraz asyncio (do uruchomiania w pętli asynchroniczej kolejnych stanów maszyny). Będzie on odpowiadał za czasy rotacji i ekspozycji maszyny wirtualnej oraz zostanie uruchomiony na osobnej maszynie wewnętrznej. Prosta aplikacja web świadcząca usługi klientom będzie zbudowana przy użyciu biblioteki flask. Pozwoli nam to m.in. zasymulować mechanizm zachowania sesji w trakcie przełączania.

## METRYKI 

Czas odpowiedzi dla użytkowników, zmienną jest ilość użytkowników i czas ekspozycji systemu.
Czas ekspozycji definiujący kompromis między bezpieczeństwem a dostępnością. Zużycie procesora przy zmiennej jest ilość kopii serwera

## SCENARIUSZE

1) Sprawdzenie czy tylko jeden, aktywny serwer przetwarza zlecenia.
2) Przełączanie serwera w trakcie przetwarzania zleceń i sprawdzenie czy je dokańcza (sesja powinna być zachowana).
3) Zbadanie czy serwery zmieniają stany przy pomocy kontrolera.
4) Sprawdzenie zachowania metody przy większej ilości maszyn wirtualnych.
5) Przesyłamy do serwera dużo zgłoszeń (szukamy granicy działania). Problemem będzie prawdopodobnie wysłanie większej ilości zapytań niż serwer może przetworzyć w danym kwancie.

## URUCHOMIENIE

```
Sprzęt musi posiadać możliwość wirtualizacji
docker-compose (https://docs.docker.com/compose/install/)
python3.8+ (https://www.python.org/downloads/)
pip3 (https://pypi.org/project/pip/)
```

### Przygotowanie

```
conda env create -f environment.yml
```

### Uruchomienie docker-compose
```
W osobnym terminalu, który znajduje się w lokalizacji SCIT/scit

docker-compose up
```

### Uruchomienie controlera
```
W osobnym terminalu, który znajduje się w lokalizacji SCIT/scit/controller

python main.py
```

### Uruchomienie testów
```
Trzeba dodać biblioteki matplotlib i timeit.
W osobnym terminalu, który znajduje się w lokalizacji SCIT/scit
python tests/response.py
```
