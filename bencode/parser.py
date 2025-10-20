class BencodeParser:
    def __init__(self, data: bytes):
        self.data = data
        print('data', self.data)
        self.index = 0
    
    def decode(self):
        return self._decode_value()
    
    def _decode_value(self):
        if self.index >= len(self.data):
            raise ValueError("Unexpected end of data")
        
        char = chr(self.data[self.index])
        print('char', char)
        
        if char.isdigit():
            return self._decode_string()
        elif char == 'i':
            return self._decode_integer()
        elif char == 'l':
            return self._decode_list()
        elif char == 'd':
            return self._decode_dict()
        else:
            raise ValueError(f"Invalid bencode character: {char}")
    
    def _decode_string(self):
        colon_pos = self.data.find(b':', self.index)
        if colon_pos == -1:
            raise ValueError("Invalid string format")
        
        length = int(self.data[self.index:colon_pos])
        self.index = colon_pos + 1
        
        if self.index + length > len(self.data):
            raise ValueError("String length exceeds data")
        
        result = self.data[self.index:self.index + length]
        self.index += length
        return result
    
    def _decode_integer(self):
        self.index += 1  # skip 'i'
        end_pos = self.data.find(b'e', self.index)
        if end_pos == -1:
            raise ValueError("Invalid integer format")
        
        result = int(self.data[self.index:end_pos])
        self.index = end_pos + 1
        return result
    
    def _decode_list(self):
        self.index += 1  # skip 'l'
        result = []
        
        while self.index < len(self.data) and chr(self.data[self.index]) != 'e':
            result.append(self._decode_value())
        
        if self.index >= len(self.data):
            raise ValueError("Unterminated list")
        
        self.index += 1  # skip 'e'
        return result
    
    def _decode_dict(self):
        self.index += 1  # skip 'd'
        result = {}
        
        while self.index < len(self.data) and chr(self.data[self.index]) != 'e':
            key = self._decode_value()
            if not isinstance(key, bytes):
                raise ValueError("Dictionary key must be string")
            value = self._decode_value()
            result[key] = value
        
        if self.index >= len(self.data):
            raise ValueError("Unterminated dictionary")
        
        self.index += 1  # skip 'e'
        return result

def encode(obj):
    if isinstance(obj, bytes):
        return str(len(obj)).encode() + b':' + obj
    elif isinstance(obj, str):
        return encode(obj.encode())
    elif isinstance(obj, int):
        return b'i' + str(obj).encode() + b'e'
    elif isinstance(obj, list):
        return b'l' + b''.join(encode(item) for item in obj) + b'e'
    elif isinstance(obj, dict):
        items = []
        for key in sorted(obj.keys()):
            items.append(encode(key))
            items.append(encode(obj[key]))
        return b'd' + b''.join(items) + b'e'
    else:
        raise ValueError(f"Cannot encode type: {type(obj)}")

def decode(data: bytes):
    parser = BencodeParser(data)
    return parser.decode()

# Example usage
if __name__ == "__main__":
    # Test encoding
    data = {
        b'announce': b'http://tracker.example.com:8080/announce',
        b'info': {
            b'name': b'example.txt',
            b'length': 1024,
            b'piece length': 32768
        }
    }
    
    encoded = encode(data)
    print(f"Encoded: {encoded}")
    
    # Test decoding
    decoded = decode(encoded)
    print(f"Decoded: {decoded}")
    
    # Test individual types
    print(f"String: {decode(b'5:hello')}")
    print(f"Integer: {decode(b'i42e')}")
    print(f"List: {decode(b'l5:helloi42ee')}")
