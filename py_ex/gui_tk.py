from tkinter import *


class queryrunner(Tk):
    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent
        self.minsize(width=800,height=500)
        self.initialize()

    def initialize(self):
        self.grid_columnconfigure(2,weight=1)
        self.grid_columnconfigure(3,weight=1)
        self.grid_columnconfigure(6,weight=2)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=1)
        self.grid_rowconfigure(4,weight=1)
        # BUCKET AND N1QL LABEL + INPUT PAIRS:
        self.label = Label(self,text="IP", width=10, anchor="w")
        self.label.grid(column=0,row=0,columnspan=1,sticky='W')
        self.entry = Entry(self)
        self.entry.grid(column=1,row=0, columnspan=3, rowspan=1, sticky='EW')
        # EXECUTE N1QL QUERY AGAINST BUCKET WHEN BUTTON CLICKED:
        self.button = Button(self,text="Go",width=20, command=self.on_button1)
        self.button.grid(column=6,row=0)
        self.label2 = Label(self,text="Filter", anchor="w")
        self.label2.grid(column=0,row=1,columnspan=1,sticky='W')
        self.entry2 = Entry(self)
        self.entry2.grid(column=1,row=1, columnspan=3, rowspan=1, sticky='W')

        self.label3 = Label(self,text="Output:", width=50,anchor="w")
        self.label3.grid(column=0,row=4,columnspan=5,sticky='W')
        self.entry3 = Text(self,height=18)
        self.entry3.grid(column=1,row=5, columnspan=5, rowspan=1, sticky='W')
        # PROBLEM: GET SCROLLBAR TO BE THE RIGHT SIZE (IT'S NOT THE SIZE OF THE THING ITS BESIDE)
        self.scrollbar = Scrollbar(self) # height= not permitted here!
        self.entry3.config(yscrollcommand= self.scrollbar.set)
        self.scrollbar.config(command= self.entry3.yview)
        self.grid()
        self.scrollbar.grid(column=6, row=5, rowspan=2,  sticky=N+S+W)

    def on_button1(self):
        quote = self.entry2.get()
        self.entry3.insert(END, quote)


if __name__ == "__main__":
    app = queryrunner(None)
    app.title('AOS Query POWER')
    app.mainloop()
