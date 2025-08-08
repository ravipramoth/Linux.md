# Ansible Detailed Examples and Use Cases

This file contains comprehensive examples based on the interview questions and concepts from Notes.txt.

## Table of Contents
1. [Basic Playbook Structure](#basic-playbook-structure)
2. [Variable Priority Examples](#variable-priority-examples)
3. [Conditional Execution (OS-specific)](#conditional-execution-os-specific)
4. [Error Handling Examples](#error-handling-examples)
5. [Tags Usage Examples](#tags-usage-examples)
6. [Handlers and Notifications](#handlers-and-notifications)
7. [Loops and Iterations](#loops-and-iterations)
8. [Vault and Security](#vault-and-security)
9. [Wait and Retry Examples](#wait-and-retry-examples)
10. [Block, Rescue, Always](#block-rescue-always)
11. [Serial, Throttle, and Forks](#serial-throttle-and-forks)
12. [Callback Plugins Configuration](#callback-plugins-configuration)

---

## Basic Playbook Structure

### Example 1: Simple Software Installation Playbook
```yaml
---
- name: Install and configure web server
  hosts: webservers
  become: true
  gather_facts: true
  
  vars:
    web_package: nginx
    web_service: nginx
    config_file: /etc/nginx/nginx.conf
    
  tasks:
    - name: Install web server package
      ansible.builtin.package:
        name: "{{ web_package }}"
        state: present
        
    - name: Start and enable web service
      ansible.builtin.service:
        name: "{{ web_service }}"
        state: started
        enabled: true
        
    - name: Copy configuration file
      ansible.builtin.copy:
        src: nginx.conf
        dest: "{{ config_file }}"
        backup: true
      notify: restart nginx
      
  handlers:
    - name: restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
```

---

## Variable Priority Examples

### Example 2: Understanding Variable Precedence
```yaml
---
- name: Variable priority demonstration
  hosts: localhost
  gather_facts: false
  
  vars:
    priority_level: "playbook_vars"
    environment: "development"
    
  vars_files:
    - vars/common.yml
    
  tasks:
    - name: Show variable from playbook vars
      ansible.builtin.debug:
        msg: "Priority level is: {{ priority_level }}"
        
    - name: Set fact variable (higher priority)
      ansible.builtin.set_fact:
        priority_level: "set_fact_vars"
        
    - name: Show updated variable
      ansible.builtin.debug:
        msg: "Updated priority level: {{ priority_level }}"
        
    - name: Show environment variable
      ansible.builtin.debug:
        msg: "Environment: {{ environment }}"

# Run with: ansible-playbook playbook.yml -e "priority_level=command_line_vars"
# Command line vars have highest priority
```

### vars/common.yml
```yaml
---
environment: "production"
database_host: "db.example.com"
app_version: "1.2.3"
```

---

## Conditional Execution (OS-specific)

### Example 3: OS-specific Package Installation
```yaml
---
- name: Install packages based on OS family
  hosts: all
  become: true
  gather_facts: true
  
  tasks:
    - name: Install nginx on Debian/Ubuntu systems
      ansible.builtin.apt:
        name: nginx
        state: present
        update_cache: true
      when: ansible_facts['os_family'] == "Debian"
      tags:
        - nginx
        - debian
        
    - name: Install nginx on RedHat/CentOS systems
      ansible.builtin.yum:
        name: nginx
        state: present
      when: ansible_facts['os_family'] == "RedHat"
      tags:
        - nginx
        - redhat
        
    - name: Install nginx on SUSE systems
      ansible.builtin.zypper:
        name: nginx
        state: present
      when: ansible_facts['os_family'] == "Suse"
      tags:
        - nginx
        - suse
        
    - name: Display OS information
      ansible.builtin.debug:
        msg: |
          OS Family: {{ ansible_facts['os_family'] }}
          Distribution: {{ ansible_facts['distribution'] }}
          Version: {{ ansible_facts['distribution_version'] }}
```

---

## Error Handling Examples

### Example 4: Comprehensive Error Handling
```yaml
---
- name: Error handling demonstration
  hosts: webservers
  become: true
  gather_facts: false
  
  tasks:
    - name: Try to install a package that might fail
      ansible.builtin.package:
        name: nonexistent-package
        state: present
      ignore_errors: true
      register: package_result
      
    - name: Handle the error gracefully
      ansible.builtin.debug:
        msg: "Package installation failed, but continuing..."
      when: package_result.failed
      
    - name: Install fallback package
      ansible.builtin.package:
        name: curl
        state: present
      when: package_result.failed
      
    - name: Fail if critical condition is not met
      ansible.builtin.fail:
        msg: "Critical service is not running!"
      when: 
        - ansible_facts['services']['sshd'] is defined
        - ansible_facts['services']['sshd']['state'] != "running"
      ignore_errors: false
```

---

## Tags Usage Examples

### Example 5: Strategic Tag Usage
```yaml
---
- name: Multi-environment deployment with tags
  hosts: all
  become: true
  
  tasks:
    - name: Install base packages
      ansible.builtin.package:
        name: "{{ item }}"
        state: present
      loop:
        - git
        - curl
        - wget
      tags:
        - base
        - always
        
    - name: Install development tools
      ansible.builtin.package:
        name: "{{ item }}"
        state: present
      loop:
        - gcc
        - make
        - nodejs
      tags:
        - development
        - dev-tools
        
    - name: Install production monitoring
      ansible.builtin.package:
        name: "{{ item }}"
        state: present
      loop:
        - htop
        - iotop
        - netstat-nat
      tags:
        - production
        - monitoring
        
    - name: Configure firewall for production
      ansible.builtin.service:
        name: firewalld
        state: started
        enabled: true
      tags:
        - production
        - security
        - never

# Usage examples:
# ansible-playbook site.yml --tags "base"
# ansible-playbook site.yml --tags "development"
# ansible-playbook site.yml --tags "production" --skip-tags "never"
```

---

## Handlers and Notifications

### Example 6: Advanced Handler Usage
```yaml
---
- name: Web server configuration with handlers
  hosts: webservers
  become: true
  
  vars:
    nginx_config_dir: /etc/nginx
    nginx_sites_dir: /etc/nginx/sites-available
    
  tasks:
    - name: Install nginx
      ansible.builtin.package:
        name: nginx
        state: present
        
    - name: Copy main nginx configuration
      ansible.builtin.template:
        src: nginx.conf.j2
        dest: "{{ nginx_config_dir }}/nginx.conf"
        backup: true
      notify:
        - validate nginx config
        - restart nginx
        
    - name: Copy site configuration
      ansible.builtin.template:
        src: site.conf.j2
        dest: "{{ nginx_sites_dir }}/mysite"
      notify:
        - validate nginx config
        - reload nginx
        
    - name: Enable site
      ansible.builtin.file:
        src: "{{ nginx_sites_dir }}/mysite"
        dest: /etc/nginx/sites-enabled/mysite
        state: link
      notify: reload nginx
      
  handlers:
    - name: validate nginx config
      ansible.builtin.command: nginx -t
      listen: "validate nginx config"
      
    - name: restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
      listen: "restart nginx"
      
    - name: reload nginx
      ansible.builtin.service:
        name: nginx
        state: reloaded
      listen: "reload nginx"
```

---

## Loops and Iterations

### Example 7: Different Loop Types
```yaml
---
- name: Loop examples demonstration
  hosts: localhost
  gather_facts: false
  
  vars:
    users:
      - name: alice
        group: admin
        shell: /bin/bash
      - name: bob
        group: users
        shell: /bin/zsh
      - name: charlie
        group: developers
        shell: /bin/bash
        
    packages:
      centos:
        - httpd
        - mod_ssl
      ubuntu:
        - apache2
        - apache2-utils
        
  tasks:
    - name: Simple loop with list
      ansible.builtin.debug:
        msg: "Processing package: {{ item }}"
      loop:
        - git
        - curl
        - wget
        
    - name: Loop with dictionary (users)
      ansible.builtin.debug:
        msg: "User {{ item.name }} uses {{ item.shell }} and belongs to {{ item.group }}"
      loop: "{{ users }}"
      
    - name: Loop with dictionary using dict2items
      ansible.builtin.debug:
        msg: "For {{ item.key }}: {{ item.value }}"
      loop: "{{ packages | dict2items }}"
      
    - name: Nested loop example
      ansible.builtin.debug:
        msg: "OS: {{ item.0 }}, Package: {{ item.1 }}"
      loop: "{{ packages | dict2items | subelements('value') }}"
      
    - name: Loop with conditional
      ansible.builtin.debug:
        msg: "Admin user found: {{ item.name }}"
      loop: "{{ users }}"
      when: item.group == "admin"
      
    - name: Loop with index
      ansible.builtin.debug:
        msg: "Item {{ ansible_loop.index }}: {{ item }}"
      loop:
        - first
        - second
        - third
      loop_control:
        extended: true
```

---

## Vault and Security

### Example 8: Ansible Vault Usage
```yaml
---
- name: Secure deployment with vault
  hosts: databases
  become: true
  gather_facts: false
  
  vars:
    db_config_file: /etc/mysql/mysql.conf.d/mysqld.cnf
    
  vars_files:
    - vault/secrets.yml  # encrypted file
    
  tasks:
    - name: Install MySQL
      ansible.builtin.package:
        name: mysql-server
        state: present
        
    - name: Configure MySQL with secure password
      ansible.builtin.template:
        src: mysql.cnf.j2
        dest: "{{ db_config_file }}"
        mode: '0600'
        owner: mysql
        group: mysql
      notify: restart mysql
      no_log: true  # Don't log sensitive data
      
    - name: Create database user
      ansible.builtin.mysql_user:
        name: "{{ vault_db_username }}"
        password: "{{ vault_db_password }}"
        host: localhost
        priv: "myapp.*:ALL"
        state: present
      no_log: true
      
  handlers:
    - name: restart mysql
      ansible.builtin.service:
        name: mysql
        state: restarted

# vault/secrets.yml (encrypted)
# Create with: ansible-vault create vault/secrets.yml
# Edit with: ansible-vault edit vault/secrets.yml
# vault_db_username: myapp_user
# vault_db_password: super_secure_password_123
# vault_api_key: abc123def456ghi789

# Run with: ansible-playbook playbook.yml --ask-vault-pass
```

---

## Wait and Retry Examples

### Example 9: Comprehensive Wait and Retry
```yaml
---
- name: Service deployment with wait conditions
  hosts: webservers
  become: true
  
  tasks:
    - name: Install application
      ansible.builtin.package:
        name: myapp
        state: present
        
    - name: Start application service
      ansible.builtin.service:
        name: myapp
        state: started
        
    - name: Wait for application port to be ready
      ansible.builtin.wait_for:
        port: 8080
        host: localhost
        delay: 10
        timeout: 300
        msg: "Application failed to start within 5 minutes"
        
    - name: Wait for application health check
      ansible.builtin.uri:
        url: "http://localhost:8080/health"
        method: GET
        status_code: 200
      register: health_check
      retries: 10
      delay: 30
      until: health_check.status == 200
      
    - name: Wait for specific file to be created
      ansible.builtin.stat:
        path: /var/log/myapp/startup.log
      register: log_file
      retries: 15
      delay: 10
      until: log_file.stat.exists
      
    - name: Wait for database connection
      ansible.builtin.shell: |
        mysql -h {{ db_host }} -u {{ db_user }} -p{{ db_pass }} -e "SELECT 1;"
      register: db_connection
      retries: 5
      delay: 20
      until: db_connection.rc == 0
      no_log: true
      
    - name: Pause for manual verification
      ansible.builtin.pause:
        prompt: "Please verify the application is working correctly, then press enter to continue"
        minutes: 2
```

---

## Block, Rescue, Always

### Example 10: Error Handling with Blocks
```yaml
---
- name: Deployment with comprehensive error handling
  hosts: webservers
  become: true
  
  tasks:
    - name: Application deployment block
      block:
        - name: Stop existing service
          ansible.builtin.service:
            name: myapp
            state: stopped
            
        - name: Backup current application
          ansible.builtin.archive:
            path: /opt/myapp
            dest: "/backup/myapp-{{ ansible_date_time.epoch }}.tar.gz"
            
        - name: Deploy new application version
          ansible.builtin.unarchive:
            src: myapp-v2.0.tar.gz
            dest: /opt/
            remote_src: false
            
        - name: Update configuration
          ansible.builtin.template:
            src: app.conf.j2
            dest: /opt/myapp/config/app.conf
            
        - name: Start service with new version
          ansible.builtin.service:
            name: myapp
            state: started
            
      rescue:
        - name: Log deployment failure
          ansible.builtin.lineinfile:
            path: /var/log/deployment.log
            line: "Deployment failed at {{ ansible_date_time.iso8601 }}"
            create: true
            
        - name: Restore from backup
          ansible.builtin.shell: |
            systemctl stop myapp
            rm -rf /opt/myapp
            tar -xzf /backup/myapp-*.tar.gz -C /
            systemctl start myapp
            
        - name: Send failure notification
          ansible.builtin.mail:
            to: admin@company.com
            subject: "Deployment Failed on {{ inventory_hostname }}"
            body: "Application deployment failed and was rolled back"
            
      always:
        - name: Clean up temporary files
          ansible.builtin.file:
            path: /tmp/myapp-deploy
            state: absent
            
        - name: Update deployment status
          ansible.builtin.uri:
            url: "http://monitoring.company.com/api/deployments"
            method: POST
            body_format: json
            body:
              host: "{{ inventory_hostname }}"
              status: "{{ 'success' if ansible_failed_task is not defined else 'failed' }}"
              timestamp: "{{ ansible_date_time.iso8601 }}"
```

---

## Serial, Throttle, and Forks

### Example 11: Controlled Deployment Strategy
```yaml
---
- name: Rolling deployment with controlled execution
  hosts: webservers
  become: true
  serial: 2  # Deploy to 2 servers at a time
  max_fail_percentage: 25  # Allow 25% failure rate
  
  tasks:
    - name: Health check before deployment
      ansible.builtin.uri:
        url: "http://{{ inventory_hostname }}:8080/health"
        method: GET
      register: pre_check
      
    - name: Drain server from load balancer
      ansible.builtin.uri:
        url: "http://loadbalancer/api/drain/{{ inventory_hostname }}"
        method: POST
      throttle: 1  # One server at a time for load balancer operations
      delegate_to: localhost
      
    - name: Stop application service
      ansible.builtin.service:
        name: myapp
        state: stopped
        
    - name: Deploy new application
      ansible.builtin.copy:
        src: myapp-v2.0.jar
        dest: /opt/myapp/myapp.jar
        backup: true
      throttle: 3  # Limit concurrent file transfers
      
    - name: Start application service
      ansible.builtin.service:
        name: myapp
        state: started
        
    - name: Wait for application to be ready
      ansible.builtin.wait_for:
        port: 8080
        timeout: 120
        
    - name: Health check after deployment
      ansible.builtin.uri:
        url: "http://{{ inventory_hostname }}:8080/health"
        method: GET
        status_code: 200
      retries: 5
      delay: 10
      
    - name: Add server back to load balancer
      ansible.builtin.uri:
        url: "http://loadbalancer/api/enable/{{ inventory_hostname }}"
        method: POST
      throttle: 1
      delegate_to: localhost

# Run with specific fork settings:
# ansible-playbook rolling-deploy.yml --forks=10
```

---

## Callback Plugins Configuration

### Example 12: ansible.cfg with Callback Plugins
```ini
[defaults]
inventory = inventory/hosts
remote_user = ansible
host_key_checking = False
retry_files_enabled = False
log_path = /var/log/ansible/ansible.log
callback_whitelist = profile_tasks, timer, slack

# Slack callback configuration
slack_webhook_url = https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK
slack_channel = #devops
slack_username = ansible-bot

# Performance settings
forks = 15
poll_interval = 15
timeout = 30

# Vault settings
vault_password_file = ~/.ansible/vault_pass

[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml

[ssh_connection]
pipelining = True
control_path = /tmp/ansible-ssh-%%h-%%p-%%r
```

### Custom Callback Plugin Example
```python
# ~/.ansible/plugins/callback/custom_logger.py
from ansible.plugins.callback import CallbackBase
import json
import time

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'custom_logger'

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.start_time = time.time()

    def v2_playbook_on_start(self, playbook):
        self._display.display("=== PLAYBOOK START ===")
        self._display.display(f"Playbook: {playbook._file_name}")
        self._display.display(f"Started at: {time.ctime()}")

    def v2_playbook_on_stats(self, stats):
        end_time = time.time()
        duration = end_time - self.start_time
        
        self._display.display("=== PLAYBOOK STATS ===")
        self._display.display(f"Duration: {duration:.2f} seconds")
        
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            s = stats.summarize(h)
            self._display.display(f"Host {h}: ok={s['ok']} changed={s['changed']} failed={s['failures']}")
```

---

## Advanced Inventory Examples

### Example 13: Dynamic Inventory with Groups
```yaml
# inventory/group_vars/all.yml
---
ntp_servers:
  - pool.ntp.org
  - time.google.com

common_packages:
  - htop
  - curl
  - git

# inventory/group_vars/webservers.yml
---
nginx_worker_processes: auto
nginx_worker_connections: 1024
ssl_certificate: /etc/ssl/certs/company.crt

# inventory/host_vars/web01.yml
---
server_role: primary
nginx_worker_processes: 4
backup_schedule: "0 2 * * *"

# inventory/hosts.yml
---
all:
  children:
    webservers:
      hosts:
        web01:
          ansible_host: 192.168.1.10
          environment: production
        web02:
          ansible_host: 192.168.1.11
          environment: production
        web03:
          ansible_host: 192.168.1.12
          environment: staging
    databases:
      hosts:
        db01:
          ansible_host: 192.168.1.20
          mysql_role: master
        db02:
          ansible_host: 192.168.1.21
          mysql_role: slave
    loadbalancers:
      hosts:
        lb01:
          ansible_host: 192.168.1.30
          lb_algorithm: roundrobin
```

---

This comprehensive example file demonstrates practical implementations of all the key concepts mentioned in the interview notes, providing ready-to-use templates and patterns for real-world Ansible automation.
