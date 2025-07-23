# Ansible Module to Work with Files

## 1. ansible.builtin.command
Executes a command on a remote machine.

**Description:**  
Runs a specified command on the target machine. It does not process the command through a shell, so no shell features like piping, redirection, or variable substitution are available.

**Examples:**
- `ansible all -m ansible.builtin.command -a "ls /home/" -b`
- `ansible all -m ansible.builtin.command -a "ls -l /var/log" -b`
- `ansible all -m ansible.builtin.command -a "mkdir -p /tmp/demo-dir" -b`


## 2. ansible.builtin.shell
Executes a shell command on the remote machine.

**Description:**  
Runs a shell command on the target machine, and allows you to use shell features like pipes, redirects, and variable substitution.

**Examples:**
- `ansible all -m ansible.builtin.shell -a "echo 'Hello, World!' > /opt/hello.txt" -b`
- `ansible all -m ansible.builtin.shell -a "cat /home/ansadmin/test/test.txt | wc -l" -b`

### Difference between `shell` and `command`

| Feature                   | `command`         | `shell`           |             |
| ------------------------- | ----------------- | ----------------- | ----------- |
| Uses shell                | ❌ No              | ✅ Yes             |             |
| Supports pipes (`|`)      | ❌ No              | ✅ Yes             |             |
| Supports redirects (`>`)  | ❌ No              | ✅ Yes             |             |
| Safe from shell injection | ✅ Yes             | ❌ No              |             |
| Performance               | ✅ Slightly faster | ❌ Slightly slower |             |
| Example                   | `ls -l /etc`      | `ls -l /etc | grep conf` |             |

## 3. ansible.builtin.file

Create/Modify file attributes like permissions, owner, and group.  
It can create/delete directories or files.

**Description:**  
Used to set or change the permissions, ownership, and symbolic links of files or directories on the remote machine.

**Examples:**
- `ansible all -m ansible.builtin.file -a "path=/home/ansadmin/test/test.txt mode=0644 owner=ansadmin group=ansadmin" -b`
- `ansible all -m ansible.builtin.file -a "path=/home/ansadmin/test/dirc owner=ansadmin group=ansadmin state=directory" -b`

### Options:
- **Create a file:** `touch`
- **Create a directory:** `directory`
- **Delete a file/directory:** `absent`
- **Create a symbolic link (soft link):** `link`
- **Create a hard link:** `hard`

**Example for link creation:**
- `ansible all -m ansible.builtin.file -a "src=/home/ansadmin/test/test2.txt dest=/tmp/text.txt owner=ansadmin group=ansadmin state=link" -b`


--------------------------------------------------------------------------------------- 

## 4. ansible.builtin.copy

We can copy files from the controller to managed nodes.

**Example 1:**  
Copy a file from the controller to managed nodes:
```bash
ansible all -m ansible.builtin.copy -a "src=/home/ansadmin/aws dest=/tmp" -b
``` 
**Example 2:** 
Copy inline content to a file on managed nodes 
```bash
ansible all -m ansible.builtin.copy -a "content='# This is demo to show inline content to file \n' dest=/tmp/aws" -b
```
**Example 3:**

```bash
ansible all -m ansible.builtin.copy -a "content='# This is demo to inline content to file \n' dest=/tmp/aws backup=true" -b
``` 


------------------------------------------- 
## 5. ansible.builtin.lineinfile

**Purpose:** Ensure a specific line is present or absent in a file.

### State Options:
- `state=present`: Ensures the line is present in the file.
- `state=absent`: Ensures the line is absent from the file.

### Example 1: Add a line to a file
```bash
ansible all -m ansible.builtin.lineinfile -a "path=/etc/hostname line='newhostname' state=present create=yes"
```
### Example 2: Remove a line from a file
```bash
ansible all -m ansible.builtin.lineinfile -a "path=/etc/hostname line='oldhostname' state=absent"

``` 
### Create a Test File on All Hosts

This command creates a test file with some content on all hosts:
```bash

ansible all -m ansible.builtin.copy -a "dest=/tmp/demo.txt content='Name: Alice\nAge: 30\nCity: Mumbai\n'"

``` 
Insert a Line After a Pattern Match 

``` 
ansible all -m ansible.builtin.lineinfile -a "path=/tmp/demo.txt line='Phone: 1234567890' insertafter='^Name:'" -b

``` 

Insert a Line Before a Pattern Match
``` 
ansible all -m ansible.builtin.lineinfile -a "path=/tmp/demo.txt line='Country: India' insertbefore='^City:'" -b

```
Insert a Line at the End (if not present)

``` bash 
ansible all -m ansible.builtin.lineinfile -a "path=/tmp/demo.txt line='Email: alice@example.com'"
``` 
Insert a Line at the End Using EOF

```bash 

ansible all -m ansible.builtin.lineinfile -a "path=/tmp/demo.txt line='--- End of File ---' insertafter=EOF"

``` 

Replace Line with Matching Pattern 
 
 ``` bash 
ansible all -m ansible.builtin.lineinfile -a "path=/tmp/demo.txt regexp='^City:' line='City: Chennai'"
``` 
Replace Line with Matching Pattern

``` bash 

ansible all -m ansible.builtin.lineinfile -a "path=/tmp/demo.txt regexp='^Phone:' state=absent"

``` 

## 6. ansible.builtin.stat

Purpose: Insert a block of text into a file 

###Example: Add a block of lines to a configuration file

``` bash 
ansible all -m ansible.builtin.stat -a "path=/path/to/file"

``` 

## 7. ansible.builtin.blockinfile

Purpose: Insert a block of text into a file.

### Example: Add a block of lines to a configuration file

``` bash 
ansible all -m ansible.builtin.blockinfile -a "path=/etc/my_config.conf block='[section1]\noption1=value1\noption2=value2' state=present"
``` 
## 8. Fetch Module 
Purpose: To download the file from remote servers to controller node 
``` bash
 PROD -m ansible.builtin.fetch -a "src =/opt/devops dest= /tmp/ flat=true" -b 
``` 
## 9. Package Module 

Purpose : to install package to manged nodes 

Type :  ansible.builtin.package  -- Genric Package 
        ansible.builtin.yum -- RHEL Famil ( red hat, amazon linu, cent os )
        ansible.builtin.apt -- Debian ( ubuntu)
        ansible.builtin.dnf -- RHEL family 

### Example 

``` bash
ansible all -m ansible.builtin.package -a "name=s/w package state=present/absent/latest/started/enabled/restared" 

``` 

note: if you run ansible command with diffren user you can use -u or --username 
To password you need use -k " it prompt the password" 

## 10 . Facts 

Purpose : it will collect some information about the manged nodes. These collected facts called as Gather facts 

it will saved on JSON format 

``` bash 

ansible all -m ansible.builtin.setup -a "filter=ansible_distribution,ansible_uptime_seconds" 

``` 




 