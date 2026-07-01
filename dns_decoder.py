import struct

def unpack_dns(data):
    try:
        transaction_id, flags, qdcount = struct.unpack('! H H H', data[:6])
        
        query_name = ""
        idx = 12
        while idx < len(data):
            length = data[idx]
            if length == 0:
                idx += 1
                break
            if length & 0xC0:
                query_name += '[ptr]'
                idx += 2
                break
            query_name += data[idx+1:idx+1+length].decode('utf-8', errors='ignore') + "."
            idx += length + 1
        
        idx += 4
        
        return {
            'transaction_id': hex(transaction_id),
            'flags': hex(flags),
            'query_name': query_name.strip('.'),
            'type': 'Consulta DNS'
        }
    except Exception:
        return None