"""
Git Clone & Pull with CI-Pipeline

Linux: Disable History <unset HISTFILE>
"""
import os
import functools
from .pipeline import run_pipeline
from .utils import load_auth, command


def git_base(
    append: str = None,
    method: str = None,
    url: str = None,
    username: str = None,
    password: str = None,
    path: str = None,
    shell: bool = False,
):
    """Get Git from Https"""
    text = ""
    secure = False

    # Clean
    if url.startswith("https"):
        secure = True
    if secure:
        repo = url.replace("https://", "")
    else:
        repo = url.replace("http://", "")

    # Build
    if secure:
        text = f"git {method} https://{username}:{password}@{repo} {path or ''}".strip()
    else:
        text = f"git {method} http://{username}:{password}@{repo} {path or ''}".strip()

    # os.system(cmd_text + "; history -d $(history 1)")
    cmd_text = f"{append or ''} " + text
    if shell:
        return command(cmd_text)
    else:
        os.system(cmd_text)


def git_run(
    method: str = "clone",
    file_name: str = ".ci-auth.yml",
    go_to: bool = False,
    shell: bool = False,
):
    """Load setup from a file"""
    config = load_auth(file_name)
    path = None
    append = None
    if method == "clone":
        path = config.get("path")
    if go_to:
        append = f'cd {config.get("path")} &&'
        shell = True
    return git_base(
        method=method,
        url=config.get("url"),
        username=config.get("username"),
        password=config.get("password"),
        path=path,
        append=append,
        shell=shell,
    )


def pull(file_name: str = ".ci-auth.yml"):
    """Git Pull"""
    do_pull = functools.partial(git_run, method="pull", file_name=file_name, go_to=True)
    log = do_pull()
    if "Already up to date" not in log:
        run_pipeline()


def clone(file_name: str = ".ci-auth.yml"):
    """Git Clone"""
    do_clone = functools.partial(
        git_run, file_name=file_name, method="clone", shell=True
    )
    log = do_clone()
    if "$ERROR" not in log:
        run_pipeline()
