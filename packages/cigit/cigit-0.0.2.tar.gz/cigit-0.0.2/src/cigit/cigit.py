import argparse
from .pipeline import run_pipeline as run
from .gitman import clone, pull


def cli():
    """Command Line Interface"""

    # Parser
    parser = argparse.ArgumentParser()

    # Args
    parser.add_argument("action", help="Options: [run, clone, pull]")
    parser.add_argument("-s", "--stages", help="Stages of the Pipeline you want to run")
    parser.add_argument("-c", "--config", help="Use custom setting's file")

    args = parser.parse_args()

    match args.action:
        case "run":
            run()
        case "clone":
            clone()
        case "pull":
            pull()
