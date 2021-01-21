import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_ssh_is_running(host):
    assert host.service('sshd').is_running

def test_ssh_config(host):
    ssh_conf = host.file('/etc/ssh/sshd_config')
    assert ssh_conf.exists
    assert ssh_conf.contains('PermitRootLogin no')
    assert ssh_conf.contains('Port 22')


def test_ssh_services_work(host):
    assert host.socket("tcp://0.0.0.0:22").is_listening