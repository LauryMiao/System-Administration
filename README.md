# System-Administration

ssh_su.py
#
# Function: ssh to remote linux server with normal_user and su - to root and execute shell_cmd in multiprocess
#
# Bugs: can NOT ending quickly (jump out of the while loop) with wrong password for root
#

Formate:
ip.txt:
ip1,normal_user,pwd_for_normal_user,pwd_for_root,shell_cmd
ip2,normal_user,pwd_for_normal_user,pwd_for_root,shell_cmd

usage:
python ssh_su.py
