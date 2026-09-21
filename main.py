"""Point d'entrée : charge les secteurs, les reprojette et affiche les superficies."""

from geo_quality_demo.sectors import compute_areas, load_sectors, reproject, summarize

DATA_PATH = "data/secteurs.geojson"


def main() -> None:
    """Exécute le pipeline complet et affiche le résultat en console."""
    gdf = load_sectors(DATA_PATH)
    gdf = reproject(gdf)
    gdf = compute_areas(gdf)

    print("Résultats :")
    for line in summarize(gdf):
        print(f"  - {line}")


if __name__ == "__main__":
    main()
