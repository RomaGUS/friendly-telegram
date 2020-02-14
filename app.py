from hikka import app
import config

if __name__ == "__main__":
    app.run(
        debug=config.debug,
        host=config.host,
        port=config.port
    )
