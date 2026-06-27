import struct
import socket

def unpack_arp(data):
    try:
        # Cabeçalho ARP tem 28 bytes
        hw_type, proto_type, hw_size, proto_size, opcode, src_mac, src_ip, dest_mac, dest_ip = struct.unpack('! H H B B H 6s 4s 6s 4s', data[:28])
        
        return {
            'hw_type': hw_type,
            'proto_type': hex(proto_type),
            'opcode': opcode,
            'src_mac': ':'.join(map('{:02x}'.format, src_mac)).upper(),
            'src_ip': socket.inet_ntoa(src_ip),
            'dest_mac': ':'.join(map('{:02x}'.format, dest_mac)).upper(),
            'dest_ip': socket.inet_ntoa(dest_ip)
        }
    except Exception:
        return None