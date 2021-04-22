import json


def get_next_batch_of_ads_from_s3(s3_client: object, bucket: str, keys: list) -> list:
  if s3_client is None or keys is None or len(keys) == 0:
    return None

  ads = []

  for key in keys:
    response = s3_client.get_object(Bucket = bucket, Key = key)
    if 'Body' in response:
      ad = json.loads(response['Body'].read().decode('utf-8'))
      ads.append(ad)

  return ads


def get_next_batch_of_ad_keys(s3_client: object, bucket: str, prefix: str, max_keys: int = 3, continuation_token: str = None) -> list:
  response = None

  if continuation_token:
    response = s3_client.list_objects_v2(
      Bucket = bucket,
      Prefix = prefix,
      MaxKeys = max_keys,
      ContinuationToken = continuation_token
    )
  else:
    response = s3_client.list_objects_v2(
      Bucket = bucket,
      Prefix = prefix,
      MaxKeys = max_keys      
    )

  keys: list = []
  continuation_token: str = None

  if 'Contents' not in response:
    return None, None

  for obj in response['Contents']:
    keys.append(obj['Key'])
  
  if 'NextContinuationToken' in response:
    continuation_token = response['NextContinuationToken']

  return keys, continuation_token