import redis

class DocumentComparer:
    _instance = None

    def __init__(self):
        self.redis_client = redis.StrictRedis(host='redis', port=6379, db=0)