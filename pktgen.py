#!/usr/bin/python
import sys
from scapy.all import *

def send_trans_pkt(eth_src, eth_dst, ip_src, ip_dst, proto, port_src, port_dst, pkt_size, eth):
	if proto == 'TCP':
		print ip_src
		trans_pkt = Ether(src = eth_src, dst = eth_dst) / IP(src = ip_src, dst = ip_dst) / TCP(sport = port_src, dport = port_dst, flags='S')
	elif proto == 'UDP':
		trans_pkt = Ether(src = eth_src, dst = eth_dst) / IP(src = ip_src, dst = ip_dst) / UDP(sport = port_src, dport = port_dst)
	else:
		print 'error\n'
		return
	if len(trans_pkt) < pkt_size:
		trans_pkt = trans_pkt / Raw(RandString(size=pkt_size)) 
	sendp(trans_pkt, iface = eth)


def main():
    for i in range(0, 2000):
    	send_trans_pkt('11:11:11:11:11:11', '22:22:22:22:22:22', '10.0.0.3', '10.0.0.4', 'TCP', 100, 99, 10, 'p1p1')


if __name__ == '__main__':
	main()
