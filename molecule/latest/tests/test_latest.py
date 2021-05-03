import os
import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_user(host):
    assert host.group("loki").exists
    assert host.user("loki").exists


def test_service(host):
    s = host.service("promtail")
    assert s.is_running

    s = host.service("loki")
    assert s.is_running


def test_sockets(host):
    # Loki GRPC
    s = host.socket("tcp://0.0.0.0:9095")
    assert s.is_listening

    # Loki HTTP
    s = host.socket("tcp://0.0.0.0:3100")
    assert s.is_listening

    # Promtail GRPC is random, and not extremely relevant

    # Promtail HTTP
    s = host.socket("tcp://0.0.0.0:9080")
    assert s.is_listening


def test_version(host):
    res = host.run("/usr/local/bin/promtail --version")
    assert res.rc == 0
    assert "promtail" in res.stdout

    res = host.run("/usr/local/bin/loki --version")
    assert res.rc == 0
    assert "loki" in res.stdout
