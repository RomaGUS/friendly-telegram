import s3fs
import config

fs = s3fs.S3FileSystem(anon=False,
						key=config.spaces['app'],
						secret=config.spaces['secret'],
						client_kwargs={'endpoint_url': config.spaces['endpoint'],
										'region_name': config.spaces['region']})

fs.put('test.txt', 'hikka/test3.txt')
fs.chmod('hikka/test3.txt', 'public-read')
