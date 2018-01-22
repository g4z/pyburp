#!/usr/bin/env bash

for i in $(seq 1 2); do
    label=herbert$(printf "%03d" $i)
    lxc rm --force $label
    lxc init ubuntu $label
    sed "s/{{botnick}}/$label/g" cloudinit.yml > /tmp/buffer.yml
    lxc config set $label user.user-data - < /tmp/buffer.yml
    # lxc config show $label
    lxc start $label
done
