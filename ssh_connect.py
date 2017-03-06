'''
Date Modified: 2017-3-6
Author: Billy Downing
Purpose: Generates GUI to take inputs in order to log
into several devices, run a command, and output the
results to a file in a user created directory.
'''

from netmiko import ConnectHandler
from tkinter import *
import os

class Connect:

    def sshConnect():

        #Variable manipulation
        ip = ipAddress.get()
        cmd = command.get()
        #cmdList = cmd.split('\n')
        #cmdLen = len(cmdList)
        ipAddressList = ip.split(',')
        ipAddressLen = len(ipAddressList)

        # Navigate create new directory & Navigate to it
        os.chdir(mkdir.get())

        # create new file, might not need this
        textoutput = open(mkfile.get(), 'w')

        #loop to iterate through each IP within the list
        for i in range(ipAddressLen):
            try:
                if osText.get() == ('asa' or 'ASA'):
                    ASA = {
                        'device_type': 'cisco_asa',
                        'ip': ipAddressList[i],
                        'username': userName.get(),
                        'password': passWord.get(),
                    }
                    ssh_conn = ConnectHandler(**ASA)

                    output1 = ssh_conn.send_command_expect(cmd)
                    output2 = ssh_conn.send_command_expect('show hostname')
                    textoutput = open(mkfile.get(), 'a')
                    textoutput.write('----------\n')
                    textoutput.write(output2 + ' ' + ipAddressList[i])
                    textoutput.write('\n')
                    textoutput.write(output1)
                
                elif osText.get() == ('ios' or 'IOS'):
                    IOS = {
                        'device_type': 'cisco_ios',
                        'ip': ipAddressList[i],
                        'username': userName.get(),
                        'password': passWord.get(),
                    }
                    ssh_conn = ConnectHandler(**IOS)

                    output1 = ssh_conn.send_command_expect(cmd)
                    output2 = ssh_conn.send_command_expect("show run | in hostname")
                    textoutput = open(mkfile.get(), 'a')
                    textoutput.write('----------\n')
                    textoutput.write(output2 + ' ' + ipAddressList[i])
                    textoutput.write('\n')
                    textoutput.write(output1)
                    textoutput.write('\n----------')
                
                elif osText.get() == ('nxos' or 'NXOS'):
                    NXOS = {
                        'device_type': 'cisco_nxos',
                        'ip': ipAddressList[i],
                        'username': userName.get(),
                        'password': passWord.get(),
                    }
                    ssh_conn = ConnectHandler(**NXOS)

                    output1 = ssh_conn.send_command_expect(cmd)
                    output2 = ssh_conn.send_command_expect("show run | in hostname")
                    textoutput = open(mkfile.get(), 'a')
                    textoutput.write('----------\n')
                    textoutput.write(output2 + ' ' + ipAddressList[i])
                    textoutput.write('\n')
                    textoutput.write(output1)
                    textoutput.write('\n----------')
                
                else:
                    errorLabel.config(text="You've Entered an Incorrect OS")
            
            except Exception as ValueError:
                print(ValueError)
                textoutput.write('#########--' + str(ValueError) + ipAddressList[i] + '--#########')
                textoutput.write('\n')

    def tkinterGui():
        """TKinter GUI for Variable Input"""

        # Create window for credentials
        window = Tk(className='Credentials')
        window.geometry('400x400')
        window.configure(background='#A09897')

        # Create label for username entry
        global userName
        userLabel = Label(window, text='Username: ')
        userLabel.configure(background='#A09897')
        userLabel.pack()
        userName = Entry(window, bd=1)
        userName.pack()

        # create label for password entry
        global passWord
        passwordLabel = Label(window, text='Password: ')
        passwordLabel.configure(background='#A09897')
        passwordLabel.pack()
        passWord = Entry(window, bd=1, show="*")
        passWord.pack()

        # create label for IP address entry
        global ipAddress
        ipLabel = Label(window, text='IP: ')
        ipLabel.configure(background='#A09897')
        ipLabel.pack()
        ipAddress = Entry(window, bd=1)
        ipAddress.pack()

        # create label for OS
        global osText
        osLabel = Label(window, text='OS(ios/asa/nxos): ')
        osLabel.configure(background='#A09897')
        osLabel.pack()
        osText = Entry(window, bd=1)
        osText.pack()

        # create label for Command
        global command
        commandLabel = Label(window, text='Command: ')
        test = Label()
        commandLabel.configure(background='#A09897')
        commandLabel.pack()
        command = Entry(window, bd=1)
        command.pack()

        # Create file location
        global mkdir
        mkdirLabel = Label(window, text='Destination File Location: ')
        mkdirLabel.configure(background='#A09897')
        mkdirLabel.pack()
        mkdir = Entry(window, bd=1)
        mkdir.pack()

        # create new file for output
        global mkfile
        mkfileLabel = Label(window, text='Destination File Name: ')
        mkfileLabel.configure(background='#A09897')
        mkfileLabel.pack()
        mkfile = Entry(window, bd=1)
        mkfile.pack()

        button = Button(window, text='Submit', command=Connect.sshConnect)
        button.pack()

        # Error field
        global errorLabel
        errorLabel = Label(window, text='')
        errorLabel.configure(background='#A09897')
        errorLabel.pack()

        window.mainloop()

Connect.tkinterGui()
