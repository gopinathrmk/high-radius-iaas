#cloud-config
disable_root: False

hostname: @@{vm_name}@@
fqdn: @@{vm_name}@@.@@{domain_name}@@

users:
  - default
  - name: @@{linux.username}@@
    ssh-authorized-keys:
      - @@{linux.public_key}@@
    sudo: ['ALL=(ALL) NOPASSWD:ALL']

runcmd:
  - [systemctl, mask, cloud-init-local, cloud-init, cloud-config, cloud-final]
  - [eject]