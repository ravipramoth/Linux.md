# Linux Utilities and Permissions

## File/Directory Permissions

- -> it is file or directory d-> Directory l --> link file 
rw- --> Owner of file 
r--  --- > group permission 
r-- -->  Other permission 

0==>  No Permission 
1==> Excute 
2==> write 
3 (2+1) ==> Execute + read 
4 ===> read 
5 (4+1) ==> read + excute 
6 (4+2) ===> read + write 
7 == Full Permission  ( R+ W + X )

Default permission  file create 644 
default Permission for directory 755 

Link file is noting both Shortcut 

Hard Link --- > What ever change happen in actual file and same will be changed in shortcut file change will happen 
            --- > in case if we delete file -- > still we can have shorcut file 
            ln <orginal - file name > < shortcut-file >

Soft Link : --- > What ever change happen in actual file and same will be changed in shortcut file change will happen 
            --> if we delete orginal file shortcut file become danggling not accessible 
            ln -s <orginal - file name > < shortcut-file >

## Zip Commands

to create a zip file 
    zip newfile-name <file1,file2>
to see the content in the zip file 
    zip -sf <zip file name >
to append a file to zip 
    zip -r <zipfilename> < appendfile>

## Find Command Examples

find /var/log -type f -mtime +7
dd if=/dev/zero of=15mb_file.txt bs=1M count=100

## System Info Script Outline

Write a Script which will help you get important details of your machine like

- IP Details
- Uptime
- Last login details
- Disk Space Utilization
- Free Memory Stats
