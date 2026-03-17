import io
from pathlib import Path

from matplotlib import pyplot as plt

from app_api.db.my_sql import mysql_service
from app_api.maps_data.DigitalHunter_map import plot_map_with_geometry


def generate_target_path_map(entity_id: str):
    query = """
            SELECT reported_lon, reported_lat
            FROM intel_signals
            WHERE entity_id = %s
            ORDER BY timestamp;
            """
    points = mysql_service.execute_query(query=query, params=(entity_id,), fetch=True)
    if not points:
        return None

    coords = [(p['reported_lon'], p['reported_lat']) for p in points]

    shapefile_path = Path(__file__).resolve().parent.parent / 'maps_data' / 'ne_50m_admin_0_countries.shp'
    plot_map_with_geometry(coords, shapefile_path=str(shapefile_path))

    if len(coords) > 1:
        start_lon, start_lat = coords[0]
        end_lon, end_lat = coords[-1]

        plt.scatter(start_lon, start_lat, color='green', s=100, label='Start', zorder=5)
        plt.scatter(end_lon, end_lat, color='red', s=100, label='End', zorder=5)
        plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    plt.close()
    return buf.getvalue()
