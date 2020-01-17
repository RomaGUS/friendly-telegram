# Config file

To start running hikka website you have to create `config.py` file in root of project folder:

```python
debug = True
secret = "Lorem ipsum dolor sit."
host = "0.0.0.0"
port = 1234

spaces = {
    "app": "APP_ID",
    "secret": "APP_SECRET",
    "endpoint": "APP_ENDPOINT",
    "region": "APP_REGION",
    "space": "APP_SPACE"
}

db = {
    "username": "USERNAME",
    "password": "PASSWORD",
    "port": 27017,
    "name": "DB_NAME"
}
```
