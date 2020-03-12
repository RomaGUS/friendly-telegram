import config
import s3fs

def init_fs():
    return s3fs.S3FileSystem(
        anon=False,
        key=config.storage["app"],
        secret=config.storage["secret"],
        client_kwargs={"endpoint_url": config.storage["endpoint"],
                        "region_name": config.storage["region"]}
    )
