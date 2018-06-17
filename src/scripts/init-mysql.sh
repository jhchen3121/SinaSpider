#!/bin/sh
#-*- coding:utf-8 -*- 

if [ -z "$PROJ_NAME" ];then
    echo PROJ_DIR not set
    exit 1
fi

proj_name=$PROJ_NAME
proj_db="${proj_name}db"

echo "Project Name: $proj_name"
echo "MySQL username: $proj_name"
echo "MySQL password: $proj_name"
echo "MySQL Database: $proj_db"

cat << EOF|mysql -u root -v | sed -e '/^$/d' -e '/----/d' -e 's/^/\t[-] /'
drop database if exists ${proj_db};
create database ${proj_db} default character set = utf8;
EOF

cat << EOF|mysql -u root -v | sed -e '/^$/d' -e '/----/d' -e 's/^/\t[-] /'
drop user '${proj_name}'@'localhost';
EOF

cat << EOF|mysql -u root -v | sed -e '/^$/d' -e '/----/d' -e 's/^/\t[-] /'
create user '${proj_name}'@'localhost' identified by '${proj_name}';
grant all on ${proj_db}.* to '${proj_name}'@'localhost';
EOF
