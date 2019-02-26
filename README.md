# OneSHelper

OpenNebula shell extender

## Install

    git clone https://github.com/zztalker/onesh.git
    cd onesh
    ./install.sh

Put credentials to environment variables ONE_USER, ONE_PASSWORD or
in ~/.one/one_auth file in format login:password.

Put endpoint URL to environment variable ONE_ENDPOINT or
in ~/.one/endpoint file for example:

    cat /~.one/endpoint
    https://nebula.cloud.com:1234/RPC2

## Usage

- Get list of VMS:

    `onels`

- SSH to vm cloud-1:

    `onesh c<TAB><ENTER>`

![List of vms and ssh](https://raw.githubusercontent.com/zztalker/onesh/master/github-assets/onesh_onels.gif)

- RSYNC current folder to cloud-1:

    `onesync c<TAB> \remote`

- PING cloud-1:

    `oneping c<TAB><ENTER>`

- SCP file to same file on cloud-1:

    `onescp /etc/hosts c<TAB><ENTER>`

- SCP file to different path on cloud-1:

    `onescp /etc/hosts c<TAB> /root/test`

## TODO

1. oneping (ping VM)
