#bp5
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("WordCountFromFile").getOrCreate()


text_df = spark.read.text("sample.txt")

text_rdd = text_df.rdd 

words_rdd = text_rdd.flatMap(lambda row: row.value.lower().split())

total_words = words_rdd.count()

print(f"Total number of words in the file: {total_words}")

print("First 10 words:", words_rdd.take(10))

spark.stop()
