import json
import requests
import os
import time
import multiprocessing as mp
from contextlib import contextmanager
import boto3

s3 = boto3.client('s3')
s3_bucket = 'sm-ads'

def explode_ad_campaign(ad_campaign: dict, start_hour: int, end_hour: int) -> list:
  ad_campaign_hours = []

  for hour in range(start_hour, end_hour):
    ad_campaign_hours.append('{}/{}/{}/{}'.format(
      ad_campaign['country'],
      ad_campaign['lang'],
      hour,
      ad_campaign['id'],
    ).lower())

  return ad_campaign_hours


def get_ad_campaign_universe(ad_campaign: dict) -> list:
  """
    Processes an ad campaign based on its start_hour and end_hour 
    and expands it into the individual hours of when it can be shown

    Args:
      ad_campaign (list): The ad campaign for which to get individual 
        hours that it is available for

    Returns:
      ad_campaign_hours: a list of keys representing the ad campaign hours for this ad with a country/lang/hour prefix
  """
  ad_campaign_hours = []

  start_hour = ad_campaign['start_hour']
  end_hour = ad_campaign['end_hour']

  if start_hour == end_hour:
    ad_campaign_hours = explode_ad_campaign(ad_campaign, 0, 24)

  if start_hour < end_hour:
    ad_campaign_hours = explode_ad_campaign(
    ad_campaign, start_hour, end_hour)

  if start_hour > end_hour:
    ad_campaign_hours = explode_ad_campaign(ad_campaign, start_hour, 24)
    ad_campaign_hours.extend(explode_ad_campaign(ad_campaign, 0, end_hour))

  return ad_campaign_hours


def process_ad(ad: dict):
  """
    Builds ad campaign universe for 'ad' and sinks it to S3 data lake
  """
  ad_campaign_universe = get_ad_campaign_universe(ad)

  ad_id = ad['id']
  video_url = ad['video_url']

  ad = {'id': ad_id, 'videoUrl': video_url}

  for key in ad_campaign_universe:
    upload_to_s3(s3, s3_bucket, key, ad)


def upload_to_s3(s3_client: object, bucket: str, key: str, ad: dict):    
  s3.put_object(Body=json.dumps(ad), Bucket=bucket, Key=key)


@contextmanager
def poolcontext(*args, **kwargs):
  pool = mp.Pool(*args, **kwargs)
  yield pool
  pool.terminate()


if __name__ == '__main__':
  cpu_count = mp.cpu_count()
  chunksize = 50
  ads = None

  # with open('./ads.json', 'r') as f:
  #   ads = json.loads(''.join(f.readlines()))
  #   ads = ads['ads']

  video_ad_service_url = 'https://gist.githubusercontent.com/victorhurdugaci/22a682eb508e65d97bd5b9152f564ab3/raw/dbf27ef217dba9bbd753de26cdabf8a91bdf1550/sm_ads.json'

  ads = requests.get(video_ad_service_url).text 
  ads = json.loads(ads)
  ads = ads['ads']

  with poolcontext(processes=cpu_count) as pool:
    pool.map(get_ad_campaign_universe, ads, chunksize)
