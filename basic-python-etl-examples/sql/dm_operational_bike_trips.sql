CREATE VIEW dm_operational.bike_trips_daily AS

SELECT trip_date, SUM(total_trips) as total_trips_daily
  FROM `{project_id}.dwh_bikesharing.fact_trips_daily`
 GROUP BY trip_date;
