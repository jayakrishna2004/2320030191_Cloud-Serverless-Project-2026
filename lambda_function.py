import json
import boto3
import base64

# SES client
ses = boto3.client('ses', region_name='us-east-1')

def lambda_handler(event, context):

    print("EVENT:", event)

    try:
        # ✅ Handle CORS
        if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                "body": ""
            }

        # ✅ Parse body
        body = event.get('body', '{}')

        if isinstance(body, str):
            body = json.loads(body)

        # ✅ Inputs
        email = body.get('email')
        subject = body.get('subject', 'KL Notification')
        message = body.get('message', 'Hello from KL Smart Notify')
        file_data = body.get('file')   # base64 file
        file_name = body.get('filename', 'attachment.csv')

        print("EMAIL:", email)

        if not email:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps("Email is required")
            }

        # 🔥 If NO file → normal email
        if not file_data:
            response = ses.send_email(
                Source='klsmartnotification@gmail.com',
                Destination={'ToAddresses': [email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {
                        'Text': {'Data': message}
                    }
                }
            )

        # 🔥 If file exists → send with attachment
        else:
            msg = f"""From: klsmartnotification@gmail.com
To: {email}
Subject: {subject}
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary="NextPart"

--NextPart
Content-Type: text/html

<p>{message}</p>

--NextPart
Content-Type: application/octet-stream; name="{file_name}"
Content-Disposition: attachment; filename="{file_name}"
Content-Transfer-Encoding: base64

{file_data}

--NextPart--
"""

            response = ses.send_raw_email(
                Source='klsmartnotification@gmail.com',
                Destinations=[email],
                RawMessage={'Data': msg}
            )

        print("SES RESPONSE:", response)

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps("Email sent successfully!")
        }

    except Exception as e:
        print("ERROR:", str(e))
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(str(e))
        }