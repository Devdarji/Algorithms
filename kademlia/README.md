# Kademlia DHT Implementation

A minimal implementation of the Kademlia Distributed Hash Table algorithm.

## Files

- `kademlia.py` - Core Kademlia implementation
- `algorithm_explained.py` - Comprehensive examples and algorithm explanation
- `README.md` - This file

## Algorithm Overview

Kademlia is a peer-to-peer distributed hash table that uses XOR metric for efficient routing:

### Key Concepts

1. **XOR Distance**: `distance(a,b) = a XOR b`
   - Symmetric: d(A,B) = d(B,A)
   - Unique: For any node A and distance d, exactly one node B exists where d(A,B) = d

2. **k-buckets**: Routing table with k nodes per distance range
   - Bucket i contains nodes at distance [2^i, 2^(i+1))
   - Typically k=20 nodes per bucket

3. **Lookup Process**: O(log n) complexity
   - Find k closest nodes iteratively
   - Query closest nodes for target key/node

## Usage

```python
from kademlia import KademliaNode, KademliaDHT

# Create DHT network
dht = KademliaDHT()
node1 = KademliaNode()
node2 = KademliaNode()

# Add nodes and bootstrap
dht.add_node(node1)
dht.add_node(node2)
dht.bootstrap(node2, node1.node_id)

# Store and retrieve data
node1.store("key", "value")
result = dht.lookup(node2.node_id, "key")
```

## Run Examples

```bash
python algorithm_explained.py
```

This demonstrates:
- XOR distance calculation
- k-bucket structure
- Lookup process
- Routing efficiency
- Fault tolerance

## Real-World Usage

Kademlia is used in:
- BitTorrent DHT
- Ethereum node discovery
- IPFS content routing
- Various P2P applications
