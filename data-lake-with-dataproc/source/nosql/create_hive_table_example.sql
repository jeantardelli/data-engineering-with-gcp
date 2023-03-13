/* Drop existing table */
DROP TABLE IF EXISTS simple_table;

/* Creates external table */
CREATE EXTERNAL TABLE simple_table (
	col_1 STRING,
	col_2 STRING,
	col_3 STRING)
   ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE location '/data/source/csv/'
       TBLPROPERTIES ("skip.header.line.count"="1");

/* Selects data */
SELECT * FROM simple_table;
