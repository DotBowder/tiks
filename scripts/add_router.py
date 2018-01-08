#### Imports ####
import tkinter as tk
from tkinter import *
import subprocess
import ast
import os

CWD = os.getcwd()

#### Initialize tkinter
root = Tk()
root.title("Add Router")
# root.geometry("800x370")
mainWindow = Frame(root)
mainWindow.grid()



def AddRouter_GenerateIDFile():
    ip=entryRouter.get()

    print(ip)
    print('ssh-keygen', '-v', '-t', 'rsa', '-b', '2048', '-N', '', '-f', '{}/identity_files/{}_rsa_2048'.format(CWD,ip))
    pr_lsID = subprocess.Popen([ 'ls', '{}/identity_files/'.format(CWD) ], stdout=subprocess.PIPE)
    exists = False
    for line in pr_lsID.stdout:
        l = line.decode("utf-8").split("\n")[0]
        if l == "{}_rsa_2048".format(ip):
            exists = True
    if exists:
        pr_acceptOverwrite = subprocess.Popen(['echo', '-e', 'y\n'], stdout=subprocess.PIPE)
        pr_generateID = subprocess.Popen([ 'ssh-keygen', '-t', 'rsa', '-b', '2048', '-N', '', '-f', '{}/identity_files/{}_rsa_2048'.format(CWD,ip) ], stdin=pr_acceptOverwrite.stdout)
    else:
        pr_generateID = subprocess.Popen([ 'ssh-keygen', '-t', 'rsa', '-b', '2048', '-N', '', '-f', '{}/identity_files/{}_rsa_2048'.format(CWD,ip) ])
    entryIDFileText.set("{}_rsa_2048".format(ip))


def Load_RouterList():
    #### Load Known Hosts ####
    f = open("hosts_config", "r")
    lines = f.read().split("\n")
    f.close()

    global hosts
    hosts = {}

    for line in lines:
        if line.startswith("#") or line == "":
            pass
        else:
            try:
                ip, username, id_file, custom = line.split(",")
                hosts[ip] = {
                "ip":ip,
                "username":username,
                "id_file":id_file,
                "custom":custom
                }
            except:
                pass

def AddRouter_Submit():
    ip=entryRouter.get()
    username=entryUsername.get()
    id_file=entryIDFile.get()
    custom=entryCustom.get()

    Load_RouterList()
    global hosts
    hosts[ip] = {
    "ip":ip,
    "username":username,
    "id_file":id_file,
    "custom":custom
    }
    print(hosts)

    s = "# Syntax: [host ip],[username],[identity file],[custom]\n"
    for host in hosts:
        s = s + hosts[host]["ip"] + "," + hosts[host]["username"] + "," + hosts[host]["id_file"] + "," + hosts[host]["custom"] + "\n"

    f = open("hosts_config", "w")
    f.write(s)
    f.close()
    print(s)
    # pr = subprocess.Popen([ 'scripts/shell_scripts.sh', 'identity', SELECTED_ROUTER["ip"], SELECTED_ROUTER["username"], CWD + "/identity_files/" + SELECTED_ROUTER["id_file"] ],stdout=subprocess.PIPE)
    # output = str(pr.stdout.read(), encoding='utf-8').replace("\r", "")

    root.quit()

def AddRouter_Cancel():
    root.quit()

labelRouterIP = Label(mainWindow, text="Router IP:")
labelRouterIP.grid(row="1", column="0", sticky=E+W+N+S)

entryRouter = Entry(mainWindow)
entryRouter.grid(row="1", column="1", columnspan="3", sticky=E+W+N+S)
entryRouter.configure(width="30")

labelUsername = Label(mainWindow, text="Username:")
labelUsername.grid(row="2", column="0", sticky=E+W+N+S)

entryUsername = Entry(mainWindow)
entryUsername.grid(row="2", column="1", columnspan="3", sticky=E+W+N+S)
entryUsername.configure(width="30")

labelIDFile = Label(mainWindow, text="ID File:")
labelIDFile.grid(row="3", column="0", sticky=E+W+N+S)

entryIDFileText = StringVar()
entryIDFile = Entry(mainWindow, textvariable=entryIDFileText)
entryIDFile.grid(row="3", column="1", columnspan="2", sticky=E+W+N+S)
entryIDFile.configure(width="30")

btnIDFileGen = Button(mainWindow, text="Generate", command=AddRouter_GenerateIDFile)
btnIDFileGen.grid(row="3", column="3", sticky=E+W+N+S)
btnIDFileGen.configure(pady="1")


labelCustom= Label(mainWindow, text="Custom:")
labelCustom.grid(row="4", column="0", sticky=E+W+N+S)

entryCustom = Entry(mainWindow)
entryCustom.grid(row="4", column="1", columnspan="3", sticky=E+W+N+S)
entryCustom.configure(width="30")

btnSetPasswordSubmit = Button(mainWindow, text="Submit",command=AddRouter_Submit)
btnSetPasswordSubmit.grid(row="5", column="0", columnspan="2", sticky=E+W+N+S)

btnSetPasswordCancel = Button(mainWindow, text="Cancel", command=AddRouter_Cancel)
btnSetPasswordCancel.grid(row="5", column="2", columnspan="2", sticky=E+W+N+S)




root.mainloop()
