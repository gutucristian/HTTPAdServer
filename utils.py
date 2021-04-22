import json


def get_ssm_parameter_value(ssm_client: object, paramater: str) -> str:
  parameter: str = ssm_client.get_parameter(Name=paramater, WithDecryption=True)
  return parameter['Parameter']['Value']


def get_config(environment: str):
  config = None

  if environment == 'dev':
    config_path = './conf/dev.json'

  with open(config_path) as f:
    config = json.loads(''.join(f.readlines()))

  return config