#!/usr/bin/python3

    
import boto3

def list_faces_in_collection(collection_id):


    maxResults=2
    faces_count=0
    tokens=True
    hello = []
    extfaces = []

    client=boto3.client('rekognition')
    response=client.list_faces(CollectionId=collection_id,
                               MaxResults=maxResults)

    print('Faces in collection ' + collection_id)

 
    while tokens:

        faces=response['Faces']

        for face in faces:
            print(face)
            faces_count+=1
        
        if 'NextToken' in response:
            nextToken=response['NextToken']
            response=client.list_faces(CollectionId=collection_id,
                                       NextToken=nextToken,MaxResults=maxResults)
        else:
            tokens=False
      
    return hello

def add_faces_to_collection(bucket,photo,collection_id):


    
    client=boto3.client('rekognition')

    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                ExternalImageId=photo,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print ('Results for ' + photo) 	
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

def main():

    collection_id='user_profile_images'
    bucket = 'eid-image-rekognition'
    photo = 'isha.jpg'
    hello=list_faces_in_collection(collection_id)
    
    
    faces=[]
    faces.append("ddc0206b-93fb-41a0-8c71-8cdb44108557")
    
    #indexed_faces_count=add_faces_to_collection(bucket, photo, collection_id)

    #faces_count=delete_faces_from_collection(collection_id, faces)
    



if __name__ == "__main__":
	main()
