from redis_om import Migrator, get_redis_connection
from redis import Redis

from api.config import Config

def init_db():
        from .models import Contact

        Migrator().run()

def flush_db():
        r = get_redis_connection()
        r.flushall()
