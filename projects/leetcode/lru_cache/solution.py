from typing import Dict, Optional

class Node:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: Dict[int, Node] = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)

        self.head.next = self.tail
        self.tail.prev = self.head


    def _remove_node(self, node: Node):
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev

    def _append_node(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node


    def put(self, key: int, value: int):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove_node(node)
            self._append_node(node)
        else:
            if len(self.cache) >= self.capacity:
                lru_node = self.tail.prev
                if lru_node:
                    self._remove_node(lru_node)
                    del self.cache[lru_node.key]

            new_node = Node(key, value)
            self._append_node(new_node)
            self.cache[key] = new_node

    def get(self, key: int):
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove_node(node)
        self._append_node(node)
        return node.value
