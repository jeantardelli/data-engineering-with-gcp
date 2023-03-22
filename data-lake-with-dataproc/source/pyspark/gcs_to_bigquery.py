"""Read data from GCS and store the output into BigQuery"""
import os
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("spark_gcs_to_bigquery").getOrCreate()

sc = spark.sparkContext
sc.setLogLevel("WARN")

DATAPROC_CLUSTER_NAME = os.environ.get("DATAPROC_CLUSTER_NAME")
FILEPATH = os.environ.get("FILEPATH")

GCS_BUCKET_NAME = "-".join(DATAPROC_CLUSTER_NAME.split("-")[:-1])
GCS_BUCKET_NAME += "-" + os.environ.get("GCP_PROJECT_ID")

log_files_rdd = sc.textFile("gs://{}/{}*".format(GCS_BUCKET_NAME, FILEPATH))

# Split the logs with the " " delimiter space; this code line will split each
# record so that we can access the records like an array
splitted_rdd = log_files_rdd.map(lambda x: x.split(" "))
selected_col_rdd = splitted_rdd.map(lambda x: (x[0], x[3], x[5], x[6]))

columns = ["ip", "date", "method", "url"]
logs_df = selected_col_rdd.toDF(columns)
logs_df.createOrReplaceTempView("logs_df")

# access the DataFrame using SQL in Spark
sql = """
    SELECT url,
           COUNT(*) AS count
      FROM logs_df
     WHERE url LIKE '%/article%'
     GROUP BY url
"""

article_count_df = spark.sql(sql)
print(" ### Get only articles and blogs records ### ")
article_count_df.show(5)

article_count_df.write.format("bigquery").option(
    "temporaryGcsBucket", GCS_BUCKET_NAME
).option("table", "dm_content_creators.article_count_df").mode("overwrite").save()
