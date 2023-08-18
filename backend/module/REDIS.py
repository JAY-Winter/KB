import redis

class DocumentComparer:
    _instance = None

    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def compare_similarity(self, content):
        # content를 키로 해시를 생성합니다.
        hash_key = str(hash(content))
        
        # Redis에서 결과를 검색합니다.
        cached_result = self.redis_client.get(hash_key)
        
        # 캐시에 값이 있다면 바로 반환합니다.
        if cached_result:
            return cached_result.decode('utf-8')
        
        # 실제 유사도 계산 로직
        results = ...  # 유사도 계산 결과
        
        # 결과를 Redis에 저장합니다.
        # (예: 1시간 동안 캐시를 보관하려면 expire를 3600초로 설정)
        self.redis_client.set(hash_key, results, ex=3600)
        
        return results
