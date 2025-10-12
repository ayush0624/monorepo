# LRU Cache (LeetCode Medium)

### Problem Description
Design an **LRU (Least Recently Used) cache** that supports the following operations in **O(1)** time complexity:

- `get(key)`: Retrieve the value of the key if it exists, otherwise return `-1`.
- `put(key, value)`: Insert or update the key-value pair.  
  - If the cache exceeds its capacity, evict the least recently used key.

### Example

```python
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
print(cache.get(1))   # returns 1
cache.put(3, 3)       # evicts key 2
print(cache.get(2))   # returns -1 (not found)
cache.put(4, 4)       # evicts key 1
print(cache.get(1))   # returns -1
print(cache.get(3))   # returns 3
print(cache.get(4))   # returns 4
