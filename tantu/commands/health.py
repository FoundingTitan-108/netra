import time
import click
import psutil
import socket
import platform
from datetime import datetime

stats = psutil.net_if_stats()
addrs = psutil.net_if_addrs()


VIRTUAL_KEYWORDS = (
    "vmware",
    "vbox",
    "virtual",
    "hyper-v",
    "vethernet",
    "docker",
    "loopback",
    "teredo",
    "bluetooth",
)


def is_virtual_interface(name):
    name = name.lower()
    return any(keyword in name for keyword in VIRTUAL_KEYWORDS)


def get_active_interface():
    interfaces = psutil.net_if_addrs()

    candidates = []

    for iface_name, addresses in interfaces.items():

        if not stats[iface_name].isup:
            continue

        if is_virtual_interface(iface_name):
            continue

        ipv4 = "-"

        for addr in addresses:
            if addr.family == socket.AF_INET:
                ipv4 = addr.address
                break

        if ipv4 == "-" or ipv4.startswith("169.254") or ipv4.startswith("127."):
            continue

        candidates.append({
            "name": iface_name,
            "ipv4": ipv4,
            "speed": stats[iface_name].speed,
        })

    if not candidates:
        return None

    priority = ["wi-fi", "wifi", "wlan", "ethernet", "eth"]

    for p in priority:
        for iface in candidates:
            if p in iface["name"].lower():
                return iface

    return candidates[0]

# print("Selected Interface:", active["name"])
# print("Available Interfaces:")

# for iface in psutil.net_io_counters(pernic=True):
#     print(iface)


# def get_live_speed(interface):
#     stats = psutil.net_io_counters(pernic=True)

#     if interface not in stats:
#         print("Available interfaces:", list(stats.keys()))
#         return None, None

#     old = stats[interface]
#     time.sleep(1)
#     new = psutil.net_io_counters(pernic=True)[interface]

#     bytes_recv = new.bytes_recv - old.bytes_recv
#     bytes_sent = new.bytes_sent - old.bytes_sent

#     download = (bytes_recv * 8) / (1024 * 1024)  # Mbps
#     upload = (bytes_sent * 8) / (1024 * 1024)

#     return round(download, 2), round(upload, 2)

def show_health():
    active = get_active_interface()

    total = len(stats)
    up = sum(1 for s in stats.values() if s.isup)

    click.echo("Health Report")
    click.echo()
    

    click.echo("System")
    click.echo("------")
    click.echo(f"{'Host':<10}: {platform.node()}")
    click.echo(f"{'OS':<10}: {platform.system()} {platform.release()}")
    click.echo(f"{'Time':<10}: {datetime.now().strftime('%H:%M:%S')}")

    click.echo()

    click.echo("Network")
    click.echo("-------")

    if active:
        click.echo(f"{'Interface':<10}: {active['name']}")
        click.echo(f"{'IPv4':<10}: {active['ipv4']}")
        click.echo(f"{'Internet':<10}: Connected")
        health = "Healthy"
    else:
        click.echo(f"{'Interface':<10}: -")
        click.echo(f"{'IPv4':<10}: -")
        click.echo(f"{'Internet':<10}: Disconnected")
        health = "Critical"

    click.echo()

    click.echo("Summary")
    click.echo("-------")
    click.echo(f"{'Interfaces':<10}: {total} ({up} UP)")
    click.echo(f"{'Health':<10}: {health}")