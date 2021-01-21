import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_timezone(host):
    cmd = host.run('timedatectl')
    assert cmd.stdout.find(u'Europe/Moscow') > -1

