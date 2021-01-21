import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_ufw_is_running(host):
    assert host.service('ufw').is_running

def test_ufw_ssh_rules(host):
    cmd = host.run("ufw status | grep 22 | awk '{print $2}' | head -1")
    assert cmd.stdout.find(u'ALLOW') > -1

def test_ufw_http_rules(host):
    cmd = host.run("ufw status | grep 80 | awk '{print $2}' | head -1")
    assert cmd.stdout.find(u'ALLOW') > -1

def test_ufw_default_rules(host):
    cmd = host.run("ufw status verbose | grep Default")
    assert cmd.stdout.find(u'Default: deny (incoming), allow (outgoing), deny (routed)') > -1
