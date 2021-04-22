import requests
import json

user_data = {
  'AuthParameters' : {
    'USERNAME' : 'foo', 
    'PASSWORD' : 'fooBarBaz1!'
  }, 
  'AuthFlow' : 'USER_PASSWORD_AUTH', 
  'ClientId' : '6p0to3eafoghamofcdv7mntf3g'
}

headers = {'Content-Type': 'application/x-amz-json-1.1', 'X-Amz-Target': 'AWSCognitoIdentityProviderService.InitiateAuth' }
resp = requests.post('https://cognito-idp.us-east-1.amazonaws.com', data=json.dumps(user_data), headers=headers)

token = json.loads(resp.content)['AuthenticationResult']['AccessToken']

print(token)

response = requests.get('https://api.gutucristian.com/ad_request?country=us&lang=eng', headers={'Authorization': token})

print('Response status code: {}'.format(response.status_code))
print('Response data: {}'.format(response.text))