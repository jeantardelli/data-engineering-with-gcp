SELECT DATE(start_date) as trip_date,
       region_id,
       member_gender,
       COUNT(trip_id) as total_trips
  FROM `{project_id}.raw_bikesharing.trips` trips
  JOIN `{project_id}.raw_bikesharing.stations` stations
       ON trips.start_station_id = stations.station_id
       WHERE DATE(start_date) = DATE('{load_date}') AND member_gender IS NOT NULL
 GROUP BY trip_date, region_id, member_gender;
