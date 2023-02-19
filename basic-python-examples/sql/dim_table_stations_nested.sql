CREATE OR REPLACE TABLE `dwh_bikesharing.dim_stations_nested` AS

SELECT regions.region_id,
       regions.name as region_name,
       ARRAY_AGG(stations) as stations
 FROM `{project_id}.raw_bikesharing.regions` AS regions
 JOIN `{project_id}.raw_bikesharing.stations` AS stations
      ON CAST(regions.region_id AS STRING) = stations.region_id
GROUP BY regions.region_id,
         regions.name
