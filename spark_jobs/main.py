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
        df.write.mode("overwrite").format("csv").option("path", "staging").save(header=True)
        print("Successfully wrote csv")
    except Exception as e:
        print(e)

    print(os.listdir())
    for file in os.listdir():
        print(file)

    file_list = []
    for path, dirs, files in os.walk("."):
        for filename in files:
            filepath = os.path.join(path,filename)
            if '.csv' in filepath and '/part-' in filepath:
                print(f"found csv: {filepath}")
                file_list.append(filepath)

    # file_list = [file for file in os.listdir("staging") if '.csv' in file and '/part-' in file]
    print(file_list)

    try:
        client = Minio(minio_ip,
            access_key="minio",
            secret_key="minio123",
            secure=False
        )

        source_file = file_list[0]
        bucket_name = "python-test-bucket"
        destination_file = "minio_emps.csv"
        
        found = client.bucket_exists(bucket_name)
        if not found:
            client.make_bucket(bucket_name)
            print("Created bucket", bucket_name)
        else:
            print("Bucket", bucket_name, "already exists")
        
        objects = client.list_objects(bucket_name)
        for obj in objects:
            print(obj)

        try:
            print(f"Uploading file to minio: {source_file} >> {destination_file}")
            result = client.fput_object(
                bucket_name=bucket_name,
                object_name=destination_file,
                file_path=source_file,
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
