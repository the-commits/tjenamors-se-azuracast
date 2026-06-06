# AzuraCast

Ansible role for deploying [AzuraCast](https://www.azuracast.com) via Docker on Linux servers.

## Requirements

### Server Requirements

#### Minimum
- 64-bit x86 (x86_64/amd64) or ARM64 CPU
- at least 2 GB of RAM
- 20 GB or greater of hard drive space
- Docker Engine and Docker Compose installed

#### Recommended
- 4 CPU cores
- 4 GB of RAM
- 40 GB or greater of hard drive space
- Docker Engine and Docker Compose installed

Recommended specs allow running 5–10 stations with ease (hobby usage). If you
wish to increase memory further, adding [swap space](https://linuxize.com/post/how-to-add-swap-space-on-ubuntu-22-04/)
should be the norm.

#### Hard Limits
- 5 CPU cores
- 5 GB of RAM
- 50 GB of hard drive space

Hard limits are 1.25× recommended. Our setup runs 1 station with ~100 average
listeners within recommended specs.

### Ansible Requirements
- Ansible 2.14+
- Root/sudo access on target hosts

## Installation

### From Ansible Galaxy (once published)

```bash
ansible-galaxy install tjenamors.azuracast
```

### From source

Add to your `requirements.yml`:

```yaml
---
roles:
  - name: azuracast
    src: git@git.sr.ht:~the-commits/tjenamors-se-azuracast
    scm: git
    version: main
```

Then install:

```bash
ansible-galaxy install -r requirements.yml -p roles/
```

## Role Variables

All variables are prefixed with `azuracast_`. See [`defaults/main.yml`](defaults/main.yml) for the full list.

| Variable | Default | Description |
|---|---|---|
| `azuracast_base_dir` | `/var/azuracast` | AzuraCast installation directory |
| `azuracast_release_channel` | `latest` | Release channel (`latest` or `stable`) |
| `azuracast_http_port` | `80` | HTTP port |
| `azuracast_https_port` | `443` | HTTPS port |
| `azuracast_sftp_port` | `2022` | SFTP port |
| `azuracast_puid` | `1000` | User ID for container processes |
| `azuracast_pgid` | `1000` | Group ID for container processes |
| `azuracast_auto_assign_port_min` | `8000` | Minimum station port |
| `azuracast_auto_assign_port_max` | `8499` | Maximum station port |
| `azuracast_memory_max` | `2048m` | Hard memory limit for web container |
| `azuracast_memory_reservation` | `1024m` | Soft memory reservation |
| `azuracast_cpus_max` | `2` | Hard CPU limit |
| `azuracast_cpus_reservation` | `1` | Soft CPU reservation |
| `azuracast_mysql_password` | `azur4c457` | MySQL password (change in production!) |
| `azuracast_enable_redis` | `true` | Enable Redis cache |
| `azuracast_service_enabled` | `true` | Start azuracast.service on boot |
| `azuracast_service_state` | `started` | Desired service state |
| `azuracast_shutdown_timeout` | `60` | Seconds to wait for graceful shutdown |

## Dependencies

Requires Docker Engine and Docker Compose to be installed on target hosts. See
[`tjenamors-se-docker`](https://git.sr.ht/~the-commits/tjenamors-se-docker) and
[`tjenamors-se-docker-compose`](https://git.sr.ht/~the-commits/tjenamors-se-docker-compose).

## Example Playbook

```yaml
- hosts: all
  become: true
  vars:
    azuracast_http_port: 8080
    azuracast_release_channel: stable
  roles:
    - role: docker
    - role: docker_compose
    - role: azuracast
```

## Local Development

### Prerequisites

```bash
pip install molecule molecule-plugins[vagrant]
vagrant plugin install vagrant-libvirt
```

### Running Tests

```bash
molecule test
```

### Project Layout

```
.
├── defaults/        # Default variable values
├── handlers/        # Ansible handlers
├── meta/            # Galaxy metadata + supported platforms
├── tasks/           # Main role tasks
├── templates/       # Jinja2 templates (.env, azuracast.env, docker-compose.yml)
├── vars/            # OS-specific variables
├── galaxy.yml       # Galaxy metadata (for publishing)
├── README.md
└── CHANGELOG.md
```

## How It Works

1. Creates the AzuraCast directory (`/var/azuracast` by default)
3. Deploys `.env`, `azuracast.env`, and `docker-compose.yml` from Jinja2 templates
4. Pulls the AzuraCast Docker images
5. Deploys a systemd service (`azuracast.service`) on systemd-based distros and starts it with `systemctl enable --now`
6. Falls back to direct `docker compose up -d` on non-systemd systems
7. Runs `azuracast_install` on first deployment

## Service Management (systemd)

On systemd-based distros (Ubuntu, Debian, RHEL, etc.), manage AzuraCast like any other system service:

```bash
sudo systemctl status azuracast
sudo systemctl start azuracast
sudo systemctl stop azuracast
sudo systemctl restart azuracast
sudo journalctl -u azuracast
```

## Contributing

1. Fork the repository on [sourcehut](https://git.sr.ht/~the-commits/tjenamors-se-azuracast)
2. Create a feature branch
3. Make your changes
4. Run `molecule test` to verify
5. Send a patch via email to `~the-commits/tjenamors-se-azuracast@lists.sr.ht`

## License

AGPL-3.0 — see [LICENSE](LICENSE) for details.
