#### Imports ####
import tkinter as tk
from tkinter import *
import subprocess
import ast
import os

#### Initialize tkinter
root = Tk()
root.title("Batch Password Changer (Salted)")
# root.geometry("800x370")
mainWindow = Frame(root)
mainWindow.grid()


def Load_ListboxBatchPass():
    listboxBatchPass.delete(0, END)

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

    # print(hosts)


    ####  Inject hosts into Router Listbox ####
    for host in hosts:
        listboxBatchPass.insert(0, hosts[host])
        # routerListbox.insert(0, "IP: {}      Username: {}     Key: {}".format(hosts[host]["ip"],hosts[host]["username"],hosts[host]["id_file"]))
    listboxBatchPass.activate(0)

def BatchSetPassword_Submit():
    # SELECTED_ROUTER = ast.literal_eval(listboxBatchPass.get(ACTIVE))

    un=entryBatchUsername.get()
    pw_A=entryBatchPassword_A.get()
    pw_B=entryBatchPassword_B.get()

    listboxBatchPass.focus_set()
    CURSELECTION = listboxBatchPass.curselection()
    hostsToUpdate = {}


    for num in range(listboxBatchPass.size()):
        if listboxBatchPass.selection_includes(num):
            try:
                host = ast.literal_eval(listboxBatchPass.get(num))
                pw = pw_A + host["custom"] + pw_B
                hostsToUpdate[host["ip"]] = host
                print(pw)

                print('scripts/shell_scripts.sh', 'change_pass', host["ip"], host["username"], "./identity_files/" + host["id_file"], un, pw)
                pr = subprocess.Popen([ 'scripts/shell_scripts.sh', 'change_pass', host["ip"], host["username"], "./identity_files/" + host["id_file"], un, pw ], stdout=subprocess.PIPE)
            except:
                print('Failed to .')

    print(hostsToUpdate)

    root.quit()

def BatchSetPassword_Cancel():
    root.quit()






labelInfo0 = Label(mainWindow, text="Select desired routers to update a user account password.")
labelInfo0.grid(row="0", column="0", columnspan="4")

listboxBatchPass = Listbox(mainWindow, exportselection=False)
listboxBatchPass.grid(row="1", column="0", columnspan="4", sticky=E+W+N+S, padx="2", pady="2")
listboxBatchPass.configure(borderwidth="3", width="80", selectmode=EXTENDED)
Load_ListboxBatchPass()

labelInfo1 = Label(mainWindow, text="The password will be salted using the 'custom' property in hosts_config. This property will be\n injected between Password Part A, and Password Part B.  ( Password = [Part A][custom][Part B] )")
labelInfo1.grid(row="2", column="0", columnspan="4")

labelBatchUsername = Label(mainWindow, text="Username:")
labelBatchUsername.grid(row="3", column="0")

entryBatchUsername = Entry(mainWindow)
entryBatchUsername.grid(row="3", column="1", columnspan="3", sticky=E+W+N+S)
entryBatchUsername.configure(width="30")

labelBatchPass = Label(mainWindow, text="Password Part A:")
labelBatchPass.grid(row="4", column="0")

entryBatchPassword_A = Entry(mainWindow)
entryBatchPassword_A.grid(row="4", column="1", columnspan="3", sticky=E+W+N+S)
entryBatchPassword_A.configure(width="30")

labelBatchPassword_B = Label(mainWindow, text="Password Part B:")
labelBatchPassword_B.grid(row="6", column="0")

entryBatchPassword_B = Entry(mainWindow)
entryBatchPassword_B.grid(row="6", column="1", columnspan="3", sticky=E+W+N+S)
entryBatchPassword_B.configure(width="30")


btnBatchSetPasswordSubmit = Button(mainWindow, text="Submit", command=BatchSetPassword_Submit)
btnBatchSetPasswordSubmit.grid(row="7", column="2", columnspan="1", sticky=E+W+N+S)
btnBatchSetPasswordSubmit.configure(width="10")

btnBatchSetPasswordCancel = Button(mainWindow, text="Cancel", command=BatchSetPassword_Cancel)
btnBatchSetPasswordCancel.grid(row="7", column="3", columnspan="1", sticky=E+W+N+S)
btnBatchSetPasswordCancel.configure(width="10")
root.mainloop()
