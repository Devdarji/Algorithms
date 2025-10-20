"""
Bencode Format Explanation and Examples

Bencode is a simple encoding format used by BitTorrent for storing and transmitting data.
It supports 4 data types: strings, integers, lists, and dictionaries.

Format Rules:
- Strings: <length>:<string> (e.g., "5:hello")
- Integers: i<integer>e (e.g., "i42e")
- Lists: l<contents>e (e.g., "l5:helloi42ee")
- Dictionaries: d<contents>e with sorted keys (e.g., "d3:keyi123ee")
"""

from parser import encode, decode

def run_examples():
    print("=== BENCODE EXAMPLES ===\n")
    
    # 1. String Examples
    print("1. STRINGS:")
    examples = [
        b"hello",
        b"",
        b"BitTorrent protocol"
    ]
    for s in examples:
        encoded = encode(s)
        decoded = decode(encoded)
        print(f"  {s} → {encoded} → {decoded}")
    print()
    
    # 2. Integer Examples
    print("2. INTEGERS:")
    examples = [42, 0, -123, 999999]
    for i in examples:
        encoded = encode(i)
        decoded = decode(encoded)
        print(f"  {i} → {encoded} → {decoded}")
    print()
    
    # 3. List Examples
    print("3. LISTS:")
    examples = [
        [],
        [b"hello"],
        [b"hello", 42],
        [b"nested", [b"list", 123]]
    ]
    for lst in examples:
        encoded = encode(lst)
        decoded = decode(encoded)
        print(f"  {lst} → {encoded} → {decoded}")
    print()
    
    # 4. Dictionary Examples
    print("4. DICTIONARIES:")
    examples = [
        {},
        {b"key": b"value"},
        {b"announce": b"http://tracker.com", b"port": 8080},
        {b"info": {b"name": b"file.txt", b"size": 1024}}
    ]
    for d in examples:
        encoded = encode(d)
        decoded = decode(encoded)
        print(f"  {d}")
        print(f"  → {encoded}")
        print(f"  → {decoded}")
        print()
    
    # 5. BitTorrent .torrent File Example
    print("5. TORRENT FILE STRUCTURE:")
    torrent = {
        b'announce': b'http://tracker.example.com:8080/announce',
        b'announce-list': [
            [b'http://tracker1.com:8080/announce'],
            [b'http://tracker2.com:8080/announce']
        ],
        b'info': {
            b'name': b'example-file.txt',
            b'length': 2048,
            b'piece length': 32768,
            b'pieces': b'abcdef1234567890' * 2  # SHA1 hashes
        },
        b'creation date': 1634567890,
        b'created by': b'Example Client v1.0'
    }
    
    encoded = encode(torrent)
    decoded = decode(encoded)
    print(f"Torrent structure encoded length: {len(encoded)} bytes")
    print(f"Successfully decoded: {decoded[b'info'][b'name']}")
    print()
    
    # 6. Edge Cases
    print("6. EDGE CASES:")
    edge_cases = [
        (b'0:', "Empty string"),
        (b'i0e', "Zero integer"),
        (b'i-42e', "Negative integer"),
        (b'le', "Empty list"),
        (b'de', "Empty dictionary"),
        (b'll5:helloeee', "Nested empty list")
    ]
    
    for bencode_data, description in edge_cases:
        try:
            decoded = decode(bencode_data)
            print(f"  {description}: {bencode_data} → {decoded}")
        except Exception as e:
            print(f"  {description}: {bencode_data} → ERROR: {e}")
    print()
    
    # 7. Manual Parsing Examples
    print("7. STEP-BY-STEP PARSING:")
    manual_examples = [
        b'5:hello',
        b'i-42e',
        b'l5:helloi42ee',
        b'd3:keyi123ee'
    ]
    
    for data in manual_examples:
        print(f"  Parsing: {data}")
        result = decode(data)
        print(f"  Result: {result}")
        print(f"  Type: {type(result)}")
        print()

if __name__ == "__main__":
    run_examples()
