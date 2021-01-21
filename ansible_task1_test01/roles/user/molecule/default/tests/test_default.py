import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_user_exist(host):
    assert host.user('serviceuser').exists
    # cmd = host.run('cat /etc/passwd')
    # assert cmd.stdout.find(u'') > -1

def test_net_services_work(host):
    sudoers = host.file('/etc/sudoers')
    assert sudoers.contains('serviceuser ALL=NOPASSWD:/bin/systemctl')