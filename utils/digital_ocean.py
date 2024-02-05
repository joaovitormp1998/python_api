from boto3 import client

from tempfile import TemporaryFile
from dotenv import load_dotenv
from os import getenv

load_dotenv()

s3 = client('s3', endpoint_url = getenv('DO_SPACES_ENDPOINT'), aws_access_key_id = getenv('DO_SPACES_KEY'), aws_secret_access_key = getenv('DO_SPACES_SECRET'))