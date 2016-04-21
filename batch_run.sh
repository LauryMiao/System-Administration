#!/bin/bash
#
# Name:batch_run
#
# version: 0.1
#
# Description: get the first parameter and the second parameter
#
# Author: Laury Miao
#
# Date: 11 Mar 2016
# Input File: IP.list contains IP and Password
#
FILE=IP.list
while read line; do
	#statements
	IP=$(echo ${line} | awk '{print $1}')
	PassWord=$(echo ${line} | awk '{print $2}')
	spawn ssh root@${IP} 
	expect 	"*yes/no" 
	send "yes\r"
	expect "*password:" 
	send "${PassWord}\r"
	expect "#*"
	send "/bin/bash < ./operation.sh"
	send "exit\r"
	expect eof
done < $FILE
#IP=10.182.131.95
#ssh root@${IP} '/bin/bash' < ./operation.sh
