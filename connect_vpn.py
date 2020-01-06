from shell import run_shell, notify

def list_vpn():
    output = run_shell("nmcli connection show | awk '/vpn/{print}' ")
    names = output.split('\n')
    names.pop()
    devices = list(map(lambda i: i.split()[3], names))
    names = list(map(lambda i: i.split()[0], names))
    return names, devices

def disconnect_all():
    vpns, devs = list_vpn()
    for vpn, dev in zip(vpns, devs):
        if dev != '--':
            run_shell('nmcli connection down {}'.format(vpn))
    notify("Disconnected from the VPN")

def connect(connection_name):
    run_shell('nmcli connection up {}'.format(connection_name))
    notify("Using the VPN: {}".format(connection_name))

def connect_with_menu():
    vpns, _ = list_vpn()
    names_pretty = list(map(lambda i: i.split('.')[0], vpns))
    names_pretty = ["disconnect"] + names_pretty
    choice = run_shell('echo -e "{}" | dmenu -l {} -fn {}'.format(
                       '\n'.join(names_pretty),
                       len(names_pretty),
                       "mono:pixelsize=20:antialias=true",
                       ))
    choice = choice[:-1] # delete traiting \n 
    if choice == '':
        return
    
    choice_idx = names_pretty.index(choice)
    disconnect_all()
    if choice_idx > 0:
        connect(vpns[choice_idx-1])

if __name__ == "__main__":
    connect_with_menu()
