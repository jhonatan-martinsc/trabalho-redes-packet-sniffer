import struct

def unpack_dns(data):
    try:
        # Extrai Transaction ID e Flags (primeiros 4 bytes)
        transaction_id, flags = struct.unpack('! H H', data[:4])
        
        # Extração básica do Query Name (QNAME começa no byte 12)
        query_name = ""
        idx = 12
        while idx < len(data):
            length = data[idx]
            if length == 0 or length > 63: # Fim do domínio ou formato inválido
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