# fr-passphrase

Générateur de passphrase en français, selon la méthode [Diceware](https://fr.wikipedia.org/wiki/Diceware).

```
python passphrase.py
vivait-fleur-vieillir-braver-rater
```

Le projet s'appuie sur [mbelivo/diceware-wordlists-fr](https://github.com/mbelivo/diceware-wordlists-fr). Le fichier `wordlist.txt` correspond à la liste `wordlist_fr_5d` : 7776 mots indexés par 5 lancers de dé (de `11111` à `66666`). Chaque mot apporte environ 12,9 bits d'entropie.

## Utilisation

Nécessite Python 3.10 ou plus récent. Le script n'utilise que la bibliothèque standard et lit automatiquement le `wordlist.txt` placé dans le même dossier.

```bash
python passphrase.py               # entropie d'au moins 56 bits (5 mots)
python passphrase.py 6             # nombre de mots imposé
python passphrase.py -e 80         # entropie minimale en bits
python passphrase.py -s " "        # séparateur personnalisé (tiret par défaut)
python passphrase.py -u            # majuscule au début d'un mot choisi au hasard
python passphrase.py -d 3          # nombre de 3 chiffres inséré à une position au hasard
python passphrase.py -v            # affiche l'entropie obtenue
```

Exemple avec `-u -d 3` : `anatomie-Hibou-768-sauveur-tabac-poche`.

La majuscule et le nombre sont tirés au hasard et comptés dans l'entropie, mais ils en apportent peu : environ 2 bits pour la majuscule et 3,3 bits par chiffre, contre 12,9 bits par mot. Ils servent surtout à respecter les politiques de mot de passe qui les exigent. Pour plus de sécurité, mieux vaut ajouter un mot.

Le script affiche un avertissement si l'entropie descend sous 44 bits.

## Version web

Une version en ligne est disponible sur https://jsdlm.github.io/fr-passphrase/. La génération se fait entièrement dans le navigateur. Le code se trouve dans `docs/`.

## Crédits

- https://theworld.com/~reinhold/diceware.html
- https://github.com/mbelivo/diceware-wordlists-fr
