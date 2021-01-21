import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_LANGUAGE(host):
    cmd = host.run('locale')
    assert cmd.stdout.find(u'LANGUAGE=C.UTF-8') > -1

def test_ssh_LC_ALL(host):
    cmd = host.run('locale')
    assert cmd.stdout.find(u'LC_ALL=C.UTF-8') > -1


