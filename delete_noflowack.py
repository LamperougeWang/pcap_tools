#!/usr/bin/env python
# coding=utf-8

from scapy.utils import PcapReader, PcapWriter
from scapy.all import *
FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80
design_flow_count = 999983

def hash_pkt(pkt):
    # ip string to int
    src_ip = pkt[IP].src
    dst_ip = pkt[IP].dst
    sport = pkt[TCP].sport
    dport = pkt[TCP].dport
    return (hash(src_ip) + hash(dst_ip) + hash(sport) + hash(dport)) % design_flow_count

# packet_count = 800000

pcap_reader = PcapReader("../bigFlows.pcap")
pcap_writer = PcapWriter("./bigFlows_aggregated.pcap")


# generate
src_ips = ["0.0.0.0"] * design_flow_count
dst_ips = ["0.0.0.0"] * design_flow_count
sports = [0] * design_flow_count
dports = [0] * design_flow_count

flow_syn = [False] * design_flow_count



# read & write
while True:
    pkt = pcap_reader.read_packet()
    if pkt == None:
        break
    if TCP in pkt:
        hash_val = hash_pkt(pkt)
        if  pkt[TCP].flags & SYN:
            src_ips[hash_val] = pkt[IP].src
            dst_ips[hash_val] = pkt[IP].dst
            sports[hash_val] = pkt[TCP].sport
            dports[hash_val] = pkt[TCP].dport
            flow_syn[hash_val] = True
            print("Bucket " + str(hash_val) + " has been set")
            pcap_writer.write(pkt)
        else:
            if flow_syn[hash_val]:
                pcap_writer.write(pkt)


pcap_writer.flush()
pcap_writer.close()

