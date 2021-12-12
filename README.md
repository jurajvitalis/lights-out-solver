# Lights Out

V našom zadaní máme implementované riešenie hry Lights Out pomocou 3 vyhľadávacích algoritmov.

## Reprezentácia stavu hry

Kedže v nasledujúcich algoritmoch sa vyžaduje vyhľadávanie v grafe, pokladali sme za potrebné definovať si štruktúru Node, ktorá reprezentuje:

- Stav hry (Rozpoloženie zasvietených políčok)
- Odkaz na rodiča (Stav, z ktorého sme dostali aktuálny stav)
- Akcia, ktora bola vykonaná na rodičovskom stave
- $h(n)$ - Hodnota heuristickej funkcie 
- $g(n)$ - Hodnota cenovej funkcie (vzdialenosť od počiatočného stavu)

## DFS

Algoritmus DFS máme implementovaný iteratívne, zásobník reprezentujeme pomocou dátovej štruktúry **stack**.

DFS spočíva v brute-force prístupe, ktorý prechádza stavový priestor (graf) nasledovným spôsobom:

1. Vyberie si posledne pridaný stav zo zásobnika
2. Ak stav ešte nebol expandovaný, expanduje ho a označí ako už expandovaný
   - Ak susedný stav, ktorý algoritmus našiel expandovaním predstavuje finálny stav hry, algoritmus našiel riešenie

## Greedy

Algoritmus Greedy máme implementovaný iteratívne, zásobník reprezentujeme pomocou dátovej štruktúry **priority queue**, ktorú zoraďujeme na základe heuristickej funkcie $h(n)$.

Heuristická funkcia vyzerá následovne:

​	$$h(n) = Pocet \space\space zasvietenych \space\space policok$$

Algoritmus prechádza stavový priestor (graf) nasledovným spôsobom:

1. Vyberie stav s minimálnou hodnotou $h(n)$ zo zásobnika
2. Ak stav predstavuje finálny stav hry, algoritmus našiel riešenie
3. Ak stav ešte nebol expandovaný, expanduje ho a označí ako už expandovaný

## A*

Algoritmus Hladového vyhľadávania máme implementovaný iteratívne, zásobník reprezentujeme pomocou dátovej štruktúry **priority queue**, ktorú zoraďujeme na základe funkcie $f(n)$.

Funkcia $f(n)$ vyzerá následovne:

$$f(n) = h(n) + g(n)$$

$$f(n) = Pocet \space\space zasvietenych \space\space policok + vzdialenost \space\space od \space\space pociatocneho \space\space stavu$$

Algoritmus prechádza stavový priestor (graf) nasledovným spôsobom:

1. Vyberie stav s minimálnou hodnotou $f(n)$ zo zásobnika
2. Ak stav predstavuje finálny stav hry, algoritmus našiel riešenie
3. Ak stav ešte nebol expandovaný, expanduje ho a označí ako už expandovaný