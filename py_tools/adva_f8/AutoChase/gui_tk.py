from Tkinter import *
from .auto_chase import *


class queryrunner(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.minsize(width=800, height=500)
        self.rst_txt = ''
        self.filename = 'auto_chase_result.txt'
        self.initialize()

    def initialize(self):
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(6, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.lbl_ip = Label(self, text="IP", width=10, anchor="w")
        self.lbl_ip.grid(column=0, row=0, columnspan=1, sticky='W')
        self.lbl_ptp = Label(self, text="Filter", anchor="w")
        self.lbl_ptp.grid(column=0, row=1, columnspan=1, sticky='W')
        self.lbl_bidi = Label(self, text="Bi-Directional?", anchor="w")
        self.lbl_bidi.grid(column=0, row=2, columnspan=1, sticky='W')
        self.lbl_file = Label(self, text="Filename", anchor="w")
        self.lbl_file.grid(column=0, row=3, columnspan=1, sticky='W')
        self.lbl_out = Label(self, text="Output:", width=50, anchor="w")
        self.lbl_out.grid(column=0, row=4, columnspan=5, sticky='W')

        self.ent_ip = Entry(self)
        self.ent_ip.grid(column=1, row=0, columnspan=3, rowspan=1, sticky='EW')
        self.ent_ptp = Entry(self)
        self.ent_ptp.grid(column=1, row=1, columnspan=3, rowspan=1, sticky='W')
        self.ent_bidi = Entry(self)
        self.ent_bidi.grid(column=1, row=2, columnspan=3,
                           rowspan=1, sticky='EW')
        self.ent_file = Entry(self)
        self.ent_file.grid(column=1, row=3, columnspan=3,
                           rowspan=1, sticky='EW')

        self.btn_start = Button(self, text="Start", width=20,
                                command=self.on_btn_start)
        self.btn_start.grid(column=6, row=0)
        self.btn_save = Button(self, text='Save to File', width=20,
                               command=self.on_btn_save)
        self.btn_save.grid(column=6, row=4)
        self.btn_quit = Button(self, text='Quit', width=20,
                               command=self.destroy)
        self.btn_quit.grid(column=6, row=6)

        self.txt_out = Text(self, height=18)
        self.txt_out.grid(column=1, row=5, columnspan=5, rowspan=1, sticky='W')
        self.scrollbar = Scrollbar(self)  # height= not permitted here!
        self.txt_out.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.txt_out.yview)
        self.scrollbar.grid(column=6, row=5, rowspan=2, sticky=N + S + W)
        self.grid()

    def on_btn_start(self):
        self.txt_out.delete(1.0, END)

        ip = self.ent_ip.get()

        ptp = self.ent_ptp.get()
        if ptp.count('/') == 1:
            ptp += '/ci'
        elif ptp.count('/') == 2:
            card, port = ptp.rsplit('/', 1)
            if not port.startswith('c'):  # ptp_head must be a client port
                port = 'ci'
                ptp = card + '/' + port
        else:
            self.txt_out.insert(INSERT, 'Wrong input for the filter!')
            return

        bidi = self.ent_bidi.get()
        if bidi == 'True':
            bidi = True
        else:
            bidi = False

        self.rst_txt = main(ip, ptp, bidi)
        self.txt_out.insert(INSERT, self.rst_txt)

    def on_btn_save(self):
        filename = self.ent_file.get()
        if filename:
            self.filename = filename
        with open(self.filename, 'w') as f:
            f.write(self.rst_txt)


if __name__ == "__main__":
    app = queryrunner(None)
    app.title('AOS Query POWER')
    app.mainloop()
