"""Tests unitaires pour geo_quality_demo.sectors."""

import geopandas as gpd
from shapely.geometry import box

from geo_quality_demo.sectors import compute_areas, reproject, summarize


def make_sample_gdf() -> gpd.GeoDataFrame:
    """Construit un petit GeoDataFrame de test, sans dépendre d'un fichier."""
    geometries = [box(0, 0, 1000, 1000), box(0, 0, 2000, 500)]  # mètres
    return gpd.GeoDataFrame(
        {"nom": ["Carré", "Rectangle"]},
        geometry=geometries,
        crs="EPSG:32198",
    )


def test_compute_areas_adds_column():
    """compute_areas doit ajouter une colonne superficie_km2."""
    gdf = make_sample_gdf()
    result = compute_areas(gdf)
    assert "superficie_km2" in result.columns


def test_compute_areas_values_are_correct():
    """Un carré de 1000 x 1000 m fait 1 km²."""
    gdf = make_sample_gdf()
    result = compute_areas(gdf)
    assert result.loc[0, "superficie_km2"] == 1.0


def test_compute_areas_does_not_mutate_input():
    """compute_areas ne doit pas modifier le GeoDataFrame d'origine."""
    gdf = make_sample_gdf()
    compute_areas(gdf)
    assert "superficie_km2" not in gdf.columns


def test_reproject_changes_crs():
    """reproject doit changer le CRS vers la cible demandée."""
    gdf = make_sample_gdf().set_crs("EPSG:4326", allow_override=True)
    result = reproject(gdf, target_crs="EPSG:32198")
    assert result.crs.to_string() == "EPSG:32198"


def test_summarize_formats_one_line_per_row():
    """summarize doit retourner une ligne de texte par secteur."""
    gdf = compute_areas(make_sample_gdf())
    lines = summarize(gdf)
    assert len(lines) == 2
    assert "Carré" in lines[0]
