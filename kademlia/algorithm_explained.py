"""
KADEMLIA ALGORITHM EXPLAINED

Kademlia is a distributed hash table (DHT) that provides efficient peer-to-peer storage and lookup.
Key innovation: Uses XOR metric for distance calculation between node IDs.

CORE CONCEPTS:
1. Node IDs: 160-bit identifiers (usually SHA-1 hashes)
2. XOR Distance: distance(a,b) = a XOR b
3. k-buckets: Routing table with k nodes per bucket (typically k=20)
4. Recursive lookup: Find closest nodes iteratively

XOR DISTANCE PROPERTIES:
- Symmetric: d(x,y) = d(y,x)
- Triangle inequality: d(x,z) ≤ d(x,y) + d(y,z)
- Unidirectional: For any x and distance d, there's exactly one y where d(x,y) = d
"""

from kademlia import KademliaNode, KademliaDHT
import random

def demonstrate_xor_distance():
    print("=== XOR DISTANCE EXAMPLES ===")
    
    # Simple 4-bit examples for clarity
    examples = [
        (0b1010, 0b1100),  # 10 XOR 12 = 6
        (0b0000, 0b1111),  # 0 XOR 15 = 15
        (0b1001, 0b1001),  # 9 XOR 9 = 0 (same node)
        (0b0101, 0b1010),  # 5 XOR 10 = 15
    ]
    
    for a, b in examples:
        distance = a ^ b
        print(f"  {a:04b} XOR {b:04b} = {distance:04b} (distance: {distance})")
    
    print("\nXOR Properties:")
    print("  - Symmetric: d(A,B) = d(B,A)")
    print("  - Self-distance is 0: d(A,A) = 0")
    print("  - Unique: For any A and distance d, only one B exists where d(A,B) = d")
    print()

def demonstrate_bucket_structure():
    print("=== K-BUCKET STRUCTURE ===")
    
    node = KademliaNode(node_id=0b10000000, k=3)  # Simple 8-bit ID for demo
    
    # Add nodes at different distances
    test_nodes = [
        (0b10000001, "Distance 1 - bucket 0"),
        (0b10000010, "Distance 2 - bucket 1"), 
        (0b10000100, "Distance 4 - bucket 2"),
        (0b10001000, "Distance 8 - bucket 3"),
        (0b10010000, "Distance 16 - bucket 4"),
        (0b11000000, "Distance 64 - bucket 6"),
        (0b00000000, "Distance 128 - bucket 7"),
    ]
    
    print(f"Main node ID: {node.node_id:08b}")
    print("Adding nodes:")
    
    for node_id, description in test_nodes:
        distance = node.distance(node.node_id, node_id)
        bucket_idx = node.bucket_index(node_id)
        node.add_node(node_id)
        print(f"  {node_id:08b} - {description} → bucket[{bucket_idx}]")
    
    print("\nBucket contents:")
    for i, bucket in enumerate(node.buckets):
        if bucket:
            print(f"  Bucket {i}: {[f'{n:08b}' for n in bucket]}")
    print()

def demonstrate_lookup_process():
    print("=== LOOKUP PROCESS EXAMPLE ===")
    
    # Create a small network
    dht = KademliaDHT()
    nodes = []
    
    # Create 8 nodes with known IDs
    node_ids = [0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80]
    for node_id in node_ids:
        node = KademliaNode(node_id=node_id, k=3)
        nodes.append(node)
        dht.add_node(node)
    
    # Connect nodes (simplified bootstrap)
    for i, node in enumerate(nodes):
        for j, other_node in enumerate(nodes):
            if i != j:
                node.add_node(other_node.node_id)
    
    # Store data on node closest to key
    target_key = "example_key"
    key_hash = 0x35  # Simulated hash
    closest_node = min(nodes, key=lambda n: n.distance(n.node_id, key_hash))
    closest_node.store(target_key, "example_value")
    
    print(f"Target key hash: 0x{key_hash:02x}")
    print(f"Stored on node: 0x{closest_node.node_id:02x}")
    print(f"Distance: {closest_node.distance(closest_node.node_id, key_hash)}")
    
    # Demonstrate lookup from different node
    lookup_node = nodes[0]
    print(f"\nLookup from node: 0x{lookup_node.node_id:02x}")
    
    # Find closest nodes to target
    closest = lookup_node.find_closest_nodes(key_hash, count=3)
    print("Closest nodes found:")
    for node_id in closest:
        distance = lookup_node.distance(node_id, key_hash)
        print(f"  Node 0x{node_id:02x} - distance: {distance}")
    
    # Perform actual lookup
    result = dht.lookup(lookup_node.node_id, target_key)
    print(f"\nLookup result: {result}")
    print()

def demonstrate_routing_efficiency():
    print("=== ROUTING EFFICIENCY ===")
    
    # Create larger network to show log(n) property
    dht = KademliaDHT()
    network_size = 64
    
    print(f"Network size: {network_size} nodes")
    print(f"Expected max hops: {network_size.bit_length()} (log₂({network_size}))")
    
    # Create nodes with random IDs
    nodes = []
    for _ in range(network_size):
        node = KademliaNode(node_id=random.randint(0, 2**16-1), k=4)
        nodes.append(node)
        dht.add_node(node)
    
    # Bootstrap network (each node knows a few others)
    for node in nodes:
        bootstrap_count = min(8, len(nodes)-1)
        bootstrap_nodes = random.sample([n for n in nodes if n != node], bootstrap_count)
        for bootstrap_node in bootstrap_nodes:
            node.add_node(bootstrap_node.node_id)
    
    # Test lookup efficiency
    test_node = nodes[0]
    target_key = "test_key"
    target_hash = hash(target_key) & 0xFFFF  # 16-bit hash
    
    closest_nodes = test_node.find_closest_nodes(target_hash, count=8)
    print(f"\nFrom node 0x{test_node.node_id:04x}, found {len(closest_nodes)} closest nodes to 0x{target_hash:04x}")
    
    for i, node_id in enumerate(closest_nodes[:5]):
        distance = test_node.distance(node_id, target_hash)
        print(f"  {i+1}. Node 0x{node_id:04x} - distance: {distance}")
    print()

def demonstrate_fault_tolerance():
    print("=== FAULT TOLERANCE ===")
    
    # Create network
    dht = KademliaDHT()
    nodes = []
    
    for i in range(16):
        node = KademliaNode(node_id=i*16, k=4)  # Spread out IDs
        nodes.append(node)
        dht.add_node(node)
    
    # Bootstrap connections
    for node in nodes:
        for other in nodes:
            if node != other:
                node.add_node(other.node_id)
    
    # Store data on multiple nodes (replication)
    key = "important_data"
    value = "critical_information"
    key_hash = hash(key) & 0xFF
    
    # Find k closest nodes and store on all of them
    storage_nodes = sorted(nodes, key=lambda n: n.distance(n.node_id, key_hash))[:4]
    
    print(f"Storing '{key}' on {len(storage_nodes)} nodes for redundancy:")
    for node in storage_nodes:
        node.store(key, value)
        distance = node.distance(node.node_id, key_hash)
        print(f"  Node 0x{node.node_id:02x} - distance: {distance}")
    
    # Simulate node failure
    failed_node = storage_nodes[0]
    print(f"\nSimulating failure of node 0x{failed_node.node_id:02x}")
    dht.nodes.pop(failed_node.node_id)
    
    # Data still retrievable from other nodes
    remaining_nodes = [n for n in storage_nodes[1:] if n.node_id in dht.nodes]
    print(f"Data still available on {len(remaining_nodes)} nodes")
    
    for node in remaining_nodes:
        result = node.find_value(key)
        if result:
            print(f"  Retrieved from node 0x{node.node_id:02x}: '{result}'")
            break
    print()

def run_all_examples():
    print("KADEMLIA ALGORITHM DEMONSTRATION\n")
    print("=" * 50)
    
    demonstrate_xor_distance()
    demonstrate_bucket_structure()
    demonstrate_lookup_process()
    demonstrate_routing_efficiency()
    demonstrate_fault_tolerance()
    
    print("=" * 50)
    print("KEY ADVANTAGES:")
    print("• O(log n) lookup complexity")
    print("• Self-organizing network topology")
    print("• Fault tolerance through redundancy")
    print("• Efficient routing with XOR metric")
    print("• Used in BitTorrent, Ethereum, IPFS")

if __name__ == "__main__":
    run_all_examples()
