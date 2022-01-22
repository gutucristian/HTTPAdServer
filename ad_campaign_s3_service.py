import json
import requests
import multiprocessing as mp
from contextlib import contextmanager
import boto3
import logging

logging.basicConfig(
  filename='adCampaignS3Service.log', 
  filemode='a', 
  format='[%(asctime)s] - %(message)s',
  datefmt='%H:%M:%S',
  level=logging.INFO
)

s3 = boto3.client('s3')
s3_bucket = 'game-ads'

def explode_ad_campaign(ad_campaign: dict, start_hour: int, end_hour: int) -> list:
  ad_campaign_hours = []

  country = ad_campaign['country']
  lang = ad_campaign['lang']  
  ad_id = ad_campaign['id']

  for hour in range(start_hour, end_hour):
    ad_campaign_hours.append(f'{country}/{lang}/{hour}/{ad_id}'.lower())

  return ad_campaign_hours


def get_ad_campaign_universe(ad_campaign: dict) -> list:
  """
    Processes an ad campaign based on its start_hour and end_hour 
    and expands it into the individual hours of when it can be shown

    Args:
      ad_campaign (list): The ad campaign for which to get individual 
        hours that it is available for

    Returns:
      ad_campaign_hours (str): a list of keys (each with a country/lang/hour prefix) representing the ad campaign hours for this ad
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
  logging.info(f'Process ad: {ad}')

  ad_campaign_universe = get_ad_campaign_universe(ad)

  logging.info(f'Ad campaign universe: {ad_campaign_universe}')

  ad_id = ad['id']
  video_url = ad['video_url']

  ad = {'id': ad_id, 'videoUrl': video_url}

  for key in ad_campaign_universe:
    logging.info(f'Writing object with key {key} to bucket {s3_bucket}')
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

  with open('./ads.json', 'r') as f:
    ads = json.loads(''.join(f.readlines()))
    ads = ads['ads']  

  # ads = requests.get(video_ad_service_url).text
  # ads = json.loads(ads)
  # ads = ads['ads']

  with poolcontext(processes=cpu_count) as pool:
    pool.map(process_ad, ads, chunksize)
