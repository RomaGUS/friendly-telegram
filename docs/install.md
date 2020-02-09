# Hikka installation guide

This installation guide provide step by step instruction for running Hikka backend. You should be able to run it on any Unix-like operating system without any issues. Also keep in mind that you will need Python 3.7 or higher.

First of all you should clone this repository :)

```
$ git clone https://github.com/hkkio/hikka.git
```

## Prerequisites

You have to [install]((https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-18-04)) MongoDB and set up DigitalOcean [Spaces](https://www.digitalocean.com/products/spaces/) or any other S3 compatible service.


## Config file

To start running Hikka backend you have to create `config.py` file in root of project folder.

```python
debug = True
secret = "Lorem ipsum dolor sit."
host = "0.0.0.0"
port = 1234

cdn = "CDN_LINK"
url = "FRONTEND_URL"

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

smtp = {
    "username": "SMTP_USERNAME",
    "password": "SMTP_PASSWORD",
    "host": "SMTP_HOST",
    "port": 587
}
```

Here is some key points overview:

- `secret`: Flask [SECRET_KEY](https://stackoverflow.com/a/22463969/9217774).
- `cdn`: link to spaces cdn domain.
- `url`: website frontend url.
- `spaces`: this object contains DigitalOcean spaces credentials, but you should be able to use any S3 compatible services.
- `smtp`: SMTP credentials.
- `db`: MongoDB credentials.

## Virtual enviroment

In order to run app you should set up Python [virtual enviroment](https://docs.python.org/3/tutorial/venv.html).

```
$ python3 -m venv venv
```

And now activate it.

```
$ source venv/bin/activate
```

## Dependencies

You can install dependencies using `requirements.txt` file.

```
$ pip3 install -r requirements.txt
```

At this point you should be able to run Hikka backend.

```
$ python3 app.py
```

I'd also recommend you set up [gunicorn](https://gunicorn.org) for running Flaks app, since default development server is not designed for production. [Here](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04) is good guide from DigitalOcean how you can do that.

