from google.cloud import storage

def quicktext():
    print('Hello, Welcome To Serverless Cloud Agnostic Python Package.')



def move_file(cloud,bucket_name, blob_name, destination_bucket_name, destination_blob_name,):
    if cloud == "GCP":
        storage_client = storage.Client()
        source_bucket = storage_client.bucket(bucket_name)
        source_blob = source_bucket.blob(blob_name)
        destination_bucket = storage_client.bucket(destination_bucket_name)
        destination_generation_match_precondition = 0

        blob_copy = source_bucket.copy_blob(source_blob, destination_bucket, destination_blob_name, if_generation_match=destination_generation_match_precondition,)
        source_bucket.delete_blob(blob_name)

        print(
        "Blob {} in bucket {} moved to blob {} in bucket {}.".format(
            source_blob.name,
            source_bucket.name,
            blob_copy.name,
            destination_bucket.name,
        )
    )

    elif cloud == "AWS":
        print("AWS package needed")
