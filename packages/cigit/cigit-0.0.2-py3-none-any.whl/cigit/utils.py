import subprocess
import yaml


def load_auth(file_name: str = ".ci-auth.yml"):
    """Load the credentials from a YAML file"""

    with open(file_name, "r") as f:
        pipeline = yaml.safe_load(f)
        return pipeline


def command(command: str):
    """Run Shell Command"""
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode("utf-8")
    if result.returncode != 0:
        output = "$ERROR"
    return output
