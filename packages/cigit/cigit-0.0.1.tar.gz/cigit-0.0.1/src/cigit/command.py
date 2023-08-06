import subprocess


def command(command: str):
    """Run Shell Command"""
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode("utf-8")
    if result.returncode != 0:
        output = "$ERROR"
    return output
