import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_monit_is_running(host):
    assert host.service('monit').is_running

def test_monit_conf(host):
    monit_conf = host.file('/etc/monit/monitrc')
    assert monit_conf.exists
    assert monit_conf.contains('set httpd port 2812') 


def test_monit_services_work(host):
    assert host.socket("tcp://127.0.0.1:2812").is_listening