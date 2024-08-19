import os
import sys
from minio import Minio
from pyspark.sql import SparkSession

if __name__ == '__main__':

    spark = SparkSession.builder \
        .appName("minikubeSpark") \
            .master("local") \
            .enableHiveSupport() \
            .getOrCreate()
    
    minio_ip = sys.argv[1]
    print(f"minio ip: {minio_ip}")
    staging_folder = "staging"
    bucket_name = "python-test-bucket"
    destination_file = "minio_emps.csv"

    df = spark.createDataFrame(
        [
            ("sue", 32),
            ("li", 3),
            ("bob", 75),
            ("heo", 13),
            ("test", 99),
        ],
        ["first_name", "age"],
    )

    df.show()

    try:
        df.write.mode("overwrite").format("csv").option("path", staging_folder).save(header=True)
        print("Successfully wrote df to csv")
    except Exception as e:
        print(e)

    spark_csv_list = []
    for path, dirs, files in os.walk(f"./{staging_folder}"):
        for filename in files:
            filepath = os.path.join(path,filename)
            if '.csv' in filepath and '/part-' in filepath:
                print(f"found csv: {filepath}")
                spark_csv_list.append(filepath)

    # file_list = [file for file in os.listdir("staging") if '.csv' in file and '/part-' in file]

    try:
        client = Minio(minio_ip,
            access_key="minio",
            secret_key="minio123",
            secure=False
        )
        
        found = client.bucket_exists(bucket_name)
        if not found:
            client.make_bucket(bucket_name)
            print(f"created bucket: {bucket_name}")
        else:
            print(f"bucket: {bucket_name} already exists")

        for index, csv_filepath in enumerate(spark_csv_list):
            try:
                destination_file = f"{index}_{destination_file}"
                print(f"uploading file to minio: {csv_filepath} >> {destination_file}")
                result = client.fput_object(
                    bucket_name=bucket_name,
                    object_name=destination_file,
                    file_path=csv_filepath,
                    content_type="application/csv",
                )
                print(
                    "created {0} object; etag: {1}, version-id: {2}".format(
                        result.object_name, result.etag, result.version_id,
                    ),
                )
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

    spark.stop()
