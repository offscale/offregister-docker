from __future__ import print_function
from functools import partial

from os import path
from sys import modules, version
from pkg_resources import resource_filename

if version[0] == "2":
    from itertools import imap as map

from fabric.contrib.files import append
from fabric.operations import sudo

from offregister_fab_utils.fs import cmd_avail


def install_docker0(*args, **kwargs):
    if cmd_avail("docker"):
        return

    kernel_version = sudo("uname -r", quiet=True)
    if tuple(map(int, kernel_version[: kernel_version.find(".", 2)].split("."))) < (
        3,
        10,
    ):
        raise NotImplementedError("Docker for older versions of the Linux kernel")

    for mnt in sudo('mount | grep "^/dev"'):
        if "xfs" not in mnt and len(mnt) > 1:
            print("mnt =", mnt)
            dev = mnt[: mnt.find(" on")]
            print("dev =", dev)
            sudo("mkfs -t xfs -n ftype=1 {dev}".format(dev=dev))

    if sudo("lsmod | grep overlay", warn_only=True).failed:
        append("/etc/modules-load.d/overlay.conf", "overlay", use_sudo=True)
        sudo("reboot")
        return "rebooting: RERUN"

    centos_join = partial(
        path.join,
        path.join(
            path.dirname(
                resource_filename(modules[__name__].__package__, "__init__.py")
            ),
            "_centos",
        ),
    )
    with open(centos_join("docker.yum")) as f:
        append("/etc/yum.repos.d/docker.repo", f.read(), use_sudo=True)

    with open(centos_join("override.conf")) as f:
        p = "/etc/systemd/system/docker.service.d"
        sudo("mkdir -p {p}".format(p=p))
        append("{p}/override.conf".format(p=p), f.read(), use_sudo=True)
    sudo("yum install -y docker-engine-1.13.1 docker-engine-selinux-1.13.1")
    sudo("systemctl start docker")
    sudo("systemctl enable docker")

    return sudo("docker ps")
