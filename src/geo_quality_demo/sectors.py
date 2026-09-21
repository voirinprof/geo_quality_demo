"""Fonctions de traitement des secteurs géographiques.

Ce module illustre un code respectant les standards attendus dans le
cours : docstrings systématiques, indices de type, une fonction par
responsabilité, aucun paramètre codé en dur.
"""

from __future__ import annotations

import geopandas as gpd

TARGET_CRS = "EPSG:32198"  # MTM Québec, CRS cible du cours


def load_sectors(path: str) -> gpd.GeoDataFrame:
    """Charge les secteurs depuis un fichier GeoJSON.

    Args:
        path: Chemin vers le fichier GeoJSON à lire.

    Returns:
        Le GeoDataFrame des secteurs, dans son CRS d'origine.
    """
    return gpd.read_file(path)


def reproject(gdf: gpd.GeoDataFrame, target_crs: str = TARGET_CRS) -> gpd.GeoDataFrame:
    """Reprojette un GeoDataFrame vers le CRS cible.

    Args:
        gdf: Le GeoDataFrame à reprojeter.
        target_crs: Le code EPSG du CRS cible.

    Returns:
        Une copie reprojetée du GeoDataFrame.
    """
    return gdf.to_crs(target_crs)


def compute_areas(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Calcule la superficie de chaque géométrie, en kilomètres carrés.

    Suppose que gdf est déjà dans un CRS projeté (mètres).

    Args:
        gdf: Le GeoDataFrame dont on calcule les superficies.

    Returns:
        Une copie de gdf avec une colonne supplémentaire "superficie_km2".
    """
    result = gdf.copy()
    result["superficie_km2"] = result.geometry.area / 1_000_000
    return result


def summarize(gdf: gpd.GeoDataFrame, name_column: str = "nom") -> list[str]:
    """Construit des lignes de résumé lisibles pour chaque secteur.

    Args:
        gdf: Le GeoDataFrame contenant une colonne "superficie_km2".
        name_column: Le nom de la colonne contenant le nom du secteur.

    Returns:
        Une liste de chaînes formatées, une par secteur.
    """
    lines = []
    for _, row in gdf.iterrows():
        lines.append(f"{row[name_column]:<15} {row['superficie_km2']:.2f} km²")
    return lines
