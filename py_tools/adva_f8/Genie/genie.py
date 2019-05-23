import io
import os
import time
import tkMessageBox



try:
    from Tkinter import *
except:
    os.system('sudo yum -y install tkinter')
    from Tkinter import *

import copy

import communicator as cn

try:
    import yaml

except:
    try:
        os.system('pip install pyaml')
        print "installed pyaml"
        import yaml
    except:
        os.system('sudo yum -y install python-yaml')
        print "installed pyaml"
        import yaml


class Gui:
    # host="10.16.45.17"
    # username=""
    # password=""
    userdata = []
    modulechecks = []
    modules = []  # ['ecm','card5','card named 42','4','5','6extrawide!!!!!!!!!!','7']
    infoLabels = []
    srcList = ['Local system']

    # name=''+

    def updateOptions(self):
        m = self.option.children['menu']
        m.delete(0, END)
        names = [d['name'] for d in self.userdata]
        for val in names:
            m.add_command(label=val, command=lambda v=self.defvar, l=val: v.set(l))
        self.defvar.set(names[0])
        #print 'done'

    def userText(self, event):
        return
        #event.widget.delete(0, END)

    def getSelected(self):

        for i in self.userdata:
            if i['name'] == self.defvar.get():
                # print  'selected option: ' + str(i)
                return i

    def getSelectedBoxes(self):
        selected = []
        n = 0
        # print 'test'+str(self.modules)
        for i in self.modules:

            # import ipdb;ipdb.set_trace()
            #print 'selecting: ' + str(self.modulechecks[n][1])
            if self.modulechecks[n][1].get() == 1:
                selected.append(i)
            n += 1

        return selected

    def getSelectedBoxesIp(self):
        selected = []
        n = 0
        # print 'test'+str(self.modules)
        for i in self.modules:

            # import ipdb;ipdb.set_trace()
            if self.modulechecks[n][1].get() == 1:
                # print self.modules[i][0]
                selected.append(self.modules[i][0])
            n += 1

        return selected

    def connect(self, event):
        tmp = self.getSelected()

        self.refreshModules(tmp['host'])
        self.refreshLabels(tmp['host'])
        # self.comm.openSSHSession(host=tmp['host'],username=tmp['username'],password=tmp['password'],port=tmp['port'])

    def add(self, event):
        if self.ehost.get() != "Enter IP":
            name = self.name.get()
            username = self.user.get()
            password = self.passwd.get()
            port = self.port.get()
            if name == 'Connection name':
                name = 'Unnamed'
            if username == 'Enter username':
                username = 'admin'
            if password == 'Enter password':
                password = 'CHGME.1a'
            if port == 'Enter port':
                port = '22'

            entry = {'name': name + ' - ' + self.ehost.get(), 'username': username, 'password': password,
                     'host': self.ehost.get(), 'port': port}

            try:
                if self.userdata[0] == None:
                    self.userdata[0] = entry
                else:
                    for i in self.userdata:
                        if i == entry:
                            return
                    self.userdata.append(entry)
                print self.userdata
                self.updateOptions()
            except:
                self.userdata = [None]
                self.add(None)
        else:
            print 'not enough info given'
        with io.open('userdata.yaml', 'w', encoding='utf8') as outfile:
            yaml.dump(self.userdata, outfile, default_flow_style=False, allow_unicode=True)

    def readFile(self):

        with open("userdata.yaml", 'r') as stream:
            self.userdata = yaml.safe_load(stream)

    def saveData(self):
        with io.open('userdata.yaml', 'w', encoding='utf8') as outfile:
            yaml.dump(self.userdata, outfile, default_flow_style=False, allow_unicode=True)
        print 'saved'
        self.root.destroy()

    def ssh(self, event):
        tmp = self.getSelected()
        self.comm.openSSHSession(host=tmp['host'])

    def dte(self, event):
        tmp = self.getSelected()
        self.comm.openDTESession(host=tmp['host'])

    def telnet(self, event):
        tmp = self.getSelected()
        self.comm.openTelnetSession(host=tmp['host'])

    def changeConnection(self, value):
        print value
        print'test'

    def prepareFirst(self):
        w = Label(self.root, text="Genie", font=("Helvetica", 24), background='#959ba5', foreground='#bc0707').grid(
            row=0, column=0, columnspan=6)
        self.ehost = Entry(self.root, background='#959ba5')
        self.ehost.insert(0, "Enter IP")
        self.ehost.bind("<Button>", self.userText)
        self.ehost.grid(row=1, column=0)

        self.user = Entry(self.root, background='#959ba5')
        self.user.insert(0, "Enter username")
        self.user.bind("<Button>", self.userText)
        self.user.grid(row=1, column=1)

        self.passwd = Entry(self.root, show="*", background='#959ba5')
        self.passwd.insert(0, "Enter password")
        self.passwd.bind("<Button>", self.userText)
        self.passwd.grid(row=1, column=2)

        self.port = Entry(self.root, background='#959ba5')
        self.port.insert(0, "Enter port")
        self.port.bind("<Button>", self.userText)
        self.port.grid(row=1, column=3)

        self.name = Entry(self.root, background='#959ba5')
        self.name.insert(0, "Connection name")
        self.name.bind("<Button>", self.userText)
        self.name.grid(row=1, column=4)

        add = Button(self.root, text="add", background='#959ba5')
        add.grid(row=1, column=5)
        add.bind("<Button>", self.add)

        self.defvar = StringVar(self.root)
        try:
            self.defvar.set(self.userdata[0])
            self.option = OptionMenu(self.root, self.defvar, 'Create connection first', command=self.changeConnection)
            self.updateOptions()
            print 'updated on launch'
        except:
            self.defvar.set('Create connection first')
            names = None
            self.option = OptionMenu(self.root, self.defvar, 'Create connection first', command=self.changeConnection)
        self.option.configure(background='#959ba5')

        self.option.grid(row=2, column=0, columnspan=2, sticky=W + E)

        connect = Button(self.root, text="Connect GUI", background='#959ba5')
        connect.grid(row=2, column=2)
        connect.bind("<Button>", self.connect)

    def prepareEcm(self):
        ssh = Button(self.root, text="SSH", background='#959ba5')
        ssh.grid(row=3, column=0, sticky=W + E)
        ssh.bind("<Button>", self.ssh)

        dte = Button(self.root, text="DTE", background='#959ba5')
        dte.grid(row=4, column=0, sticky=W + E)
        dte.bind("<Button>", self.dte)

        telnet = Button(self.root, text="Telnet", background='#959ba5')
        telnet.grid(row=5, column=0, sticky=W + E)
        telnet.bind("<Button>", self.telnet)

        # show ecm info

        # Label(self.root, text="Build id: ").grid(row=3, column=1,sticky=E)
        Label(self.root, text=" ", background='#959ba5').grid(row=13, column=1, sticky=E)

        Label(self.root, text="After connecting the GUI, select one or more modules to perform the actions below",
              font=("Helvetica", 14), background='#959ba5').grid(row=39, column=0, sticky=W, columnspan=4)

        self.version = StringVar()
        self.cpu = StringVar()

        # versionl = Label(self.root, textvariable=self.version).grid(row=3, column=2,columnspan=4,sticky=W)
        # cpul = Label(self.root, textvariable=self.cpu).grid(row=4, column=2, columnspan=4,sticky=W)
        # self.core = Label(self.root, text=" ").grid(row=5, column=2, columnspan=4)

    def refreshLabels(self, host):
        info = self.comm.getInfo(host, self.modules)
        # print self.modules
        for i in self.infoLabels:
            i.destroy()
        n = 0
        for i, m in zip(info, self.modules):
            l = Label(self.root, background='#959ba5',
                      text='     Slot: ' + str(m) + ' Build id: ' + i['id'] + ' Package: ' + i['dnm'])
            l.grid(row=3 + n, column=1, columnspan=4, sticky=W)
            self.infoLabels.append(l)

            n += 1
        # self.version.set(info['id'])
        # self.cpu.set(info['dnm'])

        # self.core['text'] = 'core 42'

    def coldReboot(self, e):

        for i in self.getSelectedBoxes():
            self.comm.reboot(self.getSelected()['host'], i, 'cold')

    def warmReboot(self, e):
        for i in self.getSelectedBoxes():
            self.comm.reboot(self.getSelected()['host'], i, 'warm')

    def factoryReset(self, e):
        for i in self.getSelectedBoxes():
            if i == 'ECM':
                self.comm.factoryReset(self.getSelected()['host'])

    def copyFile(self, e):
        for i in self.getSelectedBoxesIp():
            self.comm.copy(self.getSelected()['host'], i)

    def moduleUpgrade(self, e):
        None

    def log(self, e):
        None

    def core(self, e):
        for i in self.modules:
            self.comm.core(self.getSelected()['host'], self.modules[i][0])

    def openSSH(self, e):
        ips = self.getSelectedBoxesIp()
        names = self.getSelectedBoxes()
        print 'names' + str(names)
        print 'ips' + str(ips)
        for i in range(len(ips)):
            if names[i] == 'ECM':
                self.comm.openSSHSession(self.getSelected()['host'])
            else:
                self.comm.openSSHToNode(self.getSelected()['host'], ips[i])

    def prepareThree(self):
        cr = Button(self.root, text="Cold reboot", background='#959ba5')
        cr.grid(row=50, column=0, sticky=W + E)
        cr.bind("<Button>", self.coldReboot)

        wr = Button(self.root, text="Warm reboot", background='#959ba5')
        wr.grid(row=50, column=1, sticky=W + E)
        wr.bind("<Button>", self.warmReboot)

        fr = Button(self.root, text="Factory reset", background='#959ba5')
        fr.grid(row=50, column=2, sticky=W + E)
        fr.bind("<Button>", self.factoryReset)

        cf = Button(self.root, text="Open SSH connection", background='#959ba5')
        cf.grid(row=50, column=3, sticky=W + E)
        cf.bind("<Button>", self.openSSH)

        ore = Button(self.root, text="Check core", background='#959ba5')
        ore.grid(row=50, column=4, sticky=W + E)
        ore.bind("<Button>", self.core)

    def refreshModules(self, host):
        if host != None:
            #print 'output ' + str(self.comm.get_ipv6(host))
            self.modules = self.comm.get_ipv6(host)
            self.modules['Local system'] = ['']
            try:

                for i in self.modulechecks:
                    i[0].destroy()
            except:
                print"error deleting checkboxes"
            n = 0
            self.modulechecks = []
            srcList = []
            for i in self.modules:
                var = IntVar(value=0)
                # import ipdb;ipdb.set_trace()
                if i == 'ECM' or i == 'CEM' or 'Local' in str(i):

                    c = Checkbutton(self.root, variable=var, text=str(i), background='#959ba5',
                                    command=lambda bound_d=i: self.updateDest('' + str(bound_d)))
                    srcList.append(str(i))
                else:
                    c = Checkbutton(self.root, variable=var, text='Slot ' + str(i), background='#959ba5',
                                    command=lambda bound_d=i: self.updateDest('Slot ' + str(bound_d)))
                    srcList.append('Slot ' + str(i))
                c.grid(row=40 + n / 5, column=n % 5, sticky=W)
                self.modulechecks.append([c, var])
                n += 1

            self.updateSrc(srcList)

    def prepareCopying(self):
        Label(self.root, text="Copy files from source to destination",
              font=("Helvetica", 14), background='#959ba5').grid(row=60, column=0, sticky=W, columnspan=4)

        Label(self.root, text="Source",
              background='#959ba5').grid(row=61, column=0)
        Label(self.root, text="Destination", background='#959ba5').grid(row=61, column=2)
        Label(self.root, text="Source path", background='#959ba5').grid(row=61, column=1)
        Label(self.root, text="Destination path", background='#959ba5').grid(row=61, column=3)

        self.srcvar = StringVar(self.root)
        self.srcvar.set('Local system')
        self.source = OptionMenu(self.root, self.srcvar, 'Local system', command=self.updateSrc)
        # self.updateOptions()
        self.source.grid(row=62, column=0, sticky=W + E)
        self.source.configure(background='#959ba5')

        self.srcPath = Entry(self.root, background='#959ba5')
        self.srcPath.insert(0, '')
        self.srcPath.grid(row=62, column=1)

        self.destPath = Entry(self.root, background='#959ba5')
        self.destPath.insert(0, '')
        self.destPath.grid(row=62, column=3)

        self.destLabel = Label(self.root, background='#959ba5', text=' ')
        self.destLabel.grid(row=62, column=2)

        cr = Button(self.root, text="Copy", background='#959ba5')
        cr.grid(row=62, column=4, sticky=W + E)
        cr.configure(command=lambda: self.startCopy(cr))

    def updateSrc(self, srcList):

        m = self.source.children['menu']
        m.delete(0, END)

        for val in srcList:
            m.add_command(label=val, command=lambda v=self.srcvar, l=val: v.set(l))
        self.srcvar.set(srcList[-0])
        #print 'done'

    def updateDest(self, e):
        self.destLabel.destroy()
        txt = ''
        for i in self.getSelectedBoxes():
            if i == 'ECM' or i == 'CEM':
                txt += i + ', '
            elif 'Local' in str(i):
                txt += 'Local system, '
            else:
                txt += 'slot ' + str(i) + ', '

        self.destLabel = Label(self.root, background='#959ba5', text=txt[:-2])
        self.destLabel.grid(row=62, column=2)

    def startCopy(self, e):


        try:
            n = 0
            print self.modules
            for i in self.modules:
                if 'Slot ' in self.srcvar.get():

                    if 'Slot ' + str(i) == self.srcvar.get():
                        src = self.modules[i][0]
                else:
                    if i == self.srcvar.get():
                        if 'Local' in i:
                            src = ''
                        elif 'ECM' in i:
                            src = self.getSelected()['host']
                            print 'ECM'
                        else:
                            src = self.modules[i][0]
                    else:
                        # src=''
                        print 'default'
                n += 1

            #print src
            #print self.srcPath.get()
            #print self.destPath.get()
            #print self.getSelectedBoxesIp()

            #print self.modules['ECM']

            for i in self.getSelectedBoxesIp():
                print i

                if i == self.modules['ECM'][0]:
                    self.comm.scp(src, self.getSelected()['host'], self.srcPath.get(), self.destPath.get(),
                                  self.getSelected()['host'])
                else:
                    self.comm.scp(src, i, self.srcPath.get(), self.destPath.get(), self.getSelected()['host'])
            m = tkMessageBox.showinfo("Info", "Done copying")
        except:
            m = tkMessageBox.showinfo("Info", "Copying failed")
            None





    def __init__(self):

        # read userdata
        import warnings
        warnings.filterwarnings(action='ignore', module='.*paramiko.*')

        if os.name == 'nt':
            # 'win'
            self.os = 'win'
        else:
            self.os = 'unix'

        self.readFile()

        self.root = Tk()
        self.root.configure(background='#959ba5')  # E53B2E  #959ba5 #024386

        self.prepareFirst()
        self.prepareCopying()
        self.prepareEcm()

        self.prepareThree()

        self.comm = cn.TerminalConnector(self.os)
        self.refreshModules(None)

        self.root.protocol("WM_DELETE_WINDOW", self.saveData)

        self.root.mainloop()
        print 'exit'


Gui()
