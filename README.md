# Opty-spes

Programme d'optimisation des spécialités de la 1ère et la Terminale.

## Fichier d'entrée

Le fichier d'entrée est au format _csv_ séparé par des `;`.
Il est sous la forme du tableau suivant :

|  Classe   |   Noms   |  Prénom   | Spécialité 1 | Spécialité 2 | Spécialité 3 | ... |
|:---------:|:--------:|:---------:|:------------:|:------------:|:------------:|:---:|
| Nombre d'élèves par spécialité |||      35      |      35      |      12      |     |
| Classe 1  | Noms 1   | Prénom 1  |       1      |      1       |       1      |     |
| Classe 2  | Noms 2   | Prénom 2  |       1      |      1       |       1      |     |
| Classe 3  | Noms 3   | Prénom 3  |              |      1       |       1      |  1  |
| Classe 4  | Noms 4   | Prénom 4  |       1      |      1       |              |  1  |
| Classe 5  | Noms 5   | Prénom 5  |       1      |              |       1      |  1  |

## Fichier de résultat

Le meilleur résultat trouvé sera sauvegarder dans le fichier `résultat.csv`.
Il est sous la forme du tableau suivant :

|  Classe   |   Noms   |  Prénom   |   Groupe 1   |   Groupe 2   |   Groupe 3   |
|:---------:|:--------:|:---------:|:------------:|:------------:|:------------:|
| Classe 1  | Noms 1   | Prénom 1  | Spécialité 1 | Spécialité 4 | Spécialité 3 |
| Classe 2  | Noms 2   | Prénom 2  | Spécialité 1 | Spécialité 4 | Spécialité 7 |
| Classe 3  | Noms 3   | Prénom 3  | Spécialité 1 | Spécialité 4 | Spécialité 6 |
| Classe 4  | Noms 4   | Prénom 4  | Spécialité 1 | Spécialité 2 | Spécialité 5 |
| Classe 5  | Noms 5   | Prénom 5  | Spécialité 1 | Spécialité 2 | Spécialité 5 |
 
## Crédit
Icons made by [Eucalyp](https://www.flaticon.com/authors/eucalyp) from [www.flaticon.com](https://www.flaticon.com)