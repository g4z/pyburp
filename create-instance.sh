#!/usr/bin/env bash

for i in $(seq 1 2); do
    label=herbert_$(printf "%03d" $i)
    lxc rm --force $label
    lxc init ubuntu $label
    lxc config set $label user.user-data - < cloudinit.yml 
    # lxc config show $label
    lxc start $label
done
