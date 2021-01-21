import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_nginx_is_running(host):
    assert host.service('nginx').is_running

def test_ssh_pub_key(host):
    nginx_avail_conf = host.file('/etc/nginx/sites-available/proxy')
    assert nginx_avail_conf.exists
    nginx_enable_conf = host.file('/etc/nginx/sites-enabled/proxy')
    assert nginx_enable_conf.exists

def test_net_services_work(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening