import boto3
import requests
import json

provider_client = boto3.client('cognito-idp', region_name='us-east-1')

# API user credentials
auth_data = { 'USERNAME':'foo', 'PASSWORD':'fooBarBaz1!' }

# Provide user credentials and client id to get JWT token
response = provider_client.admin_initiate_auth(
  UserPoolId = 'us-east-1_kquJaRpJU', 
  AuthFlow = 'ADMIN_NO_SRP_AUTH', 
  AuthParameters = auth_data,
  ClientId = '6p0to3eafoghamofcdv7mntf3g'
)

token = response['AuthenticationResult']['IdToken']

response = requests.get('https://api.gutucristian.com/ad_request?country=us&lang=eng', headers={'Authorization': token})

print('Response status code: {}'.format(response.status_code))
print('Response data: {}'.format(response.text))