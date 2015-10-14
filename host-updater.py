#!/bin/env python3
#
# Updates the host file with given urls
#
# © 2015 Daniel Jankowski
# Licensed under the GNU Lesser General Public License Version 3(LGPLv3).

import urllib.request
import subprocess
import platform
import shutil
import re


URLS = ['http://someonewhocares.org/hosts/hosts', 'http://pastebin.com/raw.php?i=6Z8kwQEL']
HOST_LOCATION = '/etc/hosts'


def append_to_hosts(inp):
    with open(HOST_LOCATION, 'a') as fp:
        for i in inp:
            fp.write('\n' + i)


def compare(new_in, old_in):
    new, addition, old = [], [], []
    
    for n in new_in:
        new.append(set(n))
    
    for o in old_in:
        o = re.sub('\t', '', o)
        old.append(re.sub('\s*', '', o))
    old = set(old)
    
    for host in new:
        for item in host:
            item_e = re.sub('\t', '', item)
            item_e = re.sub('\s*', '', item_e)
            if not item_e in old:
                addition.append(item)
    return addition


def remove_comments(inp):
    out = []
    for i in inp:
        if not i.startswith('#') or i == '':
            out.append(i)
    return out


def backup_old_hosts():
    shutil.copyfile(HOST_LOCATION, HOST_LOCATION + '.backup')


def get_old_host():
    hosts = []
    with open(HOST_LOCATION, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            line = re.sub('(\n)*', '', line)
            hosts.append(line)
    return hosts


def get_host_files():
    hosts, edit = [], []
    for url in URLS:
        rqst = urllib.request.urlopen(url)
        data = rqst.read().decode('utf-8')
        hosts.append(data)
    for host in hosts:
        host = re.sub('\r', '', host)
        host = host.split('\n')
        edit.append(host)
    return edit


def reboot():
    os = platform.system()
    if os == 'Linux':
        subprocess.Popen(['shutdown', '-r', 'now'])
        return
    elif os == 'Windows':
        subprocess.Popen(['shutdown', '-r', '-t', '00'])
        return
    elif os == 'Darwin':
        subprocess.Popen(['shutdown', '-r', 'now'])
        return


def main():
    print('Host File Updater\n\n')

    new_hosts = []
    new_hosts_ed = get_host_files()
    for host in new_hosts_ed:
        host = remove_comments(host)
        new_hosts.append(host)
    old_hosts = remove_comments(get_old_host())

    addition = compare(new_hosts, old_hosts)
    
    print('Found ' + str(len(addition)) + ' new entries!\n\nAppend them to ' + HOST_LOCATION + '? [y/n]\n')
    choice = input('> ')
    if choice.lower() == 'y':
        backup_old_hosts()
        append_to_hosts(addition)

        print('\nDo you want to reboot? [y/n]\n')
        choice = input('>')
        if choice.lower() == 'y':
            reboot()
        else:
            return True
    elif choice.lower() == 'n':
        return True
    else:
        print('Wrong input! Exiting...')
        return False


if __name__ == '__main__':
    main()
