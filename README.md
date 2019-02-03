# OneSHelper

OpenNebula shell extender

## Install

    git clone git:....

    cp one-vm-list.py ~/.local/bin

    add to your ~/.bashrc

        source onesh-completion.sh

    put credentials to environment variables ONE_USER, ONE_PASSWORD or in ~/.one/one_auth file
    in format login:password

    put endpoint URL to environment variable ONE_ENDPOINT or in ~/.one/endpoint file for example:

        https://nebula.cloud.com:1234/RPC2

## Usage

    Get list of VMS:

        onesh <TAB><TAB>

    SSH to vm cloud-1:

        onesh c<TAB><ENTER>

## TODO:

1. onesync (rsync current folder to specified folder of vm)
2. oneping (ping VM)
