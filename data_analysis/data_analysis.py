from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import regexp_replace, col

# Create a SparkSession
spark = SparkSession.builder.appName('google_playstore_data_analysis').getOrCreate()

# Load the CSV file into a DataFrame
df = spark.read.csv('googlestore.csv', header=True, inferSchema=True, escape='"')

# Data cleaning and transformation
df = df.withColumn("Reviews", col("Reviews").cast(IntegerType())) \
       .withColumn("Installs", regexp_replace(col("Installs"), "[^0-9]", "").cast(IntegerType())) \
       .withColumn("Price", regexp_replace(col("Price"), "[$]", "").cast(IntegerType()))

# Create a temporary view to run SQL queries on the DataFrame
df.createOrReplaceTempView("apps")

# Top Reviews given to the app
df_review = spark.sql("""
    SELECT app, 
           SUM(reviews) AS total_reviews 
    FROM apps 
    GROUP BY app 
    ORDER BY total_reviews DESC
""")
df_review.show()

# Top 10 installed apps
df_installed = spark.sql("""
    SELECT app, 
           Type, 
           SUM(Installs) AS total_installs 
    FROM apps 
    GROUP BY app, Type 
    ORDER BY total_installs DESC
""")
df_installed.show()

# Category-wise distribution of installs
df_category = spark.sql("""
    SELECT Category, 
           SUM(Installs) AS total_installs 
    FROM apps 
    GROUP BY Category 
    ORDER BY total_installs DESC
""")
df_category.show()

# Top paid apps by total price
df_top_paid = spark.sql("""
    SELECT app, 
           SUM(price) AS total_price 
    FROM apps 
    WHERE Type = 'Paid' 
    GROUP BY app 
    ORDER BY total_price DESC
""")
df_top_paid.show()
