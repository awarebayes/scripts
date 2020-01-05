import subprocess

def run_shell(command, debug=True):
    if debug:
        print('running\n', command)
    output = subprocess.run(command, stdout=subprocess.PIPE,
                            text=True, shell=True).stdout
    return output

def list_vpn():
    output = run_shell("nmcli connection show", False)
    names = output.split('\n')
    names = list(filter(lambda i: 'vpn' in i, names))
    devices = list(map(lambda i: i.split()[3], names))
    names = list(map(lambda i: i.split()[0], names))
    return names, devices

def disconnect_all():
    vpns, devs = list_vpn()
    for vpn, dev in zip(vpns, devs):
        if dev != '--':
            run_shell('nmcli connection down {}'.format(vpn))

def main():
    vpns, _ = list_vpn()
    names_pretty = list(map(lambda i: i.split('.')[0], vpns))
    names_pretty = ["disconnect"] + names_pretty
    choice = run_shell('echo -e "{}" | dmenu -l {} -fn {}'.format(
                       '\n'.join(names_pretty),
                       len(names_pretty),
                       "mono:pixelsize=20:antialias=true",
                       ), False)
    choice = choice[:-1] # del traiting \n
    
    if choice == '':
        return
    
    choice_idx = names_pretty.index(choice)
    if choice_idx == 0:
        disconnect_all()
    else:
        run_shell('nmcli connection up {}'.format(vpns[choice_idx-1]))

main()

