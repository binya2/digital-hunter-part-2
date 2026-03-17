from app_api.db.my_sql import mysql_service


def escape_patterns():
    query = """
            WITH movement_details AS (SELECT entity_id,
                                             timestamp,
                                             (distance_from_last /
                                              NULLIF(TIMESTAMPDIFF(SECOND,
                                                                   LAG(timestamp) OVER (PARTITION BY entity_id ORDER BY timestamp),
                                                                   timestamp), 0))
                                                 * 3.6 AS speed_kmh
                                      FROM intel_signals),
                 targeted_attacks AS (SELECT a.attack_id,
                                             a.entity_id,
                                             a.timestamp AS attack_time
                                      FROM attacks a
                                               JOIN damage_assessments d ON a.attack_id = d.attack_id
                                      WHERE d.result != 'destroyed'),
                 signals_around_attack AS (SELECT ta.attack_id,
                                                  ta.entity_id,
                                                  ta.attack_time,
                                                  md.speed_kmh,
                                                  md.timestamp AS signal_time
                                           FROM targeted_attacks ta
                                                    JOIN movement_details md ON ta.entity_id = md.entity_id
                                           WHERE md.timestamp BETWEEN DATE_SUB(ta.attack_time, INTERVAL 3 HOUR)
                                                     AND DATE_ADD(ta.attack_time, INTERVAL 3 HOUR)),
                 final_analysis AS (SELECT attack_id,
                                           entity_id,
                                           AVG(CASE WHEN signal_time < attack_time THEN speed_kmh END)  AS avg_speed_before,
                                           AVG(CASE WHEN signal_time >= attack_time THEN speed_kmh END) AS avg_speed_after
                                    FROM signals_around_attack
                                    GROUP BY attack_id, entity_id)
            SELECT entity_id,
                   ROUND(avg_speed_before, 2) AS avg_speed_before,
                   ROUND(avg_speed_after, 2)  AS avg_speed_after,
                   ROUND(((avg_speed_after - avg_speed_before) / NULLIF(avg_speed_before, 0)) * 100,
                         2)                   AS percentage_change
            FROM final_analysis
            WHERE avg_speed_after >= avg_speed_before * 1.5;
            """
    result = mysql_service.execute_query(query=query, params=None, fetch=True)
    return result


def meeting_events():
    query = """
            WITH high_value_targets AS (SELECT s.entity_id,
                                               s.timestamp,
                                               s.reported_lat,
                                               s.reported_lon
                                        FROM intel_signals s
                                                 JOIN targets t ON s.entity_id = t.entity_id
                                        WHERE t.priority_level = 1),
                 unknown_entities AS (SELECT s.entity_id,
                                             s.timestamp,
                                             s.reported_lat,
                                             s.reported_lon
                                      FROM intel_signals s
                                               LEFT JOIN targets t ON s.entity_id = t.entity_id
                                      WHERE t.entity_id IS NULL)
            
            SELECT h.entity_id AS entity_id_priority,
                   u.entity_id AS entity_id_asset,
                   h.timestamp AS meeting_time,
                   ROUND(ST_Distance_Sphere(
                                 POINT(h.reported_lon, h.reported_lat),
                                 POINT(u.reported_lon, u.reported_lat)
                         ), 2) AS distance_meters
            FROM high_value_targets h
                     JOIN unknown_entities u
                          ON ABS(TIMESTAMPDIFF(SECOND, h.timestamp, u.timestamp)) <= 600
            WHERE ST_Distance_Sphere(
                          POINT(h.reported_lon, h.reported_lat),
                          POINT(u.reported_lon, u.reported_lat)
                  ) <= 1000
            ORDER BY meeting_time DESC;
            """
    result = mysql_service.execute_query(query=query, params=None, fetch=True)
    return result
