from flask import Flask, request
import logging
import redis
import boto3
from datetime import datetime,timezone
import os
import multiprocessing as mp
import json
import utils
import s3_util
import requests

# Configure logger
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# AWS S3 client
s3 = boto3.client('s3')
# AWS Secret Store Manager client
ssm = boto3.client('ssm')
# Redis client object
redis_client = None

# S3 bucket information
sm_ads_s3_bucket_name: str = None
sm_ads_s3_object_key_format: list = None
sm_ads_s3_object_key_delimiter: str = None

app = Flask(__name__)


def update_cache(redis_client: object, key: str, next_ad_index: int, ads: list, continuation_token: str):
  redis_client.set(key, json.dumps({
    'next': next_ad_index,
    'ads': ads,
    'continuationToken': continuation_token
  }))


def get_key(ad_key_components: list, values: dict, delimiter: str, utc_hour: str) -> str:
  if not ad_key_components or len(ad_key_components) == 0:
    logging.warning('Bad argument: ad key components list cannot be None or of length zero')
    raise ValueError('Ad key components list cannot be None or of length zero')
  
  if not values:
    logging.warning('Bad argument: country and language query arg parameters are missing')
    raise ValueError('Country and language query arg parameters are missing')

  if not delimiter or delimiter == '':
    logging.warning('Bad argument: ad key delimiter cannot be None or empty string')
    raise ValueError('Ad key delimiter cannot be None or empty string')

  if not utc_hour or utc_hour == '':
    logging.warning('Bad argument: UTC hour cannot be None or empty string')
    raise ValueError('UTC hour cannot be None or empty string')

  key = []

  for key_component in ad_key_components:
    if key_component not in values:
      logging.warning(f'Bad argument: missing required query arg parameter "{key_component}"')
      raise ValueError(f'Missing required query arg parameter "{key_component}"')
    key.append(values.get(key_component) + delimiter)    

  key.append(utc_hour)

  return ''.join(key)


def get_ad_from_cache(redis_client: object, key: str) -> dict:
  ads: str = redis_client.get(key).decode('utf-8')
  ads: dict = json.loads(ads)
  next_ad_index: int = ads['next']
  continuation_token: str = ads['continuationToken']
  
  if next_ad_index == len(ads['ads']) and continuation_token:
    # We have shown all available ads from the cache, so get the next batch of available ads from S3        
    next_batch_of_ad_keys, continuation_token = s3_util.get_next_batch_of_ad_keys(
      s3_client = s3,
      bucket = sm_ads_s3_bucket_name, 
      prefix = key,           
      continuation_token = continuation_token
    )

    next_batch_of_ads = s3_util.get_next_batch_of_ads_from_s3(
      s3_client = s3, 
      bucket = sm_ads_s3_bucket_name, 
      keys = next_batch_of_ad_keys
    )

    update_cache(redis_client, key, 1, next_batch_of_ads, continuation_token)
    return next_batch_of_ads[0]
  elif next_ad_index == len(ads['ads']) and not continuation_token:
    return ads['ads'][0] # TODO: pick random not 0
  elif next_ad_index < len(ads):
    update_cache(redis_client, key, next_ad_index + 1, ads['ads'], continuation_token)
    return ads['ads'][next_ad_index]


def get_availability_zone():
  logging.info('Getting container AZ...')
  ECS_CONTAINER_METADATA_URI = str(os.environ['ECS_CONTAINER_METADATA_URI'])
  data = requests.get(f'{ECS_CONTAINER_METADATA_URI}/task')
  data = json.loads(data.content)
  logging.info(f'task metadata endpoint response: {data}')
  return data['AvailabilityZone']


@app.route('/ad_request', methods=['GET'])
def api():
  try:
    utc_hour: str = str(datetime.now(timezone.utc).hour)

    key: str = get_key(
      sm_ads_s3_object_key_format, 
      request.args, 
      sm_ads_s3_object_key_delimiter, 
      utc_hour
    )

    logging.info('Received ad request for: {}'.format(key))

    az = get_availability_zone()

    if redis_client.exists(key):
      logging.info(f'Cache hit for key: {key}')

      ad = get_ad_from_cache(redis_client, key)

      ad['availability_zone'] = az

      return ad, 200
    else:
      logging.info(f'Cache miss for key: {key}')
      next_batch_of_ad_keys, continuation_token = s3_util.get_next_batch_of_ad_keys(s3, sm_ads_s3_bucket_name, key)
      next_batch_of_ads = s3_util.get_next_batch_of_ads_from_s3(s3, sm_ads_s3_bucket_name, next_batch_of_ad_keys)

      if next_batch_of_ads is None:
        key = key.split('/')
        return {
          'Message': f'No ad available for country "{key[0]}" and language "{key[1]}" at "{datetime.now(timezone.utc)}"'
        }

      update_cache(redis_client, key, 1, next_batch_of_ads, continuation_token)

      ad = next_batch_of_ads[0]

      ad['availability_zone'] = az

      return ad, 200
  except Exception as e:
    return { 
      'Message': 'Internal Server Error', 
      'Reason': f'{e}'
    }, 500


@app.route('/health', methods=['GET'])
def health_check():
  return { 'status': 'healthy' }, 200


if __name__ == '__main__':
  environment: str = 'dev'

  if 'ENV' in os.environ:
    environment: str = os.environ['ENV']

  config: object = utils.get_config(environment)

  redis_host: str = utils.get_ssm_parameter_value(ssm, config['redisHostParameterStoreName'])    
  redis_port: str = utils.get_ssm_parameter_value(ssm, config['redisPortParameterStoreName'])
  ad_server_host: str = config['adServerHost']
  ad_server_port: str = config['adServerPort']
  debug: str = config['debug']
  is_threaded: bool = config['isThreaded']
  sm_ads_s3_bucket_name: str = config['smAdsS3BucketName']
  sm_ads_s3_object_key_format: list = config['smAdsS3ObjectKeyFormat']
  sm_ads_s3_object_key_delimiter: str = config['smAdsS3ObjectKeyDelimiter']
  
  redis_client = redis.Redis(host = redis_host, port = int(redis_port))

  app.run(
    processes = mp.cpu_count(),
    host = ad_server_host,
    port = ad_server_port,
    debug = debug,
    threaded = is_threaded
  )  