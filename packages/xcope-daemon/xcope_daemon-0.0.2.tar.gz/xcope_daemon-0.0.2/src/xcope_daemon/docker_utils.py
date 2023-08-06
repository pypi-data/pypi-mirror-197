from pathlib import Path


def is_docker():
    cgroup = Path("/proc/self/cgroup")
    return Path('/.dockerenv').is_file() or cgroup.is_file() and cgroup.read_text().find("docker") > -1
