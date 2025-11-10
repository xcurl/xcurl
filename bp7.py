from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

spark = SparkSession.builder.appName("CapitalizeUDF").getOrCreate()

data = [("1", "john jones"), ("2", "tracey smith"), ("3", " amy sanders")]
columns = ["Seqno", "Name"]

rdd = spark.sparkContext.parallelize(data)

df = spark.createDataFrame(rdd, schema=columns)

def capitalize_name(name):
    return name.strip().title() if name else None

capitalize_udf = udf(capitalize_name, StringType())

result_df = df.withColumn("Capitalized_Name", capitalize_udf(col("Name")))

result_df.select("Seqno", "Name", "Capitalized_Name").show(truncate=False)

spark.stop()
