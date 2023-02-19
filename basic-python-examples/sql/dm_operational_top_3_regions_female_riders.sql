SELECT name AS region_name, total_trips
  FROM `{project_id}.dwh_bikesharing.fct_daily_by_gender_region` AS fact
  JOIN `{project_id}.dwh_bikesharing.dim_regions` AS dim
       ON fact.region_id = dim.region_id
 WHERE DATE(trip_date) = DATE('2018-01-02')
       AND member_gender = 'Female'
 ORDER BY total_trips DESC
 LIMIT 3;
