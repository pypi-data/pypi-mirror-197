import yaml
import subprocess
import os
import pathlib
from .utils import load_auth


def run_commands(commands):
    """Run All Scripts"""
    for command in commands:
        subprocess.call(command, shell=True)


def enforce_list(script):
    """Script(s) as List"""
    script = script or []
    if isinstance(script, str):
        script = [script]
    return script


def collect_jobs_by_stage(file_name: str):
    """Group Jobs By Stage"""

    jobs_by_stage = {}

    # Load the pipeline definition from a YAML file
    with open(file_name, "r") as f:
        pipeline = yaml.safe_load(f)

    # Group the jobs by stage
    for job in pipeline:
        if job not in ["stages"]:
            obj = pipeline[job]
            obj["name"] = job
            stage = obj["stage"]
            if stage not in jobs_by_stage:
                jobs_by_stage[stage] = []
            jobs_by_stage[stage].append(obj)
    return jobs_by_stage


def run_pipeline(
    stages: list | None = None, file_name: str = ".ci-git.yml", break_length: int = 70
):
    """CI/CD Pipeline"""

    jobs_by_stage = collect_jobs_by_stage(file_name)

    do_check = False
    if stages:
        do_check = True

    # Config
    config = load_auth()

    # Git Repo Path
    repo_path = str(pathlib.Path(config.get("path")).resolve())
    os.chdir(repo_path)

    # Loop through each stage and execute the jobs in order
    for stage, jobs in jobs_by_stage.items():
        if do_check and stage not in stages:
            continue
        else:
            for job in jobs:
                print("-" * break_length)
                print(f'Stage: {stage} | Executing Job: {job["name"]}')
                print("-" * break_length)
                script = job.get("script", [])
                script = enforce_list(script)
                run_commands(script)
                print("\n")
                print("~" * break_length)
                print(f'Stage: {stage} | Job Completed: {job["name"]}', end="\n")
                print("~" * break_length, end="\n\n")

    # Done
    print("=" * (break_length))
    print("All Jobs Completed.")
