# @alethpraxis
# Here Thread connection begins

'''
You can do anything with your own code.
You must respect everyone else's.

'''


# main.py

import click
import time
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from commands.iface import show_interfaces
from commands.speed import show_speed
from commands.health import show_health
# from .commands.iface import iface as show_interfaces

@click.group()
@click.version_option(
    version="0.1.0",
    prog_name="tantu",
    # message="%(prog)s %(version)s"
    message="%(prog)s v%(version)s — Thread that connects"

)
def cli():
    """Tantu — Thread that connects."""
    pass

@cli.command()
# @click.option("--json", is_flag=True, help="Output in JSON format")
# @click.option("--verbose", is_flag=True, help="Show additional details")
@click.option("--name", type=str, default=None, help="Show details for specific interface")
def iface(name):
    """Inspect and explore network interfaces."""
    # click.echo("Checking interface...")
    # time.sleep(3)
    show_interfaces(name)

@cli.command()
# @click.option("--json", is_flag=False, help="Output in JSON format")
# @click.option("--verbose", is_flag=False, help="Show additional details")
# @click.option("--ping_only", is_flag=False, help="Run only latency/ping test")
# @click.option("--export", type=str, default=None ,help="Export results to file")
def speed():
    """Measure Internet speed and performance."""
    show_speed()

@cli.command()
# @click.option("--duration", type=int, default=10, show_default=True, help="Output in JSON format")
# @click.option("--verbose", is_flag=True, help="Show additional details")
# @click.option("--json", is_flag=True, help="Show details for specific interface")
def health():
    """Diagnose network health and identify problems."""
    # click.echo("Checking health...")
    show_health()


if __name__ == "__main__":
    cli()

