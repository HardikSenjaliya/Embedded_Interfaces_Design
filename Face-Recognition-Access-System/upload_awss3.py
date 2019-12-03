#!/usr/bin/python3

import boto3
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)


local_image = '11_18_2019_21_08_22.jpg'
bucket_name = 'eid-image-rekognition' 
collection_id = 'user_profile_images'


threshold = 97
maxFaces=1

s3Client = boto3.client('s3')
rekoClient = boto3.client('rekognition')



#def create_collection(collection_id):
#    
#    response = rekoClient.create_collection(CollectionId=collection_id)
#    print('Status code: ' + str(response['StatusCode']))
#    
#def delete_collection(collection_id):
#    response = rekoClient.delete_collection(CollectionId=collection_id)
#    print(response['StatusCode'])
#    
#def delete_faces_from_collection(collection_id, faces):
#    response = rekoClient.delete_faces(CollectionId=collection_id, FaceIds=faces)
#
#def add_faces_to_collection(bucket, image, collection_id):
#    response=rekoClient.index_faces(CollectionId=collection_id,
#                                Image={'S3Object':{'Bucket':bucket,'Name':image}},
#                                ExternalImageId=image,
#                                MaxFaces=1,
#                                QualityFilter="AUTO",
#                                DetectionAttributes=['ALL'])
#    
#    print ('Results for ' + image)  
#    print('Faces indexed:')                     
#    for faceRecord in response['FaceRecords']:
#         print('  Face ID: ' + faceRecord['Face']['FaceId'])
#         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))
#
#    print('Faces not indexed:')
#    for unindexedFace in response['UnindexedFaces']:
#        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
#        print(' Reasons:')
#        for reason in unindexedFace['Reasons']:
#            print('   ' + reason)
#    return len(response['FaceRecords'])

def find_face_in_collection(bucket, image, collection_id):
#
#    response=rekoClient.search_faces_by_image(CollectionId=collection_id,
#                                Image={'S3Object':{'Bucket':bucket,'Name':image}},
#                                FaceMatchThreshold=threshold,
#                                MaxFaces=maxFaces)
#
    with open(image, 'rb') as image:
        response=rekoClient.search_faces_by_image(CollectionId=collection_id,
                                Image={'Bytes': image.read()},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)


    faceMatches=response['FaceMatches']
    print ('Matching faces')
    for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print('Name:' + match['Face']['ExternalImageId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            if(match['Similarity'] > 97):
                print('Unlock')
                GPIO.output(18, GPIO.HIGH)
                time.sleep(5)
                GPIO.cleanup()


def upload_to_aws(local_image, bucket, s3_file):

    try:
        s3Client.upload_file(local_image, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


if __name__ == '__main__':

    find_face_in_collection(bucket_name, local_image, collection_id)

    

