from __future__ import print_function
  
import json
import boto3
  
print('Loading function')
  
def lambda_handler(event, context):
  
    # Parse the JSON message 
    eventText = json.dumps(event)
    
    eventLoad = json.loads(eventText)
  
    if eventLoad["Topic"] == "Alert" :
      # Print the parsed JSON message to the console; you can view this text in the Monitoring tab in the Lambda console or in the CloudWatch Logs console
      print('Received event: ', eventText)
  
      # Create an SNS client
      sns = boto3.client('sns',region_name='us-east-1')
    
    
       # Publish a message to the specified topic
      response = sns.publish (
        TopicArn = 'arn:aws:sns:us-east-1:595492067297:P3SNSTopic',
        Message = eventText
      )
      print(response)
    
    if eventLoad["Topic"] == "Data" :
      sqs = boto3.resource('sqs')
      queue = sqs.get_queue_by_name(QueueName='mySQSQueue')
      response = queue.send_message(MessageBody=json.dumps(event))
      print(response)

