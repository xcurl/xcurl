#bp2
from pyspark import SparkContext

sc = SparkContext() 

x = sc.parallelize([("spark", 1), ("hadoop", 4)])

y = sc.parallelize([("spark", 2), ("hadoop", 5)]) 

joined_rdd = x.join(y) 

result = sorted(joined_rdd.collect()) 

print(result)

sc.stop()


#if first line doesn'r work then : use 
#from pyspark.sql import SparkSession
#spark = SparkSession.builder.appName("WorkCount").getOrCreate()
#sc = spark.sparkContext
