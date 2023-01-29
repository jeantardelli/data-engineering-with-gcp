SELECT DATE(start_date) AS trip_date,
       start_station_id,
       COUNT(trip_id) AS total_trips,
       SUM(duration_sec) AS sum_duration_sec,
       AVG(duration_sec) AS avg_duration_sec
  FROM `{project_id}.raw_bikesharing.trips` AS trips
  JOIN `{project_id}.raw_bikesharing.stations` AS stations
       ON trips.start_station_id = stations.station_id
 WhERE DATE(start_date) = DATE('{load_date}')
 GROUP BY trip_date,
       start_station_id;
