#### Imports ####
import tkinter as tk
from tkinter import *
import subprocess
import ast
import os

#### MISC Global Variables ####
SELECTED_ROUTER = {}
CWD = os.getcwd()

#### Initialize tkinter
root = Tk()
root.title("Tiks")
app = Frame(root)
app.grid()


#### Initialize Label Frames ####
labelRouters = Label(app, text="Router List: {}/hosts_config".format(CWD))
labelRouters.grid(row="0", column="0", sticky=W, padx="2", pady="2")

routerListbox = Listbox(app, exportselection=False)
routerListbox.grid(row="1", column="0", sticky=E+W+N+S, padx="2", pady="2")
routerListbox.configure(borderwidth="3")

action_LabelFrame = LabelFrame(app, text="Actions", labelanchor=N)
action_LabelFrame.grid(row="0", column="1", rowspan="2", sticky=E+W+N+S, padx="2", pady="2")
action_LabelFrame.configure(borderwidth="2")

manage_LabelFrame = LabelFrame(app)
manage_LabelFrame.grid(row="2", column="0", sticky=E+W+N+S, padx="2", pady="2")
manage_LabelFrame.configure(borderwidth="0")

appControl_LabelFrame = LabelFrame(app)
appControl_LabelFrame.grid(row="2", column="1", sticky=E+W+N+S, padx="2", pady="2")
appControl_LabelFrame.configure(borderwidth="0")

#### Configure Router Listbox ####
routerListbox.configure(height="20")
routerListbox.configure(width="80")

def LoadRouterListbox():
    routerListbox.delete(0, END)

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
        routerListbox.insert(0, hosts[host])
        # routerListbox.insert(0, "IP: {}      Username: {}     Key: {}".format(hosts[host]["ip"],hosts[host]["username"],hosts[host]["id_file"]))
    routerListbox.activate(0)

LoadRouterListbox()

#### Create Button Callbacks ####
def Btn0():
    GetIdentity()
def btnBatchPassUtil():
    pr_batch_set_password = subprocess.Popen([ 'python3', 'scripts/batch_set_password.py' ], stdout=subprocess.PIPE)
def Btn3():
    pass
def Btn4():
    pass
def BtnBatchPassUtilSalted():
    pr_batch_set_password = subprocess.Popen([ 'python3', 'scripts/batch_set_password_salted.py' ])

def BtnAdd():
    pr_add_router = subprocess.Popen([ 'python3', 'scripts/add_router.py' ])
    while pr_add_router.poll() == None:
        pass
    LoadRouterListbox()
def BtnRemove():
    global SELECTED_ROUTER
    SELECTED_ROUTER = ast.literal_eval(routerListbox.get(ACTIVE))

    s = "# Syntax: [host ip],[username],[identity file],[custom]\n# Lines beginning with # will be ignored.\n"

    for host in hosts:
        if hosts[host]["ip"] == SELECTED_ROUTER["ip"]:
            pr_removeID = subprocess.Popen([ 'rm', 'identity_files/{}_rsa_2048'.format(SELECTED_ROUTER["ip"]) ])
            pr_removeIDPUB = subprocess.Popen([ 'rm', 'identity_files/{}_rsa_2048.pub'.format(SELECTED_ROUTER["ip"]) ])
        else:
            s = s + hosts[host]["ip"] + "," + hosts[host]["username"] + "," + hosts[host]["id_file"] + "," + hosts[host]["custom"] + "\n"

    f = open("hosts_config", "w")
    f.write(s)
    f.close()
    print(s)

    LoadRouterListbox()

def BtnSearch():
    pass

def BtnAbout():
    pr_batch_set_password = subprocess.Popen([ 'python3', 'scripts/about.py' ])
def BtnQuit():
    root.quit()

#### Add elements to Label Frames ####

# Manage Label Frame
btnAdd = Button(manage_LabelFrame, command=BtnAdd)
btnRemove = Button(manage_LabelFrame, command=BtnRemove)
btnSearch = Button(manage_LabelFrame, command=BtnSearch)

btnAdd.grid(row="0", column="0", sticky=E+W+N+S)
btnRemove.grid(row="0", column="1", sticky=E+W+N+S)
btnSearch.grid(row="0", column="2", sticky=E+W+N+S)

btnAdd["text"] = "Add"
btnRemove["text"] = "Remove"
btnSearch["text"] = "Search"



# Action Label Frame
# btn0 = Button(action_LabelFrame, text="0", command=Btn0)
# btn0.grid(row="0", column="0", sticky=E+W+N+S)
# btn0.configure(width="14")
#
# btn3 = Button(action_LabelFrame, text="3", command=Btn3)
# btn3.grid(row="3", column="0", sticky=E+W+N+S)
# btn3.configure(width="14")
#
# btn4 = Button(action_LabelFrame, text="4", command=Btn4)
# btn4.grid(row="4", column="0", sticky=E+W+N+S)
# btn4.configure(width="14")

btnBatchPassUtilSalted = Button(action_LabelFrame, text="Set Password Salted", command=BtnBatchPassUtilSalted)
btnBatchPassUtilSalted.grid(row="5", column="0", sticky=E+W+N+S)
btnBatchPassUtilSalted.configure(width="14")

btnBatchPassUtil = Button(action_LabelFrame, text="Set Password", command=btnBatchPassUtil)
btnBatchPassUtil.grid(row="6", column="0", sticky=E+W+N+S)
btnBatchPassUtil.configure(width="14")

# App Control Label Frame
btnAbout = Button(appControl_LabelFrame, command=BtnAbout)
btnQuit = Button(appControl_LabelFrame, command=BtnQuit)

btnAbout.grid(row="0", column="0")
btnQuit.grid(row="0", column="1")

btnAbout.configure(width="5")
btnQuit.configure(width="5")

btnAbout["text"] = "About"
btnQuit["text"] = "Quit"



def BasicOutput(output):
    global childWindow
    childWindow = Toplevel()
    childWindow.title("Output")

    childApp = Frame(childWindow)
    childApp.grid()

    labelRemoteHost = Label(childApp, text="Output:")
    labelRemoteHost.grid(row="0", column="0", sticky=E+W+N+S)

    textOutput = Text(childApp)
    textOutput.grid(row="1", column="0", sticky=E+W+N+S)
    textOutput.configure(width="80", height="12")

    textOutput.insert(END, output)
    textOutput.config(state=DISABLED)

def GetIdentity():
    global SELECTED_ROUTER
    SELECTED_ROUTER = ast.literal_eval(routerListbox.get(ACTIVE))

    pr = subprocess.Popen([ 'scripts/shell_scripts.sh', 'identity', SELECTED_ROUTER["ip"], SELECTED_ROUTER["username"], CWD + "/identity_files/" + SELECTED_ROUTER["id_file"] ],stdout=subprocess.PIPE)
    output = str(pr.stdout.read(), encoding='utf-8').replace("\r", "")

    BasicOutput(output)





root.mainloop()
