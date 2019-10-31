import config
import s3fs

def init_fs():
	return s3fs.S3FileSystem(anon=False,
						key=config.spaces['app'],
						secret=config.spaces['secret'],
						client_kwargs={'endpoint_url': config.spaces['endpoint'],
										'region_name': config.spaces['region']})
