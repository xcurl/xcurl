# Import SparkContext from pyspark
from pyspark import SparkContext

# a. Create a SparkContext object
sc = SparkContext("local", "WordCountApp")  # Initialize SparkContext with local mode and app name

# b. Create RDD using parallelize() from list of words
words = ["scala", "java", "hadoop", "spark", "akka", "spark vs hadoop", "pyspark", "pyspark and spark"]
rdd = sc.parallelize(words)  # Distribute the list into an RDD

# c. Find total count of words in RDD
total_count = rdd.count()  # Action: returns number of elements in RDD
print("Word count is %d" % total_count)  # Print total count

# d. Filter strings containing "spark" and collect results
spark_words_rdd = rdd.filter(lambda x: "spark" in x.lower())  # Transformation: filter rows with "spark"
spark_words = spark_words_rdd.collect()  # Action: bring filtered data to driver
print("Filtered RDD: %s" % spark_words)  # Print filtered list

# Stop the SparkContext
sc.stop()  # Gracefully stop the context
