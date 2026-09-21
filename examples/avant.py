"""Exemple "avant" — volontairement mal formaté, à but pédagogique.

Ce dossier (examples/) est exclu de Black/Ruff/interrogate (voir
pyproject.toml) : il sert à démontrer ce que ces outils détectent,
pas à respecter leurs règles. Essayez en classe :

    ruff check examples/avant.py
    black --diff examples/avant.py

Comparez ensuite avec examples/apres.py.
"""

import os


def calc(a,b):
  return a+b


x={'a':1,'b':2}
