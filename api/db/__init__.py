from redis_om import Migrator, get_redis_connection

def init_db():
        import api.db.models

        Migrator().run()

def flush_db():
        r = get_redis_connection()
        r.flushall()
