#### Imports ####
import tkinter as tk
import subprocess
import ast
import os

#### MISC Global Variables ####
SELECTED_ROUTER = {}
CWD = os.getcwd()

#### Initialize tkinter
root = tk.Tk()
root.title("Tiks")
root.geometry("800x370")
app = tk.Frame(root)
app.grid()


#### Initialize Label Frames ####
routerListbox = tk.Listbox(app)
routerListbox.grid(row="0", column="0", sticky=tk.E+tk.W+tk.N+tk.S, padx="2", pady="2")
routerListbox.configure(borderwidth="3")

action_LabelFrame = tk.LabelFrame(app)
action_LabelFrame.grid(row="0", column="1", sticky=tk.E+tk.W+tk.N+tk.S, padx="2", pady="2")
action_LabelFrame.configure(borderwidth="0")

manage_LabelFrame = tk.LabelFrame(app)
manage_LabelFrame.grid(row="1", column="0", sticky=tk.E+tk.W+tk.N+tk.S, padx="2", pady="2")
manage_LabelFrame.configure(borderwidth="0")

appControl_LabelFrame = tk.LabelFrame(app)
appControl_LabelFrame.grid(row="1", column="1", sticky=tk.E+tk.W+tk.N+tk.S, padx="2", pady="2")
appControl_LabelFrame.configure(borderwidth="0")

#### Configure Router Listbox ####
routerListbox.configure(height="20")
routerListbox.configure(width="80")

def LoadRouterListbox():
    routerListbox.delete(0, tk.END)

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
                ip, username, id_file = line.split(",")
                hosts[ip] = {
                "ip":ip,
                "username":username,
                "id_file":id_file
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
def Btn1():
    SetPassword()
def Btn2():
    BatchSetPassword()
def Btn3():
    pass
def Btn4():
    pass
def Btn5():
    pass

def BtnAdd():
    AddRouter()
def BtnRemove():
    pass
def BtnSearch():
    pass

def BtnAbout():
    pass
def BtnQuit():
    root.quit()

#### Add elements to Label Frames ####

# Manage Label Frame
btnAdd = tk.Button(manage_LabelFrame, command=BtnAdd)
btnRemove = tk.Button(manage_LabelFrame, command=BtnRemove)
btnSearch = tk.Button(manage_LabelFrame, command=BtnSearch)

btnAdd.grid(row="0", column="0")
btnRemove.grid(row="0", column="1")
btnSearch.grid(row="0", column="2")

btnAdd["text"] = "Add"
btnRemove["text"] = "Remove"
btnSearch["text"] = "Search"


# Action Label Frame

### ** Button Template ** ###
# btn5 = tk.Button(action_LabelFrame, command=Btn5)
# btn5.grid(row="5", column="0")
# btn5.configure(width="14")
# btn5["text"] = "5"

btn0 = tk.Button(action_LabelFrame, command=Btn0)
btn1 = tk.Button(action_LabelFrame, command=Btn1)
btn2 = tk.Button(action_LabelFrame, command=Btn2)
btn3 = tk.Button(action_LabelFrame, command=Btn3)
btn4 = tk.Button(action_LabelFrame, command=Btn4)
btn5 = tk.Button(action_LabelFrame, command=Btn5)

btn0.grid(row="0", column="0")
btn1.grid(row="1", column="0")
btn2.grid(row="2", column="0")
btn3.grid(row="3", column="0")
btn4.grid(row="4", column="0")
btn5.grid(row="5", column="0")

btn0.configure(width="14")
btn1.configure(width="14")
btn2.configure(width="14")
btn3.configure(width="14")
btn4.configure(width="14")
btn5.configure(width="14")

btn0["text"] = "Identity"
btn1["text"] = "Set Password -single"
btn2["text"] = "Set Password -batch"
btn3["text"] = "3"
btn4["text"] = "4"
btn5["text"] = "5"


# App Control Label Frame
btnAbout = tk.Button(appControl_LabelFrame, command=BtnAbout)
btnQuit = tk.Button(appControl_LabelFrame, command=BtnQuit)

btnAbout.grid(row="0", column="0")
btnQuit.grid(row="0", column="1")

btnAbout.configure(width="5")
btnQuit.configure(width="5")

btnAbout["text"] = "About"
btnQuit["text"] = "Quit"



def BasicOutput(output):
    global childWindow
    childWindow = tk.Toplevel()
    childWindow.title("Output")

    childApp = tk.Frame(childWindow)
    childApp.grid()

    labelRemoteHost = tk.Label(childApp, text="Output:")
    labelRemoteHost.grid(row="0", column="0", sticky=tk.E+tk.W+tk.N+tk.S)

    textOutput = tk.Text(childApp)
    textOutput.grid(row="1", column="0", sticky=tk.E+tk.W+tk.N+tk.S)
    textOutput.configure(width="80", height="12")

    textOutput.insert(tk.END, output)
    textOutput.config(state=tk.DISABLED)
def GetIdentity():
    global SELECTED_ROUTER
    SELECTED_ROUTER = ast.literal_eval(routerListbox.get(tk.ACTIVE))

    pr = subprocess.Popen([ 'scripts/shell_scripts.sh', 'identity', SELECTED_ROUTER["ip"], SELECTED_ROUTER["username"], CWD + "/identity_files/" + SELECTED_ROUTER["id_file"] ],stdout=subprocess.PIPE)
    output = str(pr.stdout.read(), encoding='utf-8').replace("\r", "")

    BasicOutput(output)

def SetPassword_Submit():
    global SELECTED_ROUTER
    SELECTED_ROUTER = ast.literal_eval(routerListbox.get(tk.ACTIVE))

    print('scripts/shell_scripts.sh', 'change_pass', SELECTED_ROUTER["ip"], SELECTED_ROUTER["username"], "./identity_files/" + SELECTED_ROUTER["id_file"], entryUsername.get(), entryPassword.get())
    print(entryUsername.get(), entryPassword.get())

    pr = subprocess.Popen([ 'scripts/shell_scripts.sh', 'change_pass', SELECTED_ROUTER["ip"], SELECTED_ROUTER["username"], "./identity_files/" + SELECTED_ROUTER["id_file"], entryUsername.get(), entryPassword.get() ],stdout=subprocess.PIPE)


    childWindow.destroy()
def SetPassword_Cancel():
    childWindow.destroy()
def SetPassword():

    global childWindow
    childWindow = tk.Toplevel()
    childWindow.title("Update User Password")

    childApp = tk.Frame(childWindow)
    childApp.grid()
    global SELECTED_ROUTER
    SELECTED_ROUTER = ast.literal_eval(routerListbox.get(tk.ACTIVE))

    # labelHeading = tk.Label(childApp, text="Update User Password:")
    # labelHeading.grid(row="0", column="0", sticky=tk.E+tk.W+tk.N+tk.S, columnspan="2")

    labelRemoteHost = tk.Label(childApp, text="Router:")
    labelRemoteHost.grid(row="1", column="0", sticky=tk.E+tk.W+tk.N+tk.S)

    labelIP = tk.Label(childApp, text=SELECTED_ROUTER["ip"])
    labelIP.grid(row="1", column="1", sticky=tk.E+tk.W+tk.N+tk.S)

    labelUsername = tk.Label(childApp, text="Username:")
    labelUsername.grid(row="2", column="0", sticky=tk.E+tk.W+tk.N+tk.S)

    global entryUsername
    entryUsername = tk.Entry(childApp)
    entryUsername.grid(row="2", column="1", sticky=tk.E+tk.W+tk.N+tk.S)
    entryUsername.configure(width="30")

    labelPassword = tk.Label(childApp, text="Password:")
    labelPassword.grid(row="3", column="0", sticky=tk.E+tk.W+tk.N+tk.S)

    global entryPassword
    entryPassword = tk.Entry(childApp)
    entryPassword.grid(row="3", column="1", sticky=tk.E+tk.W+tk.N+tk.S)
    entryPassword.configure(width="30")

    btnSetPasswordSubmit = tk.Button(childApp, command=SetPassword_Submit)
    btnSetPasswordSubmit.grid(row="4", column="0", columnspan="2", sticky=tk.E+tk.W+tk.N+tk.S)
    btnSetPasswordSubmit.configure(width="19")
    btnSetPasswordSubmit["text"] = "Submit"


    btnSetPasswordCancel = tk.Button(childApp, command=SetPassword_Cancel)
    btnSetPasswordCancel.grid(row="5", column="0", columnspan="2", sticky=tk.E+tk.W+tk.N+tk.S)
    btnSetPasswordCancel.configure(width="19")
    btnSetPasswordCancel["text"] = "Cancel"


def AddRouter_Submit():
    ip=entryRouter.get()
    username=entryUsername.get()
    id_file=entryIDFile.get()

    hosts[ip] = {
    "ip":ip,
    "username":username,
    "id_file":id_file
    }
    print(hosts)

    s = "# Syntax: [host ip],[username],[identity file]\n"
    for host in hosts:
        s = s + hosts[host]["ip"] + "," + hosts[host]["username"] + "," + hosts[host]["id_file"] + "\n"

    f = open("hosts_config", "w")
    f.write(s)
    f.close()

    LoadRouterListbox()
    childWindow.destroy()
def AddRouter_Cancel():
    childWindow.destroy()
def AddRouter():
    global childWindow
    global SELECTED_ROUTER

    childWindow = tk.Toplevel()
    childWindow.title("Add Router")

    childApp = tk.Frame(childWindow)
    childApp.grid()
    SELECTED_ROUTER = ast.literal_eval(routerListbox.get(tk.ACTIVE))

    labelRouterIP = tk.Label(childApp, text="Router IP:")
    labelRouterIP.grid(row="1", column="0", sticky=tk.E+tk.W+tk.N+tk.S)

    global entryRouter
    entryRouter = tk.Entry(childApp)
    entryRouter.grid(row="1", column="1", columnspan="2", sticky=tk.E+tk.W+tk.N+tk.S)
    entryRouter.configure(width="30")

    labelUsername = tk.Label(childApp, text="Username:")
    labelUsername.grid(row="2", column="0", sticky=tk.E+tk.W+tk.N+tk.S)

    global entryUsername
    entryUsername = tk.Entry(childApp)
    entryUsername.grid(row="2", column="1", columnspan="2", sticky=tk.E+tk.W+tk.N+tk.S)
    entryUsername.configure(width="30")

    labelIDFile = tk.Label(childApp, text="ID File:")
    labelIDFile.grid(row="3", column="0", sticky=tk.E+tk.W+tk.N+tk.S)

    global entryIDFile
    entryIDFile = tk.Entry(childApp)
    entryIDFile.grid(row="3", column="1", columnspan="2", sticky=tk.E+tk.W+tk.N+tk.S)
    entryIDFile.configure(width="30")

    btnSetPasswordSubmit = tk.Button(childApp, command=AddRouter_Submit)
    btnSetPasswordSubmit.grid(row="4", column="1", sticky=tk.E+tk.W+tk.N+tk.S)
    btnSetPasswordSubmit["text"] = "Submit"

    btnSetPasswordCancel = tk.Button(childApp, command=AddRouter_Cancel)
    btnSetPasswordCancel.grid(row="4", column="2",sticky=tk.E+tk.W+tk.N+tk.S)
    btnSetPasswordCancel["text"] = "Cancel"


def Load_ListboxBatchPass():
    listboxBatchPass.delete(0, tk.END)

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
                ip, username, id_file = line.split(",")
                hosts[ip] = {
                "ip":ip,
                "username":username,
                "id_file":id_file
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

    un=entryBatchUsername.get()
    pw=entryBatchPassword.get()

    listboxBatchPass.focus_set()
    CURSELECTION = listboxBatchPass.curselection()
    hostsToUpdate = {}

    print(un,pw, CURSELECTION)

    for num in range(listboxBatchPass.size()):
        if listboxBatchPass.selection_includes(num):
            host = ast.literal_eval(listboxBatchPass.get(num))
            hostsToUpdate[host["ip"]] = host
            print('scripts/shell_scripts.sh', 'change_pass', host["ip"], host["username"], "./identity_files/" + host["id_file"], un, pw)
            pr = subprocess.Popen([ 'scripts/shell_scripts.sh', 'change_pass', host["ip"], host["username"], "./identity_files/" + host["id_file"], un, pw ], stdout=subprocess.PIPE)

    print(hostsToUpdate)


    childWindow.destroy()


def BatchSetPassword_Cancel():
    childWindow.destroy()

def BatchSetPassword():
    global childWindow
    global SELECTED_ROUTER

    childWindow = tk.Toplevel()
    childWindow.title("Batch Password Changer")

    childApp = tk.Frame(childWindow)
    childApp.grid()
    SELECTED_ROUTER = ast.literal_eval(routerListbox.get(tk.ACTIVE))

    global listboxBatchPass
    listboxBatchPass = tk.Listbox(childApp)
    listboxBatchPass.grid(row="0", column="0", columnspan="3", sticky=tk.E+tk.W+tk.N+tk.S, padx="2", pady="2")
    listboxBatchPass.configure(borderwidth="3", width="80", selectmode=tk.EXTENDED)
    Load_ListboxBatchPass()

    labelBatchUsername = tk.Label(childApp, text="Username:")
    labelBatchUsername.grid(row="1", column="0", sticky=tk.E+tk.W+tk.N+tk.S)

    global entryBatchUsername
    entryBatchUsername = tk.Entry(childApp)
    entryBatchUsername.grid(row="1", column="1", columnspan="3", sticky=tk.E+tk.W+tk.N+tk.S)
    entryBatchUsername.configure(width="30")

    labelBatchPass = tk.Label(childApp, text="New Password:")
    labelBatchPass.grid(row="2", column="0", sticky=tk.E+tk.W+tk.N+tk.S)

    global entryBatchPassword
    entryBatchPassword = tk.Entry(childApp)
    entryBatchPassword.grid(row="2", column="1", columnspan="3", sticky=tk.E+tk.W+tk.N+tk.S)
    entryBatchPassword.configure(width="30")

    btnBatchSetPasswordSubmit = tk.Button(childApp, command=BatchSetPassword_Submit)
    btnBatchSetPasswordSubmit.grid(row="3", column="1", sticky=tk.E+tk.W+tk.N+tk.S)
    btnBatchSetPasswordSubmit["text"] = "Submit"

    btnBatchSetPasswordCancel = tk.Button(childApp, command=BatchSetPassword_Cancel)
    btnBatchSetPasswordCancel.grid(row="3", column="2",sticky=tk.E+tk.W+tk.N+tk.S)
    btnBatchSetPasswordCancel["text"] = "Cancel"








root.mainloop()
