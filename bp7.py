# Import required modules
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

# i. Initialize SparkSession
spark = SparkSession.builder.appName("CapitalizeUDF").getOrCreate()

data = [("1", "john jones"), ("2", "tracey smith"), ("3", " amy sanders")]
columns = ["Seqno", "Name"]

rdd = spark.sparkContext.parallelize(data) 

df = spark.createDataFrame(rdd, schema=columns) 
print("ii. Original DataFrame:")
df.show(truncate=False)

def capitalize_name(name):
    if name is None:
        return None
    return ' '.join(word.capitalize() for word in name.strip().split())

capitalize_udf = udf(capitalize_name, StringType()) 

result_df = df.withColumn("Capitalized_Name", capitalize_udf(col("Name")))

print("iv. After applying UDF (first letter capitalized):")
result_df.select("Seqno", "Name", "Capitalized_Name").show(truncate=False)

spark.stop()
