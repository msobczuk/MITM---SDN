#libraries
from pox.lib.packet.arp import arp
from pox.lib.addresses import EthAddr, IPAddr
from pox.lib.packet.ethernet import ethernet
from pox.core import core
import logging as log
import struct

arp_cache = {} #IP/MAC dictionary

def _handle_PacketIn (event):
    packet = event.parsed
    arp_packet = packet.find('arp') #check for ARP packets

    # check if the packet is an ARP packet
    if arp_packet:
        src_ip = arp_packet.protosrc #host IP
        src_mac = arp_packet.hwsrc #host MAC
        print "ARP packet received from IP: ", src_ip, " MAC: ", src_mac
        #check ARP Spoofing
        if src_ip in arp_cache:
            if arp_cache[src_ip] == src_mac:
                print("Nothing unusual")
            else:
                print("ARP Spoofing detected - MITM is working!")
        else:
            arp_cache[src_ip] = src_mac #updating entries in arp_cache

def launch ():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
