from fabric.operations import sudo, run

from offregister_fab_utils.apt import apt_depends
from offregister_fab_utils.fs import cmd_avail


def install_docker0(*args, **kwargs):
    if cmd_avail('docker'):
        return 'Docker is already installed'

    apt_depends('apt-transport-https', 'ca-certificates', 'curl', 'gnupg-agent', 'software-properties-common')
    sudo('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -')
    sudo('apt-key fingerprint 0EBFCD88')
    distro = run('lsb_release -cs')
    sudo('add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu {distro} stable"'.format(
        distro=distro
    ))
    apt_depends('docker-ce', 'docker-ce-cli', 'containerd.io')
    sudo('systemctl enable docker')
    return 'Docker is now installed and will run at boot'


def install_docker_user1(*args, **kwargs):
    user = run('echo $USER', quiet=True)
    if run('getent group docker', warn_only=True).failed:
        sudo('groupadd docker')
    elif run('id -nG "{user}" | grep -qw docker'.format(user=user), warn_only=True, quiet=True).failed:
        sudo('usermod -aG docker {user}'.format(user=user))
    else:
        return 'Docker group already exists'

    raise NotImplementedError('You must restart machine for nonroot user to run Docker')


def test_docker2(*args, **kwargs):
    return run('docker run hello-world')


def install_docker_compose3(*args, **kwargs):
    version = '1.25.4'

    if cmd_avail('docker-compose'):
        return 'already installed'

    executable = '/usr/local/bin/docker-compose'

    sudo('curl -L https://github.com/docker/compose/releases/download/{version}/docker-compose-$(uname -s)-$(uname -m)'
         ' -o {executable}'.format(executable=executable, version=version))
    sudo('chmod +x {executable}'.format(executable=executable))
