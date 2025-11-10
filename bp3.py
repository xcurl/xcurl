#bp3
from pyspark import SparkContext

sc = SparkContext()

data = [{1, 2, 3}, {4, 5, 6}, {7, 8, 9}]
rdd = sc.parallelize(data)  

acc = sc.accumulator(0) 

def add_to_acc(number_set):
    acc.add(sum(number_set)) 

rdd.foreach(add_to_acc)

print("Sum of numbers in RDD:", acc.value)

sc.stop()
