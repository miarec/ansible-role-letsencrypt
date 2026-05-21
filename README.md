# ansible-role-letsencrypt
Role to generate Let's Encrypt SSL certificates

## Features

This role does the following;

1. Installs certbot in a python virtual environment
2. Generates SSL certificate for the requested domains using method `webroot` or `dns-route53`
3. Configures Apache with new SSL certificates
4. Configures cron for auto-renew


## Role Variables

### Python Virtual Environment

    certbot_python: python3

Certbot requires python3 to function, specify the python binary to use

### Email-address

    certbot_email: email@example.com

The email address used to agree to Let's Encrypt's TOS and subscribe to cert-related notifications.
This should be customized and set to an email address that you or your organization regularly monitors.

### Domain names

Option 1. Multiple domains:

    certbot_domains:
     - miarec.example.com
     - recording.example.com

Option 2. A single domain:

    certbot_domain: miarec.example.com


A domain for each SSL certificate should be generated.

### Challenge method

    certbot_method: webroot

Method used for challenging SSL certificate:

- `webroot` (default) will use a direct HTTP challenge, this is suitable only if this is the only server that will respond to this request
- `dns-route53` will use a DNS challenge configuring a record in AWS Route53 Hosted Zone, NOTE: Instance needs IAM permissions to modify Route53 records

### Cron auto-renew task

    certbot_auto_renew: true
    certbot_auto_renew_user: "{{ ansible_user | default(lookup('env', 'USER')) }}"
    certbot_auto_renew_hour: "3"
    certbot_auto_renew_minute: "30"
    certbot_auto_renew_options: "--quiet --no-self-upgrade"

By default, this role configures a cron job to run under the provided user account at the given hour and minute, every day.
The defaults run `certbot renew` (or `certbot-auto renew`) via cron every day at 03:30:00 by the user you use in your Ansible playbook.
It's preferred that you set a custom user/hour/minute so the renewal is during a low-traffic period and done by a non-root user account.


### Configure Apache

Create Virtual Host SSL configuration for each domain (enabled by default):

    certbot_configure_apache: true

If SSL certificates are not used in Apache, then set `certbot_configure_apache` to `false`

## Dependencies

- Python
- Apache, if using `webroot` challenge method.
- IAM role with permissions to create TXT records for the managed domains in Route53 service, if using `dns-route53` challenge method


## Example Playbook

    - hosts: web

      vars:
        certbot_email: admin@example.com
        certbot_domains:
         - miarec.example.com
         - recording.example.com
        certbot_method: dns-route53
        certbot_auto_renew_minute: "20"
        certbot_auto_renew_hour: "5"

      roles:
        - ansible-role-letsencrypt

## Testing

This role uses [Molecule](https://molecule.readthedocs.io/) with Docker for testing.
[uv](https://docs.astral.sh/uv/) is used for dependency management.

### Prerequisites

- Docker
- uv (install via `curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Running Tests

```bash
# Run full test suite
uv run molecule test

# Test against specific distro
MOLECULE_DISTRO=ubuntu2404 uv run molecule test
MOLECULE_DISTRO=rockylinux9 uv run molecule test
```

### Available Distros

| Distribution   | Variable Value  |
|----------------|-----------------|
| Ubuntu 22.04   | `ubuntu2204`    |
| Ubuntu 24.04   | `ubuntu2404`    |
| Rocky Linux 9  | `rockylinux9`   |
| RHEL 9         | `rhel9`         |

### Linting

```bash
uv run ansible-lint
```
