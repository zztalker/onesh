#!/usr/bin/env python3

import argparse
import os
import pyone
import sys
import subprocess

try:
    with open(os.path.expanduser('~/.one/one_auth')) as f:
        ONE_USER, ONE_PASSWORD = f.readline().strip().split(":", 1)
except:
    try:
        ONE_USER = os.environ['ONE_USER']
        ONE_PASSWORD = os.environ['ONE_PASSWORD']
    except KeyError:
        sys.exit('You must specify OpenNebula credentials in ~/.one/one_auth'
                 ' file or in environment variables')

try:
    with open(os.path.expanduser('~/.one/endpoint')) as f:
        ONE_ENDPOINT = f.readline().strip()
except:
    try:
        ONE_ENDPOINT = os.environ['ONE_ENDPOINT']
    except KeyError:
        sys.exit('You must specify OpenNebula XML-RPC endpoint in '
                 '~/.one/endpoint file or in environment variable')

parser = argparse.ArgumentParser()
parser.add_argument(
    'command', nargs='*',
    help='listvms - show list of VMs, ssh - connect to vm')

args = parser.parse_args()

one = pyone.OneServer(
    ONE_ENDPOINT, session="{}:{}".format(ONE_USER, ONE_PASSWORD))

vm_pool = one.vmpool.info(
    -3,  # only own vm
    -1,  # When the next parameter is >= -1 this is the Range start ID.
         # Can be -1. For smaller values this is the offset used for
         # pagination.
    -1,  # For values >= -1 this is the Range end ID. Can be -1 to get until
         # the last ID. For values < -1 this is the page size used for
         # pagination.
    3  # vm stat - active
)

vms = dict()
for vm in vm_pool.get_VM():
    vms[vm.get_NAME()] = vm.get_TEMPLATE()["NIC"]["IP"]

if args.command[0] == 'listvms':
    for k in vms.keys():
        print(k)
elif args.command[0] == 'ssh':
    subprocess.call(['ssh', 'root@{}'.format(vms[args.command[1]])])
