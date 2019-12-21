#! python3
# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("PySpark example").enableHiveSupport().getOrCreate()
spark.sparkContext.setLogLevel("WARN")
# Read data
df = spark.sql("SELECT img_label FROM sprs_log_basis.model_server_log WHERE datepart=20190425 LIMIT 10")
df.cache()
df.show()
# Get keys
df = df.select(F.map_keys("img_label").alias("keys"))
# Assign index
df = df.withColumn("doc_id", F.monotonically_increasing_id())
NUM_doc = df.count()
# One hot words
df = df.select('*', F.explode('keys').alias('token'))
df.show()
# Calculate TF
TF = df.groupBy("doc_id").agg(F.count("token").alias("doc_len")) \
    .join(df.groupBy("doc_id", "token")
          .agg(F.count("keys").alias("word_count")), ['doc_id']) \
    .withColumn("tf", F.col("word_count") / F.col("doc_len")) \
    .drop("doc_len", "word_count")
TF.cache()
# Calculate IDF
IDF = df.groupBy("token").agg(F.countDistinct("doc_id").alias("df"))
IDF = IDF.select('*', (F.log(NUM_doc / (IDF['df'] + 1))).alias('idf'))
IDF.cache()
# Calculate TF-IDF
TFIDF = TF.join(IDF, ['token']).withColumn('tf-idf', F.col('tf') * F.col('idf'))
TFIDF.show()
TFIDF.write.save("s3://***.tmp.ap-southeast-1/Default/hailin/here.csv", format='csv', header=True)
