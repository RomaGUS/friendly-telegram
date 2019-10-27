from boto3.s3.transfer import S3Transfer
import config
import boto3

class Spaces():
	def __init__(self):
		self.ACCESS_ID = config.spaces['app']
		self.SECRET_KEY = config.spaces['secret']
		self.ENDPOING = config.spaces['endpoint']
		self.REGION = config.spaces['region']
		self.SPACE = config.spaces['space']

		self.session = boto3.session.Session()
		self.client = self.session.client('s3',
								region_name=self.REGION,
								endpoint_url=self.ENDPOING,
								aws_access_key_id=self.ACCESS_ID,
								aws_secret_access_key=self.SECRET_KEY)

	def upload_file(self, file, path):
		transfer = S3Transfer(self.client)
		transfer.upload_file(file, self.SPACE, path)
		return self.client.put_object_acl(ACL='public-read', Bucket=self.SPACE, Key=path)
