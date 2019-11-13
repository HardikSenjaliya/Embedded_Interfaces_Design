#!/usr/bin/python3

import boto3

local_image = '11_13_2019_01_20_58.jpg'
bucket_name = 'eid-image-rekognition' 
collection_id = 'image-collection'
threshold = 95
maxFaces=1

s3Client = boto3.client('s3')
rekoClient = boto3.client('rekognition')


def create_collection(collection_id):
    
    response = rekoClient.create_collection(CollectionId=collection_id)
    print('Status code: ' + str(response['StatusCode']))
    

def add_faces_to_collection(bucket, image, collection_id):
    response=rekoClient.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':image}},
                                ExternalImageId=image,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])
    
    print ('Results for ' + image)  
    print('Faces indexed:')                     
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])

def find_face_in_collection(bucket, image, collection_id):
    
    response=rekoClient.search_faces_by_image(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':image}},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)

                                
    faceMatches=response['FaceMatches']
    print ('Matching faces')
    for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
        

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
    
#    uploaded = upload_to_aws(local_image, bucket_name, local_image)
#    indexed_faces_count = add_faces_to_collection(bucket_name, local_image, collection_id)
#    print("Faces Indexed Count:" + str(indexed_faces_count))
    
    find_face_in_collection(bucket_name, local_image, collection_id)
    