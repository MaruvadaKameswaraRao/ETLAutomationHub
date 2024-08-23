from pyspark.sql import SparkSession
from pyspark.sql.types import StructType,StructField,StringType,IntegerType

spark = SparkSession.builder.appName('google_playstore_data_analysis').getOrCreate()

df = spark.read.csv('googlestore.csv', header=True, inferSchema=True,escape='"')

df.show()




