'''
Date Modified: 2017-3-20
Author: Billy Downing
Purpose: Take inputs in order to log
into several devices, run an exec command,
and output the results to a file.
'''


import os
import getpass
from netmiko import ConnectHandler

cmdFilename = input('Enter Source Filename - Commands: ')
deviceFilename = input('Enter Source Filename - Devices: ')
outputFilename = input('Enter Destination Filename: ')
username = input('Username: ')
password = getpass.getpass(prompt='Password: ', stream=None)


def get_commands(cmdFilename):
    with open(cmdFilename, 'r') as cmd:
        cmdLines = cmd.read()
        cmdList = cmdLines.split('\n')
    return cmdList

def get_devices(deviceFilename):
    with open(deviceFilename, 'r') as deviceIP:
        deviceIPLines = deviceIP.read()
        deviceIPList = deviceIPLines.split('\n')
    return deviceIPList

def device_dict(deviceFilename,username,password):

    ipAddressList = (get_devices(deviceFilename))
    try:
        if (ipAddressList[0].lower()) == 'asa':
            ipAddressList.remove(ipAddressList[0])

            for IP in ipAddressList:
                ASA = {
                    'device_type': 'cisco_asa',
                    'ip': IP,
                    'username': username,
                    'password': password
                    }
                ssh_conn = ConnectHandler(**ASA)
                push_config(ssh_conn)

        elif (ipAddressList[0].lower()) == 'ios':
            ipAddressList.remove(ipAddressList[0])

            for IP in ipAddressList:
                IOS = {
                    'device_type': 'cisco_ios',
                    'ip': IP,
                    'username': username,
                    'password': password
                    }
                ssh_conn = ConnectHandler(**IOS)
                push_config(ssh_conn)

        elif (ipAddressList[0].lower()) == 'nxos':
            ipAddressList.remove(ipAddressList[0])

            for IP in ipAddressList:
                NXOS = {
                    'device_type': 'cisco_nxos',
                    'ip': IP,
                    'username': username,
                    'password': password
                    }
                ssh_conn = ConnectHandler(**NXOS)
                push_config(ssh_conn)
        else:
            print("You haven't entered a correct OS within the Devices file")

    except Exception as ValueError:
        print(ValueError)

def push_config(ssh_conn):

    cmdList = (get_commands(cmdFilename))
    try:
        for CMD in cmdList:
            result = ssh_conn.send_config_set(CMD)
            device_output(result)
    except Exception as ValueError:
        print(ValueError)

def device_output(result):
    try:
        outputFile = open(outputFilename, 'a')
        outputFile.write(result + '\n')
        outputFile.write('*' * 50 + '\n')
    except Exception as ValueError:
        print(ValueError)
    return

def main():
    get_commands(cmdFilename)
    get_devices(deviceFilename)
    device_dict(deviceFilename,username,password)
    print('Script Completed')

if __name__ == '__main__':
    main()





