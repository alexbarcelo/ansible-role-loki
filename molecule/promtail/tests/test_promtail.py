import os
import pytest
import yaml
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def AnsibleDefaults():
    with open("./defaults/main.yml", 'r') as stream:
        return yaml.full_load(stream)


@pytest.mark.parametrize("dir", [
    "/opt/promtail",
    "/etc/loki",
    "/etc/loki/file_sd",
    "/var/lib/promtail",
])
def test_directories(host, dir):
    d = host.file(dir)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("files", [
    "/etc/systemd/system/promtail.service",
    "/usr/local/bin/promtail",
    "/etc/loki/promtail-config.yml"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


@pytest.mark.parametrize("files", [
    "/etc/systemd/system/loki.service",
    "/opt/loki",
    "/usr/local/bin/loki",
    "/etc/loki/loki-config.yml"
])
def test_outsider_files(host, files):
    f = host.file(files)
    assert not f.exists


def test_user(host):
    assert host.group("loki").exists
    assert host.user("loki").exists


def test_services(host):
    s = host.service("promtail")
    assert s.is_running

    s = host.service("loki")
    assert not s.is_running


def test_version(host, AnsibleDefaults):
    version = os.getenv('LOKI', AnsibleDefaults['loki_version'])
    out = host.run("/usr/local/bin/promtail --version").stdout
    assert version in out
    assert "promtail" in out
