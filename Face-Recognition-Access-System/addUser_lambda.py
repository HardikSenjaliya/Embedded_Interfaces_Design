import json
import boto3

reko_client = boto3.client('rekognition')
s3_client = boto3.client('s3')

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

    max_results=2
    
    client=boto3.client('rekognition')

    #Display all the collections
    print('Displaying collections...')
    response=client.list_collections(MaxResults=max_results)
    collection_count=0
    done=False
    
    while done==False:
        collections=response['CollectionIds']

        for collection in collections:
            print (collection)
            collection_count+=1
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_collections(NextToken=nextToken,MaxResults=max_results)
            
        else:
            done=True
            
            
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

def lambda_handler(event, context):
    
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        obj_key = record['s3']['object']['key']
        
        add_faces_to_collection(bucket_name, obj_key, collection_id)
