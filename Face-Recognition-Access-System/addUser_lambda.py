import json
import boto3

reko_client = boto3.client('rekognition')
s3_client = boto3.client('s3')
extfaces = []
faceids = []
collection_id = 'user_profile_images'

def create_collection(collection_id):
    
    response = reko_client.create_collection(CollectionId=collection_id)
    print('Status code: ' + str(response['StatusCode']))
    if(response['StatusCode'] != 200):
        sys.exit('Error: Creating a Collection')
    
def delete_collection(collection_id):
    response = rekoClient.delete_collection(CollectionId=collection_id)
    if(response['StatusCode'] != 200):
        sys.exit('Error: Deleting a Collection')   
    

def list_collections():

    global extfaces, faces
    maxResults=2
    faces_count=0
    tokens=True


    client=boto3.client('rekognition')
    response=client.list_faces(CollectionId=collection_id,
                               MaxResults=maxResults)

    #print('Faces in collection ' + collection_id)

 
    while tokens:

        faces=response['Faces']

        for face in faces:
            extfaces.append(face['ExternalImageId'])
            #print(face)
            faces_count+=1
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collection_id,
                                       NextToken=nextToken,MaxResults=maxResults)
        else:
            tokens=False

def find_collections(obj_key):

    global extfaces, faces
    maxResults=2
    faces_count=0
    tokens=True

    client=boto3.client('rekognition')
    response=client.list_faces(CollectionId=collection_id,
                               MaxResults=maxResults)

    while tokens:

        faces=response['Faces']

        for face in faces:
            if(face['ExternalImageId'] == obj_key):
                faceids.append(face['FaceId'])
            faces_count+=1
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collection_id,
                                       NextToken=nextToken,MaxResults=maxResults)
        else:
            tokens=False

    
            
def add_faces_to_collection(bucket, image, collection_id):
    response=reko_client.index_faces(CollectionId=collection_id,
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

def delete_faces_from_collection(collection_id, faces):

    client=boto3.client('rekognition')

    response=client.delete_faces(CollectionId=collection_id,
                               FaceIds=faces)
    
    print(str(len(response['DeletedFaces'])) + ' faces deleted:') 							
    for faceId in response['DeletedFaces']:
         print (faceId)
    return len(response['DeletedFaces'])


def lambda_handler(event, context):

    global extfaces, faceids
    
    list_collections()
    
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        obj_key = record['s3']['object']['key']

        if(record['eventName'] == 'ObjectCreated:Put'):
            add_faces_to_collection(bucket_name, obj_key, collection_id)
        else:
            for user in extfaces:
                if(obj_key == user):
                    find_collections(obj_key)
                    delete_faces_from_collection(collection_id,faceids)
