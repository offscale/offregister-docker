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
