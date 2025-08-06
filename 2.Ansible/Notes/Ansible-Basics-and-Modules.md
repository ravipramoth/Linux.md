# Ansible Basics and Modules

## What is Ansible? Features

Ansible --> Automation -- Confgiuration management / Application deployemnt

What is configuation mangmnet ?
- Install package
- install programming langauge
- install build topols
- install Application runtione
- Creation users /groups/ folders
- Creation of systemctl service ..   /etc/systemd-- > Promotheus & grafana

features
- Platfrom independent
- scalbale
- Erro handling
- Readbale  and maintable
- reusable
- vault
- Rich modules
- agnet less
- Push based Arch

Ansible will use ssh connection to connect manged nodes
Ansible will YAML  ---  > yet another markup langauge

PUSH VS PULL
PULL
- internet Traffic Incresase
- Slowness in your application
- Cost ---  Data transfer cost
PUSH --
- untill there is change it wont work

## Adhoc Commands & Playbooks

To Run Ansible Commands You have 2 options
- Adhoc Commands -- Command # frem -m,
  ansible -i < inventory file > all -m <mdoule name > -a [arguments]
- To install s/w
  ansible -i <inventoryfile> -m ansible.builtin.{package/yum/dnf/ap} -a " name=s/w package state=  Present/absent/enabled/latest " --become

ansible -i list -m all ansible.builtin.package -a "name =${1} state=present" -b
ansible -i list all -m ansible.builtin.package -a "name=${1} state=present" -b

Playbook Example:

- name: install nginx s/w
  hosts: PROD
  become: yes
  tasks:
    - name: install nginx
      ansible.builtin.package:
          name: nginx
          state: present
    - name: start nginx service
      ansible.builtin.systemd:
          name: nginx
          state: started
          enabled: true

## Inventory Structure

all:
  children:
    PROD:
      hosts:
        44.198.96.123:
    DEV:
      hosts:
        52.72.157.134:
    Webserver:
        hosts:
            44.198.96.123
            10.56.256.243

## Module Usage (command, shell, file)

### 1. ansible.builtin.command
Executes a command on a remote machine.
- Runs a specified command on the target machine. It does not process the command through a shell, so no shell features like piping, redirection, or variable substitution are available.
- Examples:
  - ansible all -m ansible.builtin.command -a "ls /home/" -b
  - ansible all -m ansible.builtin.command -a "ls -l /var/log" -b
  - ansible all -m ansible.builtin.command -a "mkdir -p /tmp/demo-dir" -b

### 2. ansible.builtin.shell
Executes a shell command on the remote machine.
- Runs a shell command on the target machine, and allows you to use shell features like pipes, redirects, and variable substitution.
- Examples:
  - ansible all -m ansible.builtin.shell -a "echo 'Hello, World!' > /opt/hello.txt" -b
  - ansible all -m ansible.builtin.shell -a "cat /home/ansadmin/test/test.txt | wc -l" -b

### Difference between `shell` and `command`

| Feature                   | `command`         | `shell`           |
| ------------------------- | ----------------- | ----------------- |
| Uses shell                | ❌ No              | ✅ Yes             |
| Supports pipes (`|`)      | ❌ No              | ✅ Yes             |
| Supports redirects (`>`)  | ❌ No              | ✅ Yes             |
| Safe from shell injection | ✅ Yes             | ❌ No              |
| Performance               | ✅ Slightly faster | ❌ Slightly slower |
| Example                   | `ls -l /etc`      | `ls -l /etc | grep conf` |

### 3. ansible.builtin.file
Create/Modify file attributes like permissions, owner, and group. It can create/delete directories or files.
