# Interface statistics
# import os
# import socket

# class interfaceCheck:
#     def __init__(self):
#         self.interfaces = []
#         self.gateway = None
#         self.active = None
#     def check(self):
#         self.interfaces = self.get_interfaces()
#         self.gateway = self.get_gateway()
#         self.active =  self.get_active()
#     def get_interfaces():
#         pass
#     def get_gateway():
#         pass
#     def get_active():
#         pass

import click
import psutil
import socket
import platform
import re
import subprocess

# os_name = platform.system()

stats = psutil.net_if_stats()
addrs = psutil.net_if_addrs()



# def get_windows_gateway():
#     """Get default gateway on Windows using route table."""
#     try:
#         output = subprocess.check_output(
#             ["route", "print", "0.0.0.0"],
#             text=True,
#             encoding="utf-8"
#         )
#         for line in output.splitlines():
#             parts = line.split()
#             # Expected route row: 0.0.0.0  0.0.0.0  192.168.1.1 ...
#             if len(parts) >= 4 and parts[0] == "0.0.0.0":
#                 return parts[3]
#     except Exception:
#         pass
#     return "-"

# def get_default_gateway(): 
#     """Return the system default gateway, cross-platform."""
#     if platform.system() == "Windows":
#         return get_windows_gateway()
#     return get_unix_gateway()


def get_verify(status, ip):
    if ip.startswith("169.254"):
        return "[warn]"
    if status == "DOWN":
        return "[fail]"
    return "[ok]"


def show_interface_details(name, status, ipv4, verdict):
    click.echo("── Interface Details ─────────────────────")
    click.echo(f"  Name      : {name}")
    click.echo(f"  Status    : {status}")
    click.echo(f"  IPv4      : {ipv4}")
    click.echo(f"  Verdict   : {verdict}")
    click.echo("─────────────────────────────────────────")



def show_interfaces(name=None):
    # gateway = None
    # default_gateway = get_default_gateway()
    
    interfaces = psutil.net_if_addrs()
    found = False

    #loop-1
    # for iface_name, address in  interfaces.items():
    #     if name and iface_name != name:
    #         continue
    #     ipv4 = ""
    #     for addr in address:
    #         if addr.family == socket.AF_INET:
    #             ipv4 = addr.address
    #             break
    #     status = "UP" if stats[iface_name].isup else "DOWN"
    #     verdict = get_verify(status, ipv4)

    #     if name:
    #         show_interface_details(
    #             iface_name,
    #             status,
    #             ipv4,
    #             verdict
    #         )
    #         return

        # click.echo(
        #     f"  {iface_name:<35} {status:<10} {ipv4:<16} {verdict}"
        # )

    #loop-2
    # print(f"  {'INTERFACE':<35} {'STATUS':<10} {'IPv4':<16} {'VERDICT'}")
    # print("-"*85)

    # for name,address in interfaces.items():
    #     # print(f"ifaces: {name}")
    #     ipv4 = "-"
    #     for addr in address:
    #         if addr.family == socket.AF_INET:
    #             # print(f" family : {addr.family}")
    #             ipv4 = addr.address
    #             break
    #             # print(f" netmask : {addr.netmask}")
    #     # print(f" Gateway : {addr.gateway}")
    #     status = "UP" if stats[name].isup else "DOWN"

    #     # click.echo(f"  {name:<38} {status:<10} {ipv4:>18} {verdict:>11}")
    #     click.echo(f"  {name:<35} {status:<10} {ipv4:<16} {verdict}")

    if not name:
        click.echo(f"{'INTERFACE':<35} {'STATUS':<10} {'IPv4':<16} {'VERDICT'}")
        click.echo("-" * 85)

    for iface_name, address in interfaces.items():

        if name and iface_name != name:
            continue

        found = True

        ipv4 = "-"

        for addr in address:
            if addr.family == socket.AF_INET:
                ipv4 = addr.address
                break

        status = "UP" if stats[iface_name].isup else "DOWN"
        verdict = get_verify(status, ipv4)

        if name:
            show_interface_details(
                iface_name,
                status,
                ipv4,
                verdict
            )
            return

        click.echo(
            f"{iface_name:<35} {status:<10} {ipv4:<16} {verdict}"
        )
   

    if name and not found:
        click.echo(f"Interface '{name}' not found")
    else:
         click.echo("-" * 85)



    # if not name:
    #     click.echo("-" * 85)

    # print("-"*85)
    total =  len(stats)
    up = 0
    down = 0
    for s in stats.values():
        if s.isup:
            up += 1
        else:
            down += 1
    # print(f"Interface not found")
# print(f" COUNT:  {up} up  {down} down  {total} total")

