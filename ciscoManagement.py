'''
Date Modified: 2017-3-20
Author: Billy Downing
Purpose: Take inputs in order to log
into several devices, run an exec/config command,
and output the results to a file.
'''


import os #not yet used. 
import getpass
from netmiko import ConnectHandler

cmdFilename = input('Enter Source Filename - Commands: ')
deviceFilename = input('Enter Source Filename - Devices: ')
outputFilename = input('Enter Destination Filename: ')
username = input('Username: ')
password = getpass.getpass(prompt='Password: ', stream=None)

'''
Function to generate a list based on commands found in a text file within the same directory. Need to make this
dynamic for use of config files from anywhere. 
'''
def get_commands(cmdFilename):
    with open(cmdFilename, 'r') as cmd:
        cmdLines = cmd.read()
        cmdList = cmdLines.split('\n')
    return cmdList

#Function to generate list of devices from a text file, easy to pull from csv listing line by line
def get_devices(deviceFilename):
    with open(deviceFilename, 'r') as deviceIP:
        deviceIPLines = deviceIP.read()
        deviceIPList = deviceIPLines.split('\n')
    return deviceIPList

#Function to build device dictionary for Netmiko, also calls get_devices and push_config
def device_dict(deviceFilename,username,password):
    #calls get_devices to obtain list of device IP's
    ipAddressList = (get_devices(deviceFilename))
    try:
        devtype = ipAddressList[0].lower()
        if devtype in ("cisco_asa", "ios", "cisco_nxos"):
            ipAddressList.remove(ipAddressList[0]) #Using the first line in the device doc to dictate the OS, then remove it - Find better way

            for IP in ipAddressList:
                cisco = {
                    'device_type': devtype,
                    'ip': IP,
                    'username': username,
                    'password': password
                }
            ssh_conn = ConnectHandler(**cisco)
            push_config(ssh_conn)
        else:
            print("You haven't entered a correct OS within the Devices file")

    except Exception as ValueError:
        print(ValueError)

'''        
Function is called by device_dict. Calls get_commands to obtain list, then uses already established ssh socket to run commands
Need to incorporate more dynamic way or determining if the command is needed to be ran in config or exec mode. Currenlty either
'exex' or 'config' needs to be written atop the command list doc
'''
def push_config(ssh_conn):
    cmdList = (get_commands(cmdFilename))
    
    if (cmdList[0].lower()) == 'config':
        cmdList.remove(cmdList[0])
        result = ssh_conn.send_config_set(cmdList)
        device_output(result)
        
    elif (cmdList[0].lower()) == 'exec':
        cmdList.remove(cmdList[0])
        
        for cmd in cmdList:
            result = ssh_conn.send_command_expect(cmd)
            device_output(result)

#Function to send config or output to a file. More so to confirm the config I'm putting in each device
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
