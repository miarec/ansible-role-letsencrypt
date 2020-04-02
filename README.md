# ansible-role-letsencrypt
Role to generate Let's Encrypt SSL certificates

## Features

This role does the following 

1. Installs certbot 
2. Generates SSL certificate for the requested domain using webroot method
3. Configures Apache with new SSL certificates
4. Configures cron for auto-renew


## Role Variables

### Email-address

    certbot_admin_email: email@example.com

The email address used to agree to Let's Encrypt's TOS and subscribe to cert-related notifications. 
This should be customized and set to an email address that you or your organization regularly monitors.

### Domain name

    certbot_domain: www.example.com
    
A domain for which the SSL certificate should be generated.

### Cron auto-renew task

    certbot_auto_renew: true
    certbot_auto_renew_user: "{{ ansible_user | default(lookup('env', 'USER')) }}"
    certbot_auto_renew_hour: "3"
    certbot_auto_renew_minute: "30"
    certbot_auto_renew_options: "--quiet --no-self-upgrade"

By default, this role configures a cron job to run under the provided user account at the given hour and minute, every day. 
The defaults run `certbot renew` (or `certbot-auto renew`) via cron every day at 03:30:00 by the user you use in your Ansible playbook. 
It's preferred that you set a custom user/hour/minute so the renewal is during a low-traffic period and done by a non-root user account.

### Create SSL certificate command

    certbot_create_command: "{{ certbot_script }} certonly --webroot -w /var/www/html/ --noninteractive --agree-tos --email {{ certbot_admin_emai) }} -d {{ cert_domain }}"

The `certbot_create_command` defines the command used to generate the cert.


## Dependencies

None.

## Example Playbook

    - hosts: web
    
      vars:
        certbot_admin_email: admin@example.com
        certbot_domain: www.example.com
        certbot_auto_renew_minute: "20"
        certbot_auto_renew_hour: "5"
    
      roles:
        - ansible-role-letsencrypt
