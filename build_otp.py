#!/usr/bin/env python3

import os
import re
import pathlib
import sys
import shutil
import tarfile
import git
import docker
import collections

otp_git_dir = os.getenv("OTP_GIT_DIR", "otp")
debian_vsn = os.getenv("DEBIAN_VSN", "")

codenames = {
    "14": "forky",
    "13": "trixie",
    "12": "bookworm",
    "11": "bullseye",
    "10": "buster",
    "9": "stretch",
    "8": "jessie",
    "7": "wheezy"
}

# content = ""
# with open("/etc/debian_version") as f:
#     content = f.read()
# debian_vsn = re.sub(r"^([0-9]+).*\n$", r"\1", content)

debian_pool = pathlib.Path("debian/" + debian_vsn + "/pool")
debian_pool.is_dir() or sys.exit("missing " + str(debian_pool))

tag = re.compile(r"^OTP-[0-9.]+$")

def match(repo_tag):
    return tag.match(str(repo_tag))

def tr(repo_tag):
    return re.sub(r'^OTP-([0-9.]+)$', r'\1', str(repo_tag))

last_vsn = {}
with git.Repo("otp") as repo:
    repo.remotes.origin.fetch()
    all_vsn = [tr(repo_tag) for repo_tag in repo.tags if match(repo_tag)]
    main_vsn = set(map(lambda x:x[0:4], all_vsn))
    last_vsn = dict([[(y[0:4], y) for y in all_vsn if y[0:4]==x][-1] for x in main_vsn])

    # create inputs
    for root_vsn, vsn in last_vsn.items():
        input_path = pathlib.Path("input")
        otp_src = f"otp_src_{root_vsn}"
        tarname = f"{otp_src}.tar.gz"
        full_path = input_path / tarname
        if full_path.is_file():
            continue

        print(f"create {str(full_path)}")

        print(f"  change to tag OTP-{vsn}")
        repo.head.reference = "OTP-" + vsn
        repo.git.reset("--hard")

        if pathlib.Path(otp_src).is_file():
            print(f"  remove old {otp_src}")
            shutil.rmtree(otp_src)
        print(f"  copy otp to {otp_src}")
        shutil.copytree(otp_git_dir, otp_src, ignore=shutil.ignore_patterns(".git*"))

        print(f"  compressing {otp_src}.tar.gz")
        with tarfile.open(full_path, "w:gz") as tar:
            tar.add(otp_src)

        print(f"  removing {otp_src} directory")
        shutil.rmtree(otp_src)

last_lines = collections.deque(maxlen=10)
max_line_len = shutil.get_terminal_size().columns

def print_last_lines(last_lines):
    print("\033[F" * len(last_lines), end="")
    for line in last_lines:
        truncated_line = line[:max_line_len]
        print(f"{truncated_line:<{max_line_len}}")

def print_clean():
    print("\n" * 10, end="")

# create deb
client = docker.from_env()
for root_vsn, vsn in last_vsn.items():
    filename = "otp-" + root_vsn + "_" + vsn + "-1_amd64.deb"
    full_path = debian_pool / filename
    if full_path.is_file():
        continue

    print(f"creating {str(full_path)}")
    container = client.containers.run(
        "erlang_bookworm",
        detach=True,
        environment=[
            "ERLANG_VSN=27.0",
            "VSN=27.0.1",
            "ERL_TOP=/usr/local/src/otp-27.0-27.0.1"
        ],
        volumes={
            os.getcwd() + "/input": {"bind": "/input", "mode": "rw"},
            os.getcwd() + "/debian/12/pool": {"bind": "/output", "mode": "rw"}
        }
    )
    stream = container.logs(stream=True)
    print_clean()
    for output in stream:
        last_lines.append(output.decode('utf8').strip())
        print_last_lines(last_lines)
    container.remove()

