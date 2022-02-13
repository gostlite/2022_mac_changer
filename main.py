#!/usr/bin/env python
import subprocess
import optparse
import re

def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change the mac address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New mac address")
    (options, argument) = parser.parse_args()
    if not options.interface:
        parser.error('Please input the interface')
    elif not options.new_mac:
        parser.error("Input the mac address")
    return options


def change_mac(interface, mac):
    print(f"changing mac address for {interface} to {mac}")
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()
    old_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if not old_mac:
        print("could not read mac address")
    else:
        return old_mac.group(0)
options= get_args()
current_mac = get_current_mac(options.interface)
old_mac = current_mac
print(f"current mac is {current_mac}")
change_mac(options.interface, options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print(f" Your mac address was changed from {old_mac} to {current_mac}")
else:
    print("Mac address wasn't successfully changed")
