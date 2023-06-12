# Tests file
Nous allons ici détailler quelques tests et résultats de tesseract afin de voir son fonctionnement et ses difficultés.

## 05/12/2022
`plong-multiple-txt.png`: Une page de texte (500x500) qui contient 8 éléments de texte :
![plong-multiple-txt.png](images/plong-multiple-txt.png) \
Pour cette image, nous avons observé le résultat suivant:
```
WALT DISNEY
5 dec. 1901

ana!
£& À

v
12 avr. 1992 %,

MICKEY

DONALD
BLUTO
```
On constate donc que Tesseract a du mal avec les textes qui ne sont pas à l'horizontale. Ainsi que les polices d'écriture non pleines à couleur claire (PLUTO -> BLUTO) \
Nous avons essayé avec un fond transparent pour voir si cela reglait le problème de PLUTO :
![plong-multiple-txt-nobg.png](images/plong-multiple-txt-nobg.png) \
Le résultat est le suivant:
```
WALT DISNEY
5 dec. 1901

ana!
£& À

À
12 avr. 1992 %,

MICKEY

DONALD
BLUTO
```
Nous constatons que le résultat est identique à l'image précédente (excepté pour le 'v' de Minnie qui se transforme en 'À'). Le fond n'a donc pas d'impact sur les polices vides. \

Nous avons ensuite réessayé avec la même image mais en enlevant le texte incurvé de Disneyland Paris. \
![plong-multiple-txt-nocurve.png](images/plong-multiple-txt-nocurve.png)

Nous avons obtenu le résultat suivant:
```
WALT DISNEY
5 dec. 1901

Minnie

12 avr. 1992

MICKEY

DONALD
BLUTO
```
Tesseract a maintenant réussi à lire "Minnie". Nous pouvons en conclure que le texte incurvé est une des difficultés de Tesseract. Il faudra donc utiliser des images dans lesquelles les textes sont seulement à l'horizontale.

Precompositing opencv (n&b, contraste, ...)
Tesseract donne la position du texte lu