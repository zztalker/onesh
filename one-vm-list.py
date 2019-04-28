#!/usr/bin/env python3

import argparse
import datetime
import json
import os
import pyone
import sys
import subprocess
import time


ONE_DIR = os.path.expanduser('~/.one')
ONE_AUTH = 'one_auth'
ONE_ENDPOINT = 'endpoint'
ONE_CACHE = 'cache'
CACHE_TIME = 30  # in seconds


def create_one_dir():
    os.makedirs(ONE_DIR, exist_ok=True)


def get_one_auth_data():
    """
    Return (username, password, endpoint) tuple.
    """

    try:
        with open(ONE_DIR + '/' + ONE_AUTH) as f:
            one_user, one_password = f.readline().strip().split(":", 1)
    except:
        try:
            one_user = os.environ['ONE_USER']
            one_password = os.environ['ONE_PASSWORD']
        except KeyError:
            sys.exit('You must specify OpenNebula credentials in '
                     '~/.one/one_auth file or in environment variables')
    try:
        with open(ONE_DIR + '/' + ONE_ENDPOINT) as f:
            one_endpoint = f.readline().strip()
    except:
        try:
            one_endpoint = os.environ['ONE_ENDPOINT']
        except KeyError:
            sys.exit('You must specify OpenNebula XML-RPC endpoint in '
                     '~/.one/endpoint file or in environment variable')
    return one_user, one_password, one_endpoint


def get_cache():
    """
    Return cache vm data or None.
    """

    path_cache = ONE_DIR + '/' + ONE_CACHE
    if os.path.exists(path_cache):
        with open(path_cache) as f:
            cache_json = json.load(f)
            # check last update time
            if cache_json.get('timestamp'):
                last_update = datetime.datetime.fromtimestamp(
                    cache_json['timestamp'])
                delta = datetime.timedelta(seconds=CACHE_TIME)
                now = datetime.datetime.now()
                if (now - last_update) < delta:
                    return cache_json['vms']


def set_cache(one_data: dict) -> None:
    data = {
        'timestamp': time.time(),
        'vms': one_data
    }
    with open(ONE_DIR + '/' + ONE_CACHE, 'w') as f:
        json.dump(data, f)


def get_one_info(one_user, one_password, one_endpoint) -> dict:
    """
    Return data of virtual machines from OpenNebula.
    """
    one = pyone.OneServer(
        one_endpoint, session="{}:{}".format(one_user, one_password))

    vm_pool = one.vmpool.info(
        -3,  # only own vm
        -1,  # When the next parameter is >= -1 this is the Range start ID.
             # Can be -1. For smaller values this is the offset used for
             # pagination.
        -1,  # For values >= -1 this is the Range end ID. Can be -1 to get
             # until the last ID. For values < -1 this is the page size used
             # for pagination.
        3  # vm stat - active
    )

    vms = dict()
    for vm in vm_pool.get_VM():
        vms[vm.get_NAME()] = vm.get_TEMPLATE()["NIC"]["IP"]
    return vms


def get_template_info(one_user, one_password, one_endpoint) -> dict:
    """
    Return list of templates from OpenNebula.
    """
    one = pyone.OneServer(
        one_endpoint, session="{}:{}".format(one_user, one_password))

    list_templates = one.templatepool.info(
         -2, # -4: Resources belonging to the user’s primary group
             # -3: Resources belonging to the user
             # -2: All resources
             # -1: Resources belonging to the user and any of his groups
             # >= 0: UID User’s Resources
         -1, # >= -1 this is the Range start ID. Can be -1.
             # For smaller values this is the offset used for pagination.
         -1  # For values >= -1 this is the Range end ID.
             # Can be -1 to get until the last ID. For values < -1 this is the page size used for pagination.
	     # http://docs.opennebula.org/5.6/integration/system_interfaces/api.html#one-templatepool-info
    )
    tpls = dict()
    for tp in list_templates.get_VMTEMPLATE():
        tpls[tp.get_NAME()] = tp.get_ID(),tp.get_UNAME()
    return tpls



def vm_on_tmpl (one_user, one_password, one_endpoint,tpl_id, vm_name, start_type, addit_params, tpl_copy) -> dict:
    tpls = dict()
    start_type = False
    tpl_copy = False
    addit_params = ""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command', nargs='*',
        help='''
        createvm - create new VM based on template,
    ''')
    one = pyone.OneServer(
        one_endpoint, session="{}:{}".format(one_user, one_password))
    create_vm_based_on_tpl = one.template.instantiate(
            tpl_id,
            "%s" % vm_name,
            False,
            " ",
            False
    )

def run_command(one_vms) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command', nargs='*',
        help='''
    listvms - show list of VMs,
    listtp - show list of all available templates,
    ssh vm - connect to vm,
    scp vm file [/path/to/file/on/vm] - scp file to vm if path/to not set used same,
    rsync vm /path/on/vm - rsync current folder to vm,
    ping vm
    ''')  # noqa

    args = parser.parse_args()
    if args.command[0] == 'listvms':
        for k, v in one_vms.items():
            print(k, v)
    elif args.command[0] == 'listtp':
        user, password, endpoint = get_one_auth_data()
        one_tpls=get_template_info(user, password, endpoint)
        for k in one_tpls.items():
            print(k)
    elif args.command[0] == 'createvm':
         tpl_id = int(args.command[1])
         vm_name = args.command[2]
         #vm_options = "";
         if type(tpl_id) == int:
             #vm_on_tmpl
             print(tpl_id, "%s" % vm_name)
             user, password, endpoint = get_one_auth_data()
             vm_on_tmpl(user, password, endpoint, tpl_id, vm_name, False, "", False)
         else:
             print("please, check that template ID was set propely")
    elif args.command[0] == 'ssh':
        subprocess.call(['ssh', 'root@{}'.format(one_vms[args.command[1]])])
    elif args.command[0] == 'ping':
        try:
            subprocess.call(['ping', one_vms[args.command[1]]])
        except KeyboardInterrupt:
            pass
    elif args.command[0] == 'scp':
        vm_name = args.command[1]
        path_to_files = args.command[2:-1]
        if len(args.command) < 4:
            print("""Need to use at least 3 arguments, for example:

            onescp vm-name myfile /home/user

            Last argument - destination folder on remote.""")
        else:
            path_on_remote = args.command[-1]
            print("Sent files to {}:{}".format(vm_name, path_on_remote))
            subprocess.call([
                'scp', *path_to_files,
                'root@{}:{}'.format(one_vms[vm_name], path_on_remote)])
    elif args.command[0] == 'rsync':
        subprocess.call([
            'rsync', '-av', '--chown=root:root', '.',
            'root@{}:{}'.format(one_vms[args.command[1]], args.command[2])
        ])


def main():
    create_one_dir()
    user, password, endpoint = get_one_auth_data()
    vms = get_cache()
    if vms is None:
        vms = get_one_info(user, password, endpoint)
        set_cache(vms)
    run_command(vms)


if __name__ == '__main__':
    main()
