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
                   ROUND(avg_speed_before, 2)                                                           AS avg_speed_before,
                   ROUND(avg_speed_after, 2)                                                            AS avg_speed_after,
                   ROUND(((avg_speed_after - avg_speed_before) / NULLIF(avg_speed_before, 0)) * 100,
                         2)                                                                             AS percentage_change
            FROM final_analysis
            WHERE avg_speed_after >= avg_speed_before * 1.5;
            """
    result = mysql_service.execute_query(query=query, params=None, fetch=True)
    return result