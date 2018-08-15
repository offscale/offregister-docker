from fabric.operations import sudo, run

from offregister_fab_utils.apt import apt_depends
from offregister_fab_utils.fs import cmd_avail


def install_docker0(*args, **kwargs):
    if cmd_avail('docker'):
        return 'Docker is already installed'

    apt_depends('apt-transport-https', 'ca-certificates', 'curl', 'software-properties-common')
    sudo('curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -')
    sudo('add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"')
    apt_depends('docker-ce')
    sudo('systemctl enable docker')
    return 'Docker is now installed and will run at boot'


def install_docker_user1(*args, **kwargs):
    if run('getent group docker').succeeded:
        return 'Docker group already exists'

    sudo('groupadd docker')
    sudo('usermod -aG docker $USER')
    sudo('usermod -aG docker {user}'.format(user=run('echo $USER', quiet=True)))

    raise NotImplementedError('You must restart machine for nonroot user to run Docker')

    # return 'Docker group created'


def test_docker2(*args, **kwargs):
    return run('docker run hello-world')
