"""Read data from HDFS and store the output back in HDFS"""
import os
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("spark_hdfs_to_hdfs").getOrCreate()

sc = spark.sparkContext
sc.setLogLevel("WARN")

DATAPROC_CLUSTER_NAME = os.environ.get("DATAPROC_CLUSTER_NAME")
FILEPATH = os.environ.get("FILEPATH")

log_files_rdd = sc.textFile(
    "hdfs://{}/data/{}*".format(DATAPROC_CLUSTER_NAME, FILEPATH)
)

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

article_count_df.write.save(
    "hdfs://{}/data/from-pyspark/article_count_df".format(DATAPROC_CLUSTER_NAME),
    format="csv",
    mode="overwrite",
)
