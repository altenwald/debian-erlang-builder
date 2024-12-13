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
import getopt
import tempfile

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

debian_pool = pathlib.Path("debian/" + debian_vsn + "/pool")
debian_pool.is_dir() or sys.exit("missing " + str(debian_pool))

tag = re.compile(r"^OTP-[0-9.]+$")

def match(repo_tag):
    return tag.match(str(repo_tag))

def tr(repo_tag):
    return re.sub(r'^OTP-([0-9.]+)$', r'\1', str(repo_tag))

def create_input_tarball(root_vsn, vsn, repo, input_path):
    otp_src = f"otp_src_{root_vsn}"
    tarname = f"otp_src_{vsn}.tar.gz"
    full_path = input_path / tarname
    if full_path.is_file():
        return

    print(f"create {str(full_path)}")

    print(f"  change to tag OTP-{vsn}")
    repo.head.reference = f"OTP-{vsn}"
    repo.git.reset("--hard")

    if pathlib.Path(otp_src).is_file():
        print(f"  remove old {otp_src}")
        shutil.rmtree(otp_src)
    print(f"  copy otp to {otp_src}")
    shutil.copytree(otp_git_dir, otp_src, ignore=shutil.ignore_patterns(".git*"))

    print(f"  compressing {tarname}")
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

def header(text):
    spaces = ' ' * (max_line_len - 2 - len(text))
    print(f"\033[7m {text} {spaces}\033[27m")

def to_create(debian_vsn, root_vsn):
    if debian_vsn in ["9", "10", "11"] and root_vsn[0:2] in ["17", "18", "19", "20", "21"]:
        return False

    if debian_vsn == "12" and (root_vsn in ["24.0", "24.1"] or root_vsn[0:2] in ["17", "18", "19", "20", "21", "22", "23"]):
        return False

    return True

def create_deb(client, root_vsn, vsn, full_path, logfile):
    global codenames
    global debian_pool
    global debian_vsn

    if full_path.is_file():
        return False

    image = f"erlang_{codenames[debian_vsn]}"

    cwd = os.getcwd()
    input_temp_dir = tempfile.mkdtemp()
    shutil.copy(f"{cwd}/input/otp_src_{vsn}.tar.gz", f"{input_temp_dir}/otp_src_{root_vsn}.tar.gz")
    volumes = {
        f"{input_temp_dir}": {"bind": "/input", "mode": "rw"},
        f"{cwd}/debian/{debian_vsn}/pool": {"bind": "/output", "mode": "rw"}
    }

    if not to_create(debian_vsn, root_vsn):
        return False

    # to create is denying the creation of Debian 12 and OTP 22
    if debian_vsn == "11" and root_vsn[0:4] in ["22.0", "22.1", "22.2"]:
        image = f"{image}_gcc9"

    project_path = os.path.dirname(__file__)
    patch_dir = f"{project_path}/patches/{codenames[debian_vsn]}/{root_vsn}/patches"
    if pathlib.Path(patch_dir).is_dir():
        volumes[patch_dir] = {"bind": "/usr/local/src/debian/patches", "mode": "ro"}

    header(f"creating {str(full_path)}")
    container = client.containers.run(
        image,
        detach=True,
        environment=[
            f"ERLANG_VSN={root_vsn}",
            f"VSN={vsn}",
            f"ERL_TOP=/usr/local/src/otp-{root_vsn}-{vsn}"
        ],
        volumes=volumes
    )
    stream = container.logs(stream=True)
    print_clean()
    with open(logfile, "w") as file:
        for output in stream:
            line = output.decode('utf8')
            file.write(line)
            line = line.strip().translate(str.maketrans({chr(i): '.' for i in range(32)}))
            last_lines.append(line)
            print_last_lines(last_lines)
    container.remove()
    shutil.rmtree(input_temp_dir)
    return True

opts, args = getopt.getopt(sys.argv[1:], "hc", ["help", "check"])
for (option, value) in opts:
    if option in ["-h", "--help"]:
        print("""
        syntax: ./build_otp.py [--check|-c|--help|-h]

        help  h  show this help message
        check c  check what debian packages are missing
        """)
        sys.exit(0)

    elif option in ["-c", "--check"]:
        last_vsn = {}
        with git.Repo("otp") as repo:
            repo.remotes.origin.fetch()
            all_vsn = [tr(repo_tag) for repo_tag in repo.tags if match(repo_tag)]
            main_vsn = set(map(lambda x:x[0:4], all_vsn))
            last_vsn = dict([[(y[0:4], y) for y in all_vsn if y[0:4]==x][-1] for x in main_vsn])

        vsns = list(filter(lambda root_vsn: not (debian_pool / f"otp-{root_vsn}_{last_vsn[root_vsn]}-1_amd64.deb").is_file() and to_create(debian_vsn, root_vsn), last_vsn.keys()))
        if len(vsns) == 0:
            print("Everything done!")
        else:
            print(f"Missing ones: {vsns}")

        sys.exit(0)

last_vsn = {}
with git.Repo("otp") as repo:
    repo.remotes.origin.fetch()
    all_vsn = [tr(repo_tag) for repo_tag in repo.tags if match(repo_tag)]
    main_vsn = set(map(lambda x:x[0:4], all_vsn))
    last_vsn = dict([[(y[0:4], y) for y in all_vsn if y[0:4]==x][-1] for x in main_vsn])

    # create inputs
    input_path = pathlib.Path("input")
    for root_vsn, vsn in last_vsn.items():
        create_input_tarball(root_vsn, vsn, repo, input_path)

# create deb
client = docker.from_env()
for root_vsn, vsn in last_vsn.items():
    filename = f"otp-{root_vsn}_{vsn}-1_amd64.deb"
    deb_file = debian_pool / filename
    logfile = debian_pool / f"otp-{root_vsn}_{vsn}.log"

    if create_deb(client, root_vsn, vsn, deb_file, logfile) and not deb_file.is_file():
        print(f"\033[1;41mERROR\033[0m: you can find the log errors in {logfile}")
