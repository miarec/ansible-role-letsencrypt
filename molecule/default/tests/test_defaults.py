import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_directories(host):

    dirs = [
        "/etc/letsencrypt",
        "/var/log/letsencrypt",
        "/var/lib/letsencrypt",
        "/opt/certbot"
    ]
    for dir in dirs:
        d = host.file(dir)
        assert d.is_directory
        assert d.exists

def test_user(host):
    assert host.user("certbot").exists, "user `certbot` should exist"

def test_certbot(host):
    assert host.run("/opt/certbot/venv/bin/certbot --version").rc ==0, "Certbot should work inside venv"


def test_files(host):
    files = [
        "/etc/cron.d/ansible_certbot_renew",
    ]

    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file
