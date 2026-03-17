from app_api.db.my_sql import mysql_service


# 1
def high_value_target_movement():
    query = """
            SELECT entity_id, target_name, priority_level, movement_distance_km
            FROM targets
            WHERE priority_level IN (1, 2)
              AND movement_distance_km > 5.0;
            """
    result = mysql_service.execute_query(query=query, params=None, fetch=True)
    return result


# 3
def new_targets():
    query = """
            SELECT entity_id, COUNT(*) AS report_count
            FROM intel_signals
            WHERE priority_level = 99
            GROUP BY entity_id
            ORDER BY COUNT(*) DESC
            LIMIT 3;
            """
    result = mysql_service.execute_query(query=query, params=None, fetch=True)
    return result
