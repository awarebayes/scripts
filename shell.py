import subprocess

def run_shell(command):
    output = subprocess.run(command, stdout=subprocess.PIPE,
                            text=True, shell=True).stdout
    return output

def notify(message):
    run_shell("notify-send '{}'".format(message))

