#bp4
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("CSV_RDD_Stats").getOrCreate()

df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load("proper file path")  

rdd = df.rdd  

print("Top 5 rows from RDD:")
print(rdd.take(5))

print("\nStatistical Summary (Numerical Columns Only):")
df.describe().show()

spark.stop()
