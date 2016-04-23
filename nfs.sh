#!/bin/bash
#
# Name:NFS_collection
#
# version: 0.1
#
# Description: Get NFS_collection
#
# Author: Laury Miao
#
# Date: 18 Apr 2016
# 
#

df -hT | grep -B 1 nfs | awk '{if (NR%2==0) {printf"%s\n" ,$0} else {printf"%s",$0}}' > ~/nfs.txt

local_IP=$(cat /etc/sysconfig/network-scripts/ifcfg-eth0  | grep IPADDR | awk -F '=' '{print $2}')
FILE=~/nfs.txt
echo '******************** Summary *************************'
echo 'src_IP src_dir local_IP local_dir user-name user-uid group-name group-gid'


while read line; do
	#statements
	src=$(echo ${line} | awk '{print $1}')
	src_IP=$(echo $src | awk -F':' '{print $1}')
	src_dir=$(echo $src | awk -F':' '{print $2}')
	local_dir=$(echo ${line} | awk '{print $NF}')
	user_name=$(ls -ld $local_dir | awk '{print $3}')
	user_uid=$(ls -dln $local_dir | awk '{print $3}')
	group_name=$(ls -dl $local_dir | awk '{print $4}')
	group_gid=$(ls -dln $local_dir | awk '{print $4}')

	echo $src_IP $src_dir $local_IP $local_dir $user_name $user_uid $group_name $group_gid


done < $FILE


if [ ! -f "/usr/bin/nfsmount.sh" ];then
	mt_nfs='No nfsmount.sh'
else
	mt_nfs=$(cat /usr/bin/nfsmount.sh)
fi

if [ ! -f "/usr/bin/nfsumount.sh" ];then
	umt_nfs='No nfsumount.sh'
else
	umt_nfs=$(cat /usr/bin/nfsumount.sh)
fi
echo '********************NFS Mount*************************'
echo $mt_nfs
echo '********************NFS Umount*************************'
echo $umt_nfs
