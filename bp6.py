# Import necessary modules
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, sum as _sum

spark = SparkSession.builder.appName("EmployeeStateSalary").getOrCreate()

data = [
    ("James","Sales","NY",90000,34,10000),
    ("Michael","Sales","NV",86000,56,20000),
    ("Robert","Sales","CA",81000,30,23000),
    ("Maria","Finance","CA",90000,24,23000),
    ("Raman","Finance","DE",99000,40,24000),
    ("Scott","Finance","NY",83000,36,19000),
    ("Jen","Finance","NY",79000,53,15000),
    ("Jeff","Marketing","NV",80000,25,18000),
    ("Kumar","Marketing","NJ",91000,50,21000)
]

schema = ["employee_name","department","state","salary","age","bonus"]

rdd = spark.sparkContext.parallelize(data) 

df = spark.createDataFrame(rdd, schema)  ]

print("iii. State-wise total salaries:")
state_salary_df = df.groupBy("state").agg(_sum("salary").alias("total_salary"))
state_salary_df.show()

print("iv. States with total salary > 1 lakh:")
filtered_df = state_salary_df.filter(col("total_salary") > 100000)
filtered_df.show()

print("v. State-wise salaries in descending order:")
final_df = filtered_df.orderBy(col("total_salary").desc())
final_df.show()

spark.stop()
