from minio import Minio
import random
 
random.seed()

client = Minio("10.42.0.102", access_key='minio', secret_key='miniotest', secure=False)

buckets = client.list_buckets()
bucket_num = random.randrange(len(buckets))
objects = client.list_objects(buckets[bucket_num].name)
objects_list = list(objects)
object_num = random.randrange(len(objects_list))
client.fget_object(buckets[bucket_num].name, objects_list[object_num].object_name,'minio_s3_data.txt')

