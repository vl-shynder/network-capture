import pyshark
import re
import threading
from notifypy import Notify

DEBUG=False

def show_notification(title, message):
    notification = Notify()
    notification.title = title
    notification.message = message
    notification.send(block=False)

# Define the target domain
possible_host_names = [
    "meet.google.com",
    "hangouts.*.google.com",
]

def valid_host_name(host_name):
    # Check if host name exists in possible_host_names condirecing that * means any word
    for possible_host_name in possible_host_names:
        if possible_host_name == host_name:
            return True
        if '*' in possible_host_name:
            possible_host_name = possible_host_name.replace('*', '.*')
            if re.match(possible_host_name, host_name):
                return True
    return False

def on_valid_host_name(host_name, channel):
    show_notification("Discovered Host", f"Discovered host: {host_name}")
    print(f"Discovered host: {host_name} on channel: {channel}")

def packet_callback(packet):
    try:
        if 'tls' in packet and hasattr(packet.tls, 'handshake_extensions_server_name'):
            sni = packet.tls.handshake_extensions_server_name
            if (DEBUG):
                print(f"TLS: {sni}")
            if valid_host_name(sni):
                on_valid_host_name(sni, 'tls')

        if 'http' in packet and hasattr(packet.http, 'host'):
            host = packet.http.host
            if (DEBUG):
                print(f"HTTP: {host}")
            if valid_host_name(host):
                on_valid_host_name(host, 'http')

    except AttributeError as e:
        print(f"Attribute error: {e}")

def capture_on_interface(interface_name):
    try:
        capture = pyshark.LiveCapture(interface=interface_name)
        print(f"Capturing packets on interface: {interface_name}")
        capture.apply_on_packets(packet_callback)
    except Exception as e:
        print(f"Error capturing packets on {interface_name}: {e}")



interfaces = ['en0']  # List your interfaces here

threads = []
for iface in interfaces:
    thread = threading.Thread(target=capture_on_interface, args=(iface,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
