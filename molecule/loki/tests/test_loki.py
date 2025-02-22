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
    "/opt/loki",
    "/etc/loki"
])
def test_directories(host, dir):
    d = host.file(dir)
    assert d.is_directory
    assert d.exists


@pytest.mark.parametrize("files", [
    "/etc/systemd/system/loki.service",
    "/usr/local/bin/loki",
    "/etc/loki/loki-config.yml"
])
def test_files(host, files):
    f = host.file(files)
    assert f.exists
    assert f.is_file


@pytest.mark.parametrize("files", [
    "/var/lib/promtail",
    "/opt/promtail",
    "/etc/systemd/system/promtail.service",
    "/usr/local/bin/promtail",
    "/etc/loki/promtail-config.yml"
    "/etc/loki/file_sd",
])
def test_outsider_files(host, files):
    f = host.file(files)
    assert not f.exists


def test_sockets(host):
    # Loki GRPC
    s = host.socket("tcp://0.0.0.0:9095")
    assert s.is_listening

    # Loki HTTP
    s = host.socket("tcp://0.0.0.0:3100")
    assert s.is_listening

    # Promtail HTTP, which should not be running
    s = host.socket("tcp://0.0.0.0:9080")
    assert not s.is_listening


def test_user(host):
    assert host.group("loki").exists
    assert host.user("loki").exists


def test_services(host):
    s = host.service("promtail")
    assert not s.is_running

    s = host.service("loki")
    assert s.is_running


def test_version(host, AnsibleDefaults):
    version = os.getenv('LOKI', AnsibleDefaults['loki_version'])
    out = host.run("/usr/local/bin/loki --version").stdout
    assert version in out
    assert "loki" in out
