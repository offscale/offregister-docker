# -*- coding: utf-8 -*-
from offregister_fab_utils.apt import apt_depends
from offregister_fab_utils.fs import cmd_avail


def install_docker0(c, *args, **kwargs):
    if cmd_avail(c, "docker"):
        return "Docker is already installed"

    apt_depends(
        c,
        "apt-transport-https",
        "ca-certificates",
        "curl",
        "gnupg-agent",
        "software-properties-common",
    )
    c.sudo(
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -"
    )
    c.sudo("apt-key fingerprint 0EBFCD88")
    distro = c.run("lsb_release -cs").stdout
    c.sudo(
        'add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu {distro} stable"'.format(
            distro=distro
        )
    )
    apt_depends(c, "docker-ce", "docker-ce-cli", "containerd.io")
    c.sudo("systemctl enable docker")
    return "Docker is now installed and will run at boot"


def install_docker_user1(c, *args, **kwargs):
    user = c.run("echo $USER", hide=True).stdout.rstrip()
    if c.run("getent group docker", warn=True).exited != 0:
        c.sudo("groupadd docker")
    elif (
        c.run(
            'id -nG "{user}" | grep -qw docker'.format(user=user),
            warn=True,
            hide=True,
        ).exited
        != 0
    ):
        c.sudo("usermod -aG docker {user}".format(user=user))
    else:
        return "Docker group already exists"

    raise NotImplementedError("You must restart machine for nonroot user to run Docker")


def test_docker2(c, *args, **kwargs):
    return c.run("docker run hello-world")


def install_docker_compose3(c, *args, **kwargs):
    version = "1.27.3"

    if cmd_avail(c, "docker-compose"):
        return "already installed"

    executable = "/usr/local/bin/docker-compose"

    c.sudo(
        "curl -L https://github.com/docker/compose/releases/download/{version}/docker-compose-$(uname -s)-$(uname -m)"
        " -o {executable}".format(executable=executable, version=version)
    )
    c.sudo("chmod +x {executable}".format(executable=executable))
