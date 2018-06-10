import boto3

s3= boto3.resource('s3')
client= boto3.client('rekognition')

def list_images():
    images=[]
    bucket= s3.Bucket('images-tr')
    for image in bucket.objects.all():
        images.append(image.key)
    return images;

def create_images_index_list(images):
    for imageV in images:
        client.index_faces(
            CollectionId='faces',
            DetectionAttributes=[
            ],
            ExternalImageId=imageV[:-4],
            Image={
                'S3Object':{
                    'Bucket': 'images-t',
                    'Name':imageV,
                }
            }
        )

imagesFromS3 = list_images()
create_images_index_list(imagesFromS3)