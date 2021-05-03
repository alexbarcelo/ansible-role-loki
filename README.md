# Ansible Role: promtail

[![Test](https://github.com/alexbarcelo/ansible-role-loki/workflows/Test/badge.svg)](https://github.com/alexbarcelo/ansible-role-loki/actions?query=workflow%3ATest+branch%3Amaster)
[![License](https://img.shields.io/badge/license-MIT%20License-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Ansible Role](https://img.shields.io/badge/ansible%20role-alexbarcelo.loki-blue.svg)](https://galaxy.ansible.com/alexbarcelo/loki/)
[![GitHub tag](https://img.shields.io/github/tag/alexbarcelo/ansible-role-loki.svg)](https://github.com/alexbarcelo/ansible-role-loki/tags)

## Description

Deploy [promtail](https://github.com/grafana/loki) using ansible. Supports amd64 and arm architectures.
For recent changes, please check the [CHANGELOG](/CHANGELOG.md) or have a look at [github releases](https://github.com/patrickjahns/ansible-role-promtail/releases)


## Requirements

- Ansible >= 2.7 

## Role Variables

All variables which can be overridden are stored in [defaults/main.yml](defaults/main.yml) file as well as in table below.

ToDo

For each section (`promtail_config_clients`, `promtail_config_server`,`promtail_config_positions`,`promtail_config_scrape_configs`,`promtail_target_config`) the configuration can be passed accrodingly to the [official promtail configuration](https://github.com/grafana/loki/blob/master/docs/clients/promtail/configuration.md).
The role will converte the ansible vars into the respective yaml configuration for loki.

## Example Playbook

Basic playbook that will assume that loki will be listening at `http://127.0.0.1:3100` and a simple configuration to scrape `/var/log` logs:

```yaml
---
- hosts: all
  roles:
    - role: patrickjahns.promtail
      vars: 
        promtail_config_scrape_configs:
          - job_name: system
            static_configs:
            - targets:
                - localhost
              labels:
                job: varlogs
                __path__: /var/log/*log
```

A more complex example, that overrides server, client, positions configuration and provides a scrap configuration for `/var/log`:

```yaml
---
- hosts: all
  roles:
    - role: patrickjahns.promtail
      vars: 
        promtail_config_server:
          http_listen_port: 9080
          grpc_listen_port: 9081
        promtail_config_clients:
          - url: "http://prometheus.domain.tld:3100/loki/api/v1/push"
            external_labels:
              host: "{{ ansible_hostname }}"
        promtail_config_positions:
          filename: "{{ promtail_positions_directory }}/positions.yaml"
          sync_period: "60s"

        promtail_config_scrape_configs:
          - job_name: system
            static_configs:
            - targets:
                - localhost
              labels:
                job: varlogs
                __path__: /var/log/*log
```

## Local Testing

The preferred way of locally testing the role is to use Docker and [molecule](https://github.com/metacloud/molecule) (v3.x). You will have to install Docker on your system. See "Get started" for a Docker package suitable to for your system.
We are using tox to simplify process of testing on multiple ansible versions. To install tox execute:
```sh
pip3 install tox
```
To run tests on all ansible versions (WARNING: this can take some time)
```sh
tox
```
To run a custom molecule command on custom environment with only default test scenario:
```sh
tox -e ansible29 -- molecule test -s default
```
For more information about molecule go to their [docs](http://molecule.readthedocs.io/en/latest/).

If you would like to run tests on remote docker host just specify `DOCKER_HOST` variable before running tox tests.

## CI

Github actions is used to test and validate this ansible role via [ansible-later](https://github.com/thegeeklab/ansible-later) and [molecule](https://github.com/ansible-community/molecule).
Molecule tests will run with several operation systems as well as ansible version in order to ensure compatability.

## License

This project is licensed under MIT License. See [LICENSE](/LICENSE) for more details.

## Credits

This role is based on the [ansible promtail role](https://github.com/patrickjahns/ansible-role-promtail) done by [Patrick Jahns](https://github.com/patrickjahns).

[Alex Barcelo](https://github.com/alexbarcelo) forked that and modified it in order to achieve a loki **and** promtail installation role.
