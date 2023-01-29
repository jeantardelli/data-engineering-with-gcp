CREATE VIEW dm_operational.top_3_region_by_shortest_duration AS

SELECT trip_date,
       region_name,
       SUM(sum_duration_sec) AS total_sum_duration_sec
  FROM `{project-id}.dwh_bikesharing.fct_daily_trips`
  JOIN `{project-id}.dwh_bikesharing.dim_stations`
       ON start_station_id = station_id
 WHERE trip_date = '2018-01-02'
 GROUP BY trip_date, region_name
 ORDER BY total_sum_duration_sec asc
 LIMIT 3;
