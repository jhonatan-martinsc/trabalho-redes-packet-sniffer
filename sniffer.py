import socket
from general import *
import arp_decoder
import dns_decoder
import http_decoder
from networking.ethernet import Ethernet
from networking.ipv4 import IPv4
from networking.icmp import ICMP
from networking.tcp import TCP
from networking.udp import UDP
from networking.pcap import Pcap

TAB_1 = '\t - '
TAB_2 = '\t\t - '
TAB_3 = '\t\t\t - '
TAB_4 = '\t\t\t\t - '

DATA_TAB_1 = '\t   '
DATA_TAB_2 = '\t\t   '
DATA_TAB_3 = '\t\t\t   '
DATA_TAB_4 = '\t\t\t\t   '

def main():
    pcap = Pcap('capture.pcap')
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    try:
        while True:
            raw_data, addr = conn.recvfrom(65535)
            pcap.write(raw_data)
            eth = Ethernet(raw_data)

            print('\nEthernet Frame:')
            print(TAB_1 + 'Destination: {}, Source: {}, Protocol: {}'.format(eth.dest_mac, eth.src_mac, eth.proto))

            # IPv4
            if eth.proto == 8:
                ipv4 = IPv4(eth.data)
                print(TAB_1 + 'IPv4 Packet:')
                print(TAB_2 + 'Version: {}, Header Length: {}, TTL: {},'.format(ipv4.version, ipv4.header_length, ipv4.ttl))
                print(TAB_2 + 'Protocol: {}, Source: {}, Target: {}'.format(ipv4.proto, ipv4.src, ipv4.target))

                # ICMP
                if ipv4.proto == 1:
                    icmp = ICMP(ipv4.data)
                    print(TAB_1 + 'ICMP Packet:')
                    print(TAB_2 + 'Type: {}, Code: {}, Checksum: {},'.format(icmp.type, icmp.code, icmp.checksum))
                    print(TAB_2 + 'ICMP Data:')
                    print(format_multi_line(DATA_TAB_3, icmp.data))

                # TCP
                elif ipv4.proto == 6:
                    tcp = TCP(ipv4.data)
                    print(TAB_1 + 'TCP Segment:')
                    print(TAB_2 + 'Source Port: {}, Destination Port: {}'.format(tcp.src_port, tcp.dest_port))
                    print(TAB_2 + 'Sequence: {}, Acknowledgment: {}'.format(tcp.sequence, tcp.acknowledgment))
                    print(TAB_2 + 'Flags:')
                    print(TAB_3 + 'URG: {}, ACK: {}, PSH: {}'.format(tcp.flag_urg, tcp.flag_ack, tcp.flag_psh))
                    print(TAB_3 + 'RST: {}, SYN: {}, FIN:{}'.format(tcp.flag_rst, tcp.flag_syn, tcp.flag_fin))

                    if len(tcp.data) > 0:
                        # HTTP (Nova Implementação)
                        if tcp.src_port == 80 or tcp.dest_port == 80:
                            print(TAB_2 + 'HTTP Data (Interpretador Avançado):')
                            http_meta = http_decoder.unpack_http(tcp.data)
                            if http_meta and http_meta['method']:
                                print(TAB_3 + 'Method: {}'.format(http_meta['method']))
                                print(TAB_3 + 'Host: {}'.format(http_meta['host']))
                                print(TAB_3 + 'User-Agent: {}'.format(http_meta['user_agent']))
                            else:
                                print(format_multi_line(DATA_TAB_3, tcp.data))
                        else:
                            print(TAB_2 + 'TCP Data:')
                            print(format_multi_line(DATA_TAB_3, tcp.data))

                # UDP
                elif ipv4.proto == 17:
                    udp = UDP(ipv4.data)
                    print(TAB_1 + 'UDP Segment:')
                    print(TAB_2 + 'Source Port: {}, Destination Port: {}, Length: {}'.format(udp.src_port, udp.dest_port, udp.size))
                    
                    # DNS - (Nova Implementação)
                    if udp.src_port == 53 or udp.dest_port == 53:
                        print(TAB_2 + 'DNS Data (Interpretador Avançado):')
                        dns_info = dns_decoder.unpack_dns(udp.data)
                        if dns_info:
                            print(TAB_3 + 'Transaction ID: {}'.format(dns_info['transaction_id']))
                            print(TAB_3 + 'Flags: {}'.format(dns_info['flags']))
                            print(TAB_3 + 'Query Name: {}'.format(dns_info['query_name']))

                # Other IPv4
                else:
                    print(TAB_1 + 'Other IPv4 Data:')
                    print(format_multi_line(DATA_TAB_2, ipv4.data))

            # ARP - (Nova Implementação)
            elif eth.proto == 1544:
                print(TAB_1 + 'ARP Packet (Interpretador Avançado):')
                arp_info = arp_decoder.unpack_arp(eth.data)
                if arp_info:
                    print(TAB_2 + 'OpCode: {} | Protocol: {}'.format(arp_info['opcode'], arp_info['proto_type']))
                    print(TAB_2 + 'Sender: {} ({})'.format(arp_info['src_mac'], arp_info['src_ip']))
                    print(TAB_2 + 'Target: {} ({})'.format(arp_info['dest_mac'], arp_info['dest_ip']))

            else:
                print('Ethernet Data:')
                print(format_multi_line(DATA_TAB_1, eth.data))

    except KeyboardInterrupt:
        print('\nEncerrando...')
    finally:
        pcap.close()

if __name__ == '__main__':
    main()