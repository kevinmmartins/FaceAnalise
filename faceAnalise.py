import boto3
import json

s3= boto3.resource('s3')
client= boto3.client('rekognition')

def detectFaces():
    faceDetected=client.index_faces(
        CollectionId='faces',
        DetectionAttributes=['DEFAULT'],
        ExternalImageId='TEMPIMAGE',
        Image={
            'S3Object': {
                'Bucket': 'images-t',
                'Name': '_analise.png',
            }
        }
    )
    return faceDetected;

faces_detected= detectFaces()
print(json.dumps(faces_detected,indent=4))