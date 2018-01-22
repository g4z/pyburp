#!/usr/bin/env bash

lxc rm --force foo
lxc init ubuntu foo
lxc config set foo user.user-data - < cloudinit.yml 
lxc config show foo
lxc start foo
