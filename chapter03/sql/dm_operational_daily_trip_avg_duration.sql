CREATE VIEW dm_operational.daily_avg_trip_duration AS

SELECT trip_date,
       ROUND(AVG(avg_duration_sec)) as daily_average_duration_sec
  FROM `{project_id}.dwh_bikesharing.fct_daily_trips`
 GROUP BY trip_date;
