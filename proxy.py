#!/usr/bin/env python3

"""
Script to configure system-wide proxy settings on Linux distributions.

created by:
Nityananda Gohain 
School of Engineering, Tezpur University
27/10/17

Modified by:
Pablo Peitsch
Data Scientist, UNSAM, ARG
"""

# This files takes the location as input and writes the proxy authentication

import getpass
import os
import shutil
import sys

APT_CONF = '/etc/apt/apt.conf'
APT_BACKUP = './.backup_proxy/apt.txt'
BASH_BASHRC = r'/etc/bash.bashrc'
BASH_BACKUP = r'./.backup_proxy/bash.txt'
ENVIRONMENT = r'/etc/environment'
ENV_BACKUP = r'./.backup_proxy/env.txt'


def write_to_apt(proxy, port, username, password, flag):
    """
    Writes the proxy configuration to the apt.conf file.

    :param proxy: Proxy address
    :param port: Proxy port
    :param username: Username for authentication
    :param password: Password for authentication
    :param flag: Flag indicating whether to remove the configuration
    """
    with open(APT_CONF, "w") as filepointer:
        if not flag:
            filepointer.write(f'Acquire::http::proxy "http://{username}:{password}@{proxy}:{port}/";\n')
            filepointer.write(f'Acquire::https::proxy "https://{username}:{password}@{proxy}:{port}/";\n')
            filepointer.write(f'Acquire::ftp::proxy "ftp://{username}:{password}@{proxy}:{port}/";\n')
            filepointer.write(f'Acquire::socks::proxy "socks://{username}:{password}@{proxy}:{port}/";\n')


def write_to_env(proxy, port, username, password, flag):
    """
    Writes the proxy configuration to the environment file.

    :param proxy: Proxy address
    :param port: Proxy port
    :param username: Username for authentication
    :param password: Password for authentication
    :param flag: Flag indicating whether to remove the configuration
    """
    with open(ENVIRONMENT, "r+") as opened_file:
        lines = opened_file.readlines()
        opened_file.seek(0)
        for line in lines:
            if all(protocol not in line for protocol in ["http://", "https://", "ftp://", "socks://"]):
                opened_file.write(line)
        opened_file.truncate()

    if not flag:
        with open(ENVIRONMENT, "a") as filepointer:
            filepointer.write(f'http_proxy="http://{username}:{password}@{proxy}:{port}/"\n')
            filepointer.write(f'https_proxy="https://{username}:{password}@{proxy}:{port}/"\n')
            filepointer.write(f'ftp_proxy="ftp://{username}:{password}@{proxy}:{port}/"\n')
            filepointer.write(f'socks_proxy="socks://{username}:{password}@{proxy}:{port}/"\n')


# This function will write to the
def writeToBashrc(proxy, port, username, password, flag):
    # find and delete http:// , https://, ftp://
    with open(BASH_BASHRC, "r+") as opened_file:
        lines = opened_file.readlines()
        opened_file.seek(0)
        for line in lines:
            if r"http://" not in line and r'"https://' not in line and r"ftp://" not in line and r"socks://" not in line:
                opened_file.write(line)
        opened_file.truncate()

    # writing starts
    if not flag:
        filepointer = open(BASH_BASHRC, "a")
        filepointer.write(
            'export http_proxy="http://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.write(
            'export https_proxy="https://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.write(
            'export ftp_proxy="ftp://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.write(
            'export socks_proxy="socks://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.close()


def set_proxy(flag):
    proxy, port, username, password = "", "", "", ""
    if not flag:
        proxy = input("Enter proxy : ")
        port = input("Enter port : ")
        username = input("Enter username : ")
        password = getpass.getpass("Enter password : ")
    write_to_apt(proxy, port, username, password, flag)
    write_to_env(proxy, port, username, password, flag)
    writeToBashrc(proxy, port, username, password, flag)


def view_proxy():
    # finds the size of apt file
    size = os.path.getsize(APT_CONF)
    if size:
        filepointer = open(APT_CONF, "r")
        string = filepointer.readline()
        print('\nHTTP Proxy: ' + string[string.rfind('@') + 1: string.rfind(':')])
        print('Port: ' + string[string.rfind(':') + 1: string.rfind('/')])
        print('Username: ' + string.split('://')[1].split(':')[0])
        print('Password: ' + '*' * len(string[string.rfind(':', 0, string.rfind('@')) + 1: string.rfind('@')]))
        filepointer.close()
    else:
        print("No proxy is set")


def restore_default():
    # copy from backup to main
    shutil.copy(APT_BACKUP, APT_CONF)
    shutil.copy(ENV_BACKUP, ENVIRONMENT)
    shutil.copy(BASH_BACKUP, BASH_BASHRC)


# The main Function Starts


if __name__ == "__main__":

    # create backup	if not present
    if not os.path.isdir("./.backup_proxy"):
        os.makedirs("./.backup_proxy")
        if os.path.isfile(APT_CONF):
            shutil.copyfile(APT_CONF, APT_BACKUP)
        shutil.copyfile(ENVIRONMENT, ENV_BACKUP)
        shutil.copyfile(BASH_BASHRC, BASH_BACKUP)

    # choice
    print("Please run this program as Super user(sudo)\n")
    print("1:) Set Proxy")
    print("2:) Remove Proxy")
    print("3:) View Current Proxy")
    print("4:) Restore Default")
    print("5:) Exit")
    choice = int(input("\nChoice (1/2/3/4/5) : "))

    if choice == 1:
        set_proxy(flag=0)
    elif choice == 2:
        set_proxy(flag=1)
    elif choice == 3:
        view_proxy()
    elif choice == 4:
        restore_default()
    else:
        sys.exit()

    print("DONE!")
