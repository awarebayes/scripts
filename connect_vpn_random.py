# add this to your startup: sleep 60 && python3 ~/.scripts/connect_vpn_random.py &
import random
from shell import run_shell, notify
from connect_vpn import disconnect_all, connect

def connect_random():
    vpns = run_shell("nmcli connection show | awk '/vpn/{print $1}'")
    vpns = vpns.split()
    if not vpns:
        notify("Couldn't connect to the VPN!")
        return
    rand_vpn = random.choice(vpns)
    disconnect_all()
    connect(rand_vpn)

if __name__ == "__main__":
    connect_random()
