import struct

def unpack_dns(data):
    try:
        # Extrai os primeiros 4 bytes: ID da transação e Flags
        transaction_id, flags = struct.unpack('! H H', data[:4])
        
        # O Query Name começa a partir do byte 12 no cabeçalho DNS
        query_name = ""
        idx = 12
        while idx < len(data):
            length = data[idx]
            if length == 0 or length > 63: 
                break
            query_name += data[idx+1:idx+1+length].decode('utf-8', errors='ignore') + "."
            idx += length + 1
            
        return {
            'transaction_id': hex(transaction_id),
            'flags': hex(flags),
            'query_name': query_name.strip('.'),
            'type': 'Consulta DNS'
        }
    except Exception:
        return None