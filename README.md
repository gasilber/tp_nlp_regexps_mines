# Travaux pratiques sur les expressions régulières: JudiLibre

Vous venez d'être recruté par la jeune startup [Docteur Justice](https://fr.wikipedia.org/wiki/Docteur_Justice) qui souhaite créer un LLM afin de réaliser des analyses juridiques.
Pour cela, cette startup a besoin d'un fond documentaire incluant les données de jurisprudence des cours de droit privé (tribunaux judiciaires, cours d'appel et cour de cassation).
Votre première mission est de participer à la création d'un système permettant de récupérer toutes les décisions de la cour de cassation en HTML qui sont disponibles sur le site [judilibre](https://www.courdecassation.fr/acces-rapide-judilibre) de la cour de cassation, et de structurer les données obtenues en JSON.

## Installation du TP

```bash
git clone https://github.com/gasilber/tp_nlp_regexps_mines
# ou git clone git@github.com:gasilber/tp_nlp_regexps_mines si vous avez un compte Github
cd tp_nlp_regexps_mines
python3 -m venv .venv/tp_regexps
source .venv/tp_regexps/bin/activate
pip install -e .
```

## Exercice:  extraction de données structurées

Afin de faciliter votre travail, 120 décisions en HTML ont été récupérées sur le site Judilibre, et une première structuration partielle a été faite, dans le répertoire `data/ccass`, où pour chaque fichier HTML, un fichier JSON correspondant représente les données structurées (partiellemen). Le premier exemple est structuré complètement, pour vous donner un exemple de ce qu'il faut obtenir: `data/ccass/6757dc458b75c64649d25972.html` donnant `data/ccass/6757dc458b75c64649d25972.json`.

Grâce à des expressions régulières, modifiez la méthode `from_html` de la classe `Decision` dans le fichier `tp_regexps/decision.py` pour compléter l'extraction des différents éléments. Il faudra également compléter et créer les expressions régulières correspondantes dans `tp_regexps/regexps.py`.

Utilisez `unittest` tel que ci-dessous pour mesurer l'avancée de votre travail:

```bash
python -m unittest tp_regexps.test_regexps
```

### Exemple d'extraction du "header" et de la chambre

Tout d'abord, le _header_ qui est de la forme:

```html
<div class="decision-header">
          <p class="h4-like">Chambre criminelle
                          -
              Formation restreinte hors RNSM/NA
                      </p>
                              <p class="h4-like h4-like--emphase">
                                          Publié au Bulletin
                                                    </p>
          <p>ECLI:FR:CCASS:2024:CR01492</p>
        </div>
```

Construction d'une regexp spécifique:

```python
header_re = re.compile(r'<div\s+class="decision-header">(?P<header>.*?)</div>', re.DOTALL)
```

Affichage du résultats pour toutes les décisions, et détermination de tous les cas sur les 120 décisions pour la chambre:

```bash
(tp1) gasilber@roya tp_nlp_regexps_mines % get_judilibre parse_html_decisions tp_regexps/data/ccass | grep 'h4-like">' | sort | uniq
          <p class="h4-like">Chambre commerciale financière et économique
          <p class="h4-like">Chambre criminelle
          <p class="h4-like">Chambre sociale
          <p class="h4-like">Deuxième chambre civile
          <p class="h4-like">Première chambre civile
          <p class="h4-like">Première présidence (Ordonnance)
          <p class="h4-like">Troisième chambre civile
```

Construction de la regexp pour la chambre:

```python
chambre_re = re.compile(
	r'(?P<chambre>'
	r'Chambre\scommerciale\sfinancière\set\séconomique'
	r'|Chambre\scriminelle'
	r'|Chambre\ssociale'
	r'|Deuxième\schambre\scivile'
	r'|Première\schambre\scivile'
	r'|Première\sprésidence\s\(Ordonnance\)'
	r'|Troisième\schambre\scivile'
	r')', re.UNICODE
)
```

Après un test avec `parse_judilibre parse_html_decisions tp_regexps/data/ccass` cela semble fonctionner.

Réécriture des fichiers JSON de référence:

```bash
get_judilibre write_test_decisions tp_regexps/data/ccass --force
```

Ajout du test correspondant, et test sur les décisions:

```bash
(tp1) gasilber@roya tp_nlp_regexps_mines % python3 -m unittest tp_regexps/test_regexps.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.060s

OK
```

## Synthèse: Principe de création des regexps

**Il faut être positionné à la racine de votre dépôt Git**

Tests:

```bash
python3 -m unittest tp_regexps/test_regexps.py
```

Parser toutes les décisions:

```bash
parse_judilibre parse_html_decisions tp_regexps/data/ccass
```

Parser une décision:

```bash
parse_judilibre parse_html_decision tp_regexps/data/ccass/67593257db845b438efc6e22.html
```

Quand vous avez trouvé l'expression régulière qui fonctionne pour un attribut, réécrire tous les fichiers JSON de référence, puis vérifier que les tests passent:

```bash
parse_judilibre write_test_decisions tp_regexps/data/ccass --force
```

## Données JSON de référence

Le répertoire `refdata/ccass` contient les fichiers JSON solution partiels, pour les attributs:   `formation`, `publication`, `number`, `ecli`, `decision_date`. Cela vous donne une référence pour la cible que vous devez obtenir.

Après avoir décommenté les tests unitaires dans `test_regexps.py`, vous pouvez mesurer les erreurs avec la commande:

```bash
TP_REGEXP_TEST_REF=refdata python3 -m unittest tp_regexps/test_regexps.py
```
