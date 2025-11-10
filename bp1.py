#bp1
from pyspark import SparkContext


sc = SparkContext("local", "WordCountApp") 


words = ["scala", "java", "hadoop", "spark", "akka", "spark vs hadoop", "pyspark", "pyspark and spark"]
rdd = sc.parallelize(words) 


total_count = rdd.count() 
print("Word count is %d" % total_count)  


spark_words_rdd = rdd.filter(lambda x: "spark" in x.lower())  
spark_words = spark_words_rdd.collect() 
print("Filtered RDD: %s" % spark_words) 


sc.stop() 
