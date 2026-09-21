# geo-quality-demo

Petit projet géomatique pour illustrer les outils de qualité de code
vus en classe : **Black**, **Ruff**, **interrogate**, **pre-commit**,
**pytest** et l'intégration continue avec **GitHub Actions**.

## Contenu du dépôt

```
geo-quality-demo/
├── .github/workflows/
│   └── ci.yml                 ← vérifie tout à chaque push (voir plus bas)
├── src/geo_quality_demo/
│   ├── __init__.py
│   └── sectors.py             ← code "propre" : docstrings, types, testé
├── tests/
│   └── test_sectors.py        ← tests unitaires (pytest)
├── examples/
│   ├── avant.py                ← code volontairement mal formaté
│   └── apres.py                ← ce que Black + Ruff en feraient
├── data/
│   └── secteurs.geojson
├── main.py
├── pyproject.toml              ← configuration de Black, Ruff, interrogate, pytest
├── .pre-commit-config.yaml
├── requirements.txt            ← dépendances d'exécution
└── README.md
```

`examples/` est volontairement exclu des vérifications automatiques
(voir `pyproject.toml`) — c'est du code de démonstration, pas du code
de production.

## Installation

```bash
git clone <url-du-depot>
cd geo-quality-demo
pip install -e ".[dev]"
```

`-e` signifie "editable" : le projet est installé en mode développement,
ce qui permet de modifier les fichiers du dépôt et de les utiliser
immédiatement sans réinstaller à chaque fois. `.[dev]` indique que
l’on installe aussi les dépendances de développement définies dans le
`pyproject.toml` (Black, Ruff, pytest, pre-commit, etc.).

Ceci installe à la fois les dépendances d'exécution (GeoPandas...) et
les outils de qualité (Black, Ruff, interrogate, pytest, pre-commit).

## Pour démarrer un repo de ce type

1. Créer la structure du projet : `src/mon_projet/`, `tests/`, `.github/workflows/`, `README.md`.
2. Définir les dépendances dans `pyproject.toml` : paquet principal, runtime dependencies et optional dependencies `dev`.
3. Ajouter les outils de qualité dans les sections `[tool.black]`, `[tool.ruff]`, `[tool.interrogate]` et `[tool.pytest.ini_options]`.
4. Écrire une première version propre du code, avec docstrings, types et fonctions bien nommées.
5. Écrire des tests avec `pytest` avant d’étendre le projet.
6. Installer le projet en mode développement avec `pip install -e ".[dev]"`.
7. Vérifier manuellement : `black --check .`, `ruff check .`, `interrogate`, `pytest -v`.
8. Installer `pre-commit` et configurer le hook : `pre-commit install`.
9. Ajouter une CI GitHub Actions pour exécuter ces vérifications à chaque `push` et `pull request`.
10. Itérer sur les retours d’outils et corriger les problèmes avant de valider le code.

## Le principe de `pyproject.toml`

`pyproject.toml` est le fichier central de configuration d’un projet Python moderne.
Il remplace progressivement les anciens fichiers comme `setup.py` ou `requirements.txt`
pour centraliser :

- le nom du projet et sa version,
- les dépendances du package,
- les dépendances de développement,
- la configuration des outils comme Black, Ruff, pytest et interrogate.

C’est donc le point d’entrée pour dire à Python et aux outils de qualité
comment le projet doit être installé et vérifié.

Un début de fichier ressemble souvent à ceci :

```toml
[project]
name = "mon-projet"
version = "0.1.0"
description = "Mon projet"
requires-python = ">=3.11"

[project.optional-dependencies]
dev = [
    "black",
    "ruff",
    "pytest",
]

[tool.black]
line-length = 88

[tool.ruff]
line-length = 88

[tool.pytest.ini_options]
pythonpath = ["src"]
```

Pour le construire, il faut commencer par :

1. donner le nom du projet et la version ;
2. déclarer les dépendances de runtime ;
3. créer une section `dev` pour les outils de développement ;
4. ajouter les blocs `[tool.black]`, `[tool.ruff]`, `[tool.pytest.ini_options]`, etc. ;
5. tester la configuration avec les commandes du projet.

C’est le fichier qui permet d’exécuter des commandes comme `pip install -e ".[dev]"`,
`black --check .`, `ruff check .` et `pytest` dans un environnement cohérent.

## Les outils, un par un

### Black — formatage automatique

```bash
black .                 # reformate tous les fichiers
black --check .         # vérifie sans modifier (utilisé en CI)
black --diff examples/avant.py   # montre ce qui changerait
```

### Ruff — linting

```bash
ruff check .             # signale les problèmes
ruff check --fix .       # corrige automatiquement ce qui peut l'être
ruff check examples/avant.py     # démonstration sur le fichier "avant"
```

### interrogate — couverture de documentation

```bash
interrogate               # utilise la configuration de pyproject.toml
interrogate -v             # détail fonction par fonction
```

Le seuil est fixé à 80 % dans `pyproject.toml` (`fail-under = 80`) —
`src/` et `main.py` sont actuellement à 100 %.

### pytest — tests unitaires

```bash
pytest -v
```

Les tests dans `tests/test_sectors.py` couvrent `compute_areas`,
`reproject` et `summarize`, sans dépendre du fichier `data/secteurs.geojson`
(les données de test sont construites directement dans le fichier de
test).

### pre-commit — tout exécuter automatiquement à chaque commit

```bash
pre-commit install        # une seule fois, après le clone
git commit -m "..."       # Black, Ruff et interrogate s'exécutent automatiquement
```

Si une vérification échoue, le commit est bloqué tant que le problème
n'est pas corrigé.

## Intégration continue (GitHub Actions)

Le fichier `.github/workflows/ci.yml` exécute, à chaque `push` et
chaque *pull request* :

1. `black --check .`
2. `ruff check .`
3. `interrogate`
4. `pytest -v`

Si l'une de ces étapes échoue, GitHub affiche un ❌ sur le commit ou
la *pull request* concernée — avant même qu'un humain n'ait besoin de
relire le code en détail.

## Essayer la démonstration avant/après

```bash
ruff check examples/avant.py     # affiche : import inutilisé (os)
black --diff examples/avant.py   # affiche le reformatage proposé
diff examples/avant.py examples/apres.py
```

## Commandes de démonstration rapide

```bash
# 1. Vérifier le formatage
black --check .

# 2. Réformer automatiquement
black .

# 3. Lancer le linter
ruff check .

# 4. Corriger automatiquement ce que Ruff peut corriger
ruff check --fix .

# 5. Vérifier la documentation de code
interrogate

# 6. Lancer les tests unitaires
pytest -v

# 7. Simuler la CI locale
black --check . && ruff check . && interrogate && pytest -v

# 8. Voir les modifications apportées par Black
black --diff examples/avant.py

# 9. Comparer le code avant/après
 diff examples/avant.py examples/apres.py
```

Ces commandes sont parfaites pour montrer, en live, la différence entre
un code non conforme et un code validé par les outils de qualité.
