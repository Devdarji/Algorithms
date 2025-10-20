import hashlib
import random
from typing import Dict, List, Optional

class KademliaNode:
    def __init__(self, node_id: Optional[int] = None, k: int = 20):
        self.node_id = node_id or random.getrandbits(160)
        self.k = k  # bucket size
        self.buckets: List[List[int]] = [[] for _ in range(160)]  # 160-bit address space
        self.storage: Dict[int, str] = {}
    
    def distance(self, id1: int, id2: int) -> int:
        return id1 ^ id2
    
    def bucket_index(self, node_id: int) -> int:
        distance = self.distance(self.node_id, node_id)
        return distance.bit_length() - 1 if distance > 0 else 0
    
    def add_node(self, node_id: int):
        if node_id == self.node_id:
            return
        
        bucket_idx = self.bucket_index(node_id)
        bucket = self.buckets[bucket_idx]
        
        if node_id in bucket:
            bucket.remove(node_id)
            bucket.append(node_id)  # move to end (most recent)
        elif len(bucket) < self.k:
            bucket.append(node_id)
        else:
            # bucket full - in real implementation, ping oldest node
            bucket.pop(0)
            bucket.append(node_id)
    
    def find_closest_nodes(self, target_id: int, count: Optional[int] = None) -> List[int]:
        count = count or self.k
        all_nodes = []
        
        for bucket in self.buckets:
            all_nodes.extend(bucket)
        
        all_nodes.sort(key=lambda x: self.distance(target_id, x))
        return all_nodes[:count]
    
    def store(self, key: str, value: str):
        key_hash = int(hashlib.sha1(key.encode()).hexdigest(), 16)
        self.storage[key_hash] = value
    
    def find_value(self, key: str) -> Optional[str]:
        key_hash = int(hashlib.sha1(key.encode()).hexdigest(), 16)
        return self.storage.get(key_hash)

class KademliaDHT:
    def __init__(self):
        self.nodes: Dict[int, KademliaNode] = {}
    
    def add_node(self, node: KademliaNode):
        self.nodes[node.node_id] = node
    
    def bootstrap(self, new_node: KademliaNode, bootstrap_node_id: int):
        if bootstrap_node_id in self.nodes:
            new_node.add_node(bootstrap_node_id)
            self.nodes[bootstrap_node_id].add_node(new_node.node_id)
    
    def lookup(self, node_id: int, target_key: str) -> Optional[str]:
        if node_id not in self.nodes:
            return None
        
        node = self.nodes[node_id]
        key_hash = int(hashlib.sha1(target_key.encode()).hexdigest(), 16)
        
        # Check local storage first
        value = node.find_value(target_key)
        if value:
            return value
        
        # Find closest nodes and query them
        closest = node.find_closest_nodes(key_hash)
        for close_node_id in closest:
            if close_node_id in self.nodes:
                value = self.nodes[close_node_id].find_value(target_key)
                if value:
                    return value
        
        return None

# Example usage
if __name__ == "__main__":
    dht = KademliaDHT()
    
    # Create nodes
    node1 = KademliaNode()
    node2 = KademliaNode()
    node3 = KademliaNode()
    
    # Add to DHT
    dht.add_node(node1)
    dht.add_node(node2)
    dht.add_node(node3)
    
    # Bootstrap connections
    dht.bootstrap(node2, node1.node_id)
    dht.bootstrap(node3, node1.node_id)
    
    # Store and retrieve
    node1.store("hello", "world")
    result = dht.lookup(node2.node_id, "hello")
    print(f"Lookup result: {result}")
