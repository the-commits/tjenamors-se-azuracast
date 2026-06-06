# AzuraCast

Ansible role for deploying [AzuraCast](https://www.azuracast.com) via Docker on Linux servers.

## Requirements

- Ansible 2.14+
- Root/sudo access on target hosts
- Linux (x86_64 or aarch64)

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
| `azuracast_mysql_password` | `azur4c457` | MySQL password (change in production!) |
| `azuracast_enable_redis` | `true` | Enable Redis cache |

## Dependencies

None. Docker is installed automatically by the role using the official `get.docker.com` script.

## Example Playbook

```yaml
- hosts: all
  become: true
  vars:
    azuracast_http_port: 8080
    azuracast_release_channel: stable
  roles:
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

1. Installs Docker and Docker Compose via the official `get.docker.com` script
2. Creates the AzuraCast directory (`/var/azuracast` by default)
3. Deployes `.env`, `azuracast.env`, and `docker-compose.yml` from Jinja2 templates
4. Pulls the AzuraCast Docker images
5. Starts the containers
6. Runs `azuracast_install` on first deployment

## Contributing

1. Fork the repository on [sourcehut](https://git.sr.ht/~the-commits/tjenamors-se-azuracast)
2. Create a feature branch
3. Make your changes
4. Run `molecule test` to verify
5. Send a patch via email to `~the-commits/tjenamors-se-azuracast@lists.sr.ht`

## License

AGPL-3.0 — see [LICENSE](LICENSE) for details.
