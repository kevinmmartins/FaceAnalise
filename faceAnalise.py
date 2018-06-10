import boto3
import json

s3= boto3.resource('s3')
client= boto3.client('rekognition')

def detect_faces():
    faceDetected=client.index_faces(
        CollectionId='faces',
        DetectionAttributes=['DEFAULT'],
        ExternalImageId='TEMPIMAGE',
        Image={
            'S3Object': {
                'Bucket': 'images-tr',
                'Name': '_analise.png',
            }
        }
    )
    return faceDetected;

def create_faceId_list(faces_detected):
    faceId_detected=[]
    for images in range(len(faces_detected['FaceRecords'])):
        faceId_detected.append(faces_detected['faceRecords'][images]['Face']['FaceId'])
    return faceId_detected

def compare_images(faceId_detected):
    compare_result=[]
    for ids in faceId_detected:
        compare_result.append(
            client.searc_faces(
                CollectionId='faces',
                FaceId=ids,
                FaceMatchThreshould=80,
                MaxFaces=10.
            )
        )
    return compare_result

faces_detected= detect_faces()
print(json.dumps(faces_detected,indent=4))
face_id_list=create_faceId_list(faces_detected)
compare_result=compare_images(face_id_list)
print(json.dumps(compare_result,indent=4))