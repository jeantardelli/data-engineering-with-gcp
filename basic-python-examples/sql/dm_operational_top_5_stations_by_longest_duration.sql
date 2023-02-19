CREATE VIEW dm_operational.top_5_station_by_longest_duration AS

SELECT trip_date,
       station_name,
       sum_duration_sec
  FROM `{project_id}.dwh_bikesharing.fct_daily_trips`
  JOIN `{project_id}.dwh_bikesharing.dim_stations`
       ON start_station_id = station_id
 WHERE trip_date = '2018-01-02'
 ORDER BY sum_duration_sec desc
 LIMIT 5;
