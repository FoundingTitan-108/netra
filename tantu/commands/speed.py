# import speedtest
# import click
# import subprocess
# import re


# def get_ping():
#     output = subprocess.check_output(
#         ["ping", "8.8.8.8", "-n", "4"],
#         text=True
#     )

#     match = re.search(r"Average = (\d+)ms", output)

#     if match:
#         return int(match.group(1))

# def score_download(download):
#     if download >= 100:
#         return 5
#     elif download >= 50:
#         return 4
#     elif download >= 20:
#         return 3
#     elif download >= 5:
#         return 2
#     return 1


# def score_upload(upload):
#     if upload >= 50:
#         return 5
#     elif upload >= 20:
#         return 4
#     elif upload >= 10:
#         return 3
#     elif upload >= 3:
#         return 2
#     return 1


# def score_ping(ping):
#     if ping <= 20:
#         return 5
#     elif ping <= 50:
#         return 4
#     elif ping <= 100:
#         return 3
#     elif ping <= 200:
#         return 2
#     return 1


# def quality_label(score):
#     if score >= 4.5:
#         return "Excellent"
#     elif score >= 3.5:
#         return "Good"
#     elif score >= 2.5:
#         return "Fair"
#     elif score >= 1.5:
#         return "Poor"
#     return "Bad"


# def show_speed():
#     def calculate_quality(download, upload, ping):
#         scores = [
#             score_download(download),
#             score_upload(upload),
#             score_ping(ping)
#         ]

#         avg = sum(scores) / len(scores)
#         return avg

#     click.echo(f"Checking speed....")
#     st = speedtest.Speedtest()
#     download = st.download() / 1_000_000
#     upload = st.upload() / 1_000_000
#     results = st.results.dict()
#     ping = get_ping()
#     quality = calculate_quality(download, upload, ping)
#     label = quality_label(quality)

#     # ping_ms = seconds * 1000

#     # st = speedtest.Speedtest()
#     # best = st.get_server()
   

#     click.echo(f"Download : {download:.2f} Mbps")
#     click.echo(f"Upload : {upload:.2f} Mbps")
#     click.echo(f"Ping : {ping} ms")
#     click.echo(f"Quality : {label}")
#     # click.echo(f"Server: {best['name']}")
#     # click.echo(f"Server: {best}")

import socket
import subprocess
import re
import click
import speedtest

# is active
def has_internet(timeout=3):
    """Check if the system has Internet connectivity."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout)
        return True
    except OSError:
        return False


#ping
def get_ping():
    """Return average ping in milliseconds."""

    try:
        output = subprocess.check_output(
            ["ping", "8.8.8.8", "-n", "4"],
            text=True
        )

        match = re.search(r"Average = (\d+)ms", output)

        if match:
            return int(match.group(1))

    except Exception:
        pass

    return None

# quality

def score_download(download):
    if download >= 100:
        return 5
    elif download >= 50:
        return 4
    elif download >= 20:
        return 3
    elif download >= 5:
        return 2
    return 1


def score_upload(upload):
    if upload >= 50:
        return 5
    elif upload >= 20:
        return 4
    elif upload >= 10:
        return 3
    elif upload >= 3:
        return 2
    return 1


def score_ping(ping):
    if ping <= 20:
        return 5
    elif ping <= 50:
        return 4
    elif ping <= 100:
        return 3
    elif ping <= 200:
        return 2
    return 1


def calculate_quality(download, upload, ping):
    scores = [
        score_download(download),
        score_upload(upload),
        score_ping(ping)
    ]

    return sum(scores) / len(scores)


def quality_label(score):
    if score >= 4.5:
        return "Excellent"
    elif score >= 3.5:
        return "Good"
    elif score >= 2.5:
        return "Fair"
    elif score >= 1.5:
        return "Poor"
    return "Bad"


#showspeed
def show_speed():

    click.echo("Checking speed...\n")

    if not has_internet():
        click.echo("Internet : Disconnected")
        click.echo("Download : -")
        click.echo("Upload   : -")
        click.echo("Ping     : -")
        click.echo("Quality  : Not Available")
        return

    try:
        st = speedtest.Speedtest()

        download = st.download() / 1_000_000
        upload = st.upload() / 1_000_000
        ping = get_ping()

        if ping is None:
            click.echo("Unable to measure ping.")
            return

        quality = calculate_quality(download, upload, ping)
        label = quality_label(quality)

        click.echo(f"{'Download':<10}: {download:.2f} Mbps")
        click.echo(f"{'Upload':<10}: {upload:.2f} Mbps")
        click.echo(f"{'Ping':<10}: {ping} ms")
        click.echo(f"{'Quality':<10}: {label}")

    except speedtest.ConfigRetrievalError:
        click.echo("Unable to contact the Speedtest service.")
    except speedtest.SpeedtestException as e:
        click.echo(f"Speedtest failed: {e}")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")