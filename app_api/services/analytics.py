from app_api.db.my_sql import mysql_service


# 2
def signal_sources_analysis():
    query = """
            SELECT signal_type, COUNT(*) AS count
            FROM intel_signals
            GROUP BY signal_type
            ORDER BY count DESC;
            """
    result = mysql_service.execute_query(query=query, params=None, fetch=True)
    return result


# 4
def sleeper_cells():
    # query = """
    #         WITH signal_steps AS (SELECT *,
    #                                      LAG(reported_lat) OVER (PARTITION BY entity_id ORDER BY timestamp) AS prev_lat,
    #                                      LAG(reported_lon) OVER (PARTITION BY entity_id ORDER BY timestamp) AS prev_lon,
    #                                      LAG(timestamp) OVER (PARTITION BY entity_id ORDER BY timestamp)    AS prev_time
    #                               FROM intel_signals),
    #              calc_distances AS (SELECT *,
    #                                        DATE(DATE_SUB(timestamp, INTERVAL 8 HOUR))           AS shift_date,
    #                                        ST_Distance_Sphere(POINT(reported_lon, reported_lat),
    #                                                           POINT(prev_lon, prev_lat)) / 1000 AS dist_km,
    #                                        TIMESTAMPDIFF(SECOND, prev_time, timestamp)          AS gap_seconds
    #                                 FROM signal_steps
    #                                 WHERE prev_time IS NOT NULL),
    #              daily_aggregates AS (SELECT entity_id,
    #                                          shift_date,
    #                                          SUM(IF(HOUR(timestamp) >= 8 AND HOUR(timestamp) < 20, dist_km, 0)) AS day_dist,
    #                                          SUM(IF(HOUR(timestamp) >= 20 OR HOUR(timestamp) < 8, dist_km, 0))  AS night_dist
    #                                   FROM calc_distances
    #                                   GROUP BY entity_id, shift_date)
    #         SELECT entity_id
    #         FROM daily_aggregates
    #         WHERE day_dist = 0
    #           AND night_dist >= 10;
    #         """

    query = """SELECT entity_id
               FROM (SELECT entity_id,
                            DATE(DATE_SUB(timestamp, INTERVAL 8 HOUR))                                    AS shift_date,
                            SUM(IF(HOUR(timestamp) >= 8 AND HOUR(timestamp) < 20, distance_from_last, 0)) AS day_dist,
                            SUM(IF(HOUR(timestamp) >= 20 OR HOUR(timestamp) < 8, distance_from_last, 0))  AS night_dist
                     FROM intel_signals
                     GROUP BY entity_id, shift_date) AS daily_summary
               WHERE day_dist = 0
                 AND night_dist >= 10;"""
    result = mysql_service.execute_query(query=query, params=None, fetch=True)
    return result
