from projects.leetcode.lru_cache.solution import LRUCache

# ----------------------------
# Unit Tests
# ----------------------------


def test_basic_usage():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)
    assert cache.get(2) == -1  # evicted
    cache.put(4, 4)
    assert cache.get(1) == -1  # evicted
    assert cache.get(3) == 3
    assert cache.get(4) == 4


def test_update_existing_key():
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(1, 20)
    assert cache.get(1) == 20
    cache.put(2, 30)
    cache.put(3, 40)
    assert cache.get(1) == -1  # evicted (it was least recently used)
    assert cache.get(2) == 30
    assert cache.get(3) == 40


def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    assert cache.get(1) == 1
    cache.put(2, 2)
    assert cache.get(1) == -1
    assert cache.get(2) == 2


def test_repeated_access_keeps_recent():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)
    cache.put(3, 3)
    assert cache.get(1) == 1  # still in cache
    assert cache.get(2) == -1
    assert cache.get(3) == 3


def test_empty_cache_get_returns_minus_one():
    cache = LRUCache(2)
    assert cache.get(5) == -1


def test_stress():
    cache = LRUCache(50)
    for i in range(50):
        cache.put(i, i * 10)
    for i in range(25):
        cache.get(i)
    for i in range(50, 75):
        cache.put(i, i * 10)
    for i in range(25):
        assert cache.get(i) != -1  # recently accessed should stay
