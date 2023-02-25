SELECT station_id,
       stations.name as station_name,
       regions.name as region_name,
       capacity
  FROM `{project_id}.raw_bikesharing.stations` AS stations
  JOIN `{project_id}.raw_bikesharing.regions` AS regions
       ON stations.region_id = CAST(regions.region_id AS STRING);
