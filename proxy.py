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


# This function directly writes to the apt.conf file
def writeToApt(proxy, port, username, password, flag):
    filepointer = open(APT_CONF, "w")
    if not flag:
        filepointer.write(
            'Acquire::http::proxy "http://{0}:{1}@{2}:{3}/";\n'.format(username, password, proxy, port))
        filepointer.write(
            'Acquire::https::proxy  "https://{0}:{1}@{2}:{3}/";\n'.format(username, password, proxy, port))
        filepointer.write(
            'Acquire::ftp::proxy  "ftp://{0}:{1}@{2}:{3}/";\n'.format(username, password, proxy, port))
        filepointer.write(
            'Acquire::socks::proxy  "socks://{0}:{1}@{2}:{3}/";\n'.format(username, password, proxy, port))
    filepointer.close()


# This function writes to the environment file
# Fist deletes the lines containng http:// , https://, ftp://
def writeToEnv(proxy, port, username, password, flag):
    # find and delete line containing http://, https://, ftp://
    with open(ENVIRONMENT, "r+") as opened_file:
        lines = opened_file.readlines()
        opened_file.seek(0)  # moves the file pointer to the beginning
        for line in lines:
            if r"http://" not in line and r"https://" not in line and r"ftp://" not in line and r"socks://" not in line:
                opened_file.write(line)
        opened_file.truncate()

    # writing starts
    if not flag:
        filepointer = open(ENVIRONMENT, "a")
        filepointer.write(
            'http_proxy="http://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.write(
            'https_proxy="https://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.write(
            'ftp_proxy="ftp://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.write(
            'socks_proxy="socks://{0}:{1}@{2}:{3}/"\n'.format(username, password, proxy, port))
        filepointer.close()


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
    writeToApt(proxy, port, username, password, flag)
    writeToEnv(proxy, port, username, password, flag)
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
