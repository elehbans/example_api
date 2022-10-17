from api import create_app
from config import Config
import redis

app = create_app()
db = redis.Redis(
        host=Config.REDIS_SERVICE_NAME, 
        port=Config.REDIS_PORT, 
        decode_responses=True)


@app.route('/')
def hello():
    db.mset({"key": "hello world"})
    test = db.get("key")
    return test