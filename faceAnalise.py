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

def create_json_data(compare_result):
    json_data=[]
    for face_matches in compare_result:
        if(len(face_matches.get('FaceMatches'))) >=1:
            perfil = dict(name=face_matches['FaceMatches'][0]['Face']['ExternalImageId'],
                         faceMatch=round(face_matches['FaceMatches'][0]['Similarity'],2))
            json_data.append(perfil)
    return json_data;

def publish_data(json_data):
    file=s3.Object('site-tr','dados.json')
    file.put(Body=json.dumps(json_data))

def delete_old_image(face_id_list):
    client.delete_faces(
        CollectionId='faces',
        FaceIds=face_id_list
    )

def main(event,context):
    faces_detected= detect_faces()
    print(json.dumps(faces_detected,indent=4))
    face_id_list=create_faceId_list(faces_detected)
    compare_result=compare_images(face_id_list)
    print(json.dumps(compare_result,indent=4))
    json_data=create_json_data(compare_result)
    print(json.dumps(json_data,indent=4))
    publish_data(json_data)
    delete_old_image(face_id_list)
