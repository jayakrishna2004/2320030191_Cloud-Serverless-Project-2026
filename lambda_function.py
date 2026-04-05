import json
import boto3

sns = boto3.client('sns', region_name='us-east-1')  # 👈 force region

def lambda_handler(event, context):

    print("EVENT:", event)

    try:
        body = event.get('body', '{}')

        if isinstance(body, str):
            body = json.loads(body)

        if not isinstance(body, dict):
            body = {}

        message = body.get('message', 'Default message from API')

        print("MESSAGE:", message)  # 👈 debug

        response = sns.publish(
            TopicArn='arn:aws:sns:us-east-1:150156064700:notification:7907e213-ac97-4578-aa2e-15b5cc97b916',
            Message=message,
            Subject='Notification'
        )

        print("SNS RESPONSE:", response)  # 👈 debug

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps('Notification Sent!')
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(str(e))
        }