from pyspark.sql import SparkSession

if __name__ == '__main__':

    spark = SparkSession.builder \
        .appName("minikubeSpark") \
            .master("local") \
            .enableHiveSupport() \
            .getOrCreate()

    df = spark.createDataFrame(
        [
            ("sue", 32),
            ("li", 3),
            ("bob", 75),
            ("heo", 13),
        ],
        ["first_name", "age"],
    )

    df.show()
    spark.stop()
