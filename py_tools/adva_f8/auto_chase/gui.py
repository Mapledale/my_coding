from Tkinter import *
import auto_chase as ac


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
        ip = self.entry.get()
        filter = self.entry2.get()
        # self.entry3.insert(END, quote)
        filename = 'auto_chase_result.txt'
        bidi = False
        self.auto_main(ip, filter, filename, bidi)

    def drawProgressBar(self, percent, barLen=20):
        sys.stdout.write('\r')
        progress = ''
        for i in range(barLen):
            if i < int(barLen * percent):
                progress += '='
            else:
                progress += ' '
        sys.stdout.write('[%s] %.2f%%' % (progress, percent * 100))
        sys.stdout.flush()


    def show_ne(self, ip, ptp, rst_file):
        ne = ac.AutoChaseNe(ip, ptp, rst_file)
        print('')
        print('Working on node %s...' % ip)
        bar_len = 80
        prgs = 0.05
        self.drawProgressBar(prgs, bar_len)
        prgs = 0.1
        # ne._update_fiber_map()
        # print('\nfiber map:')
        # for fiber in ne.fiber_map:
        #     print(fiber)

        ne.update_ptp_chain()
        # print('\nPTP Chain:')
        # for e in ne.ptp_chain:
        #     print(e)
        self.drawProgressBar(prgs, bar_len)
        prgs += 0.2
        # ne.update_ne_type()
        # if ne.type == 'transit':
        #     recur = True
        # print('\nNE type is: %s' % ne.type)

        for chain_ele in ne.ptp_chain:
            rst_file.write('\nCard %s: %s\n' %
                           (chain_ele['card'], chain_ele['card_type']))
            self.drawProgressBar(prgs, bar_len)
            if chain_ele['a_end']:
                ptp = chain_ele['card'] + '/' + chain_ele['a_end']
                rst_file.write('\tPort %s:\n' % chain_ele['a_end'])
                pm = ne.get_ptp_power(ptp)
                if pm:
                    # rst_file.write('\t\tTx: %s\n' % pm[1])
                    rst_file.write('\t\tRx: %s\n' % pm[0])
                else:
                    rst_file.write('\t\tPM reading N/A\n')
            self.drawProgressBar(prgs, bar_len)
            prgs += 0.1
            if chain_ele['z_end']:
                ptp = chain_ele['card'] + '/' + chain_ele['z_end']
                rst_file.write('\tPort %s:\n' % chain_ele['z_end'])
                pm = ne.get_ptp_power(ptp)
                if pm:
                    rst_file.write('\t\tTx: %s\n' % pm[1])
                    # rst_file.write('\t\tRx: %s\n' % pm[0])
                else:
                    rst_file.write('\t\tPM reading N/A\n')
            self.drawProgressBar(prgs, bar_len)
            prgs += 0.1
        # card_type = ne._get_card_type('%s/%s' % (shelf, slot))
        # print('\nCard Type of %s/%s:' % (shelf, slot))
        # print('%s' % card_type)

        # pm = ne._get_ptp_power(ptp)
        # print('\nPM readings of %s:' % ptp)
        # print('pm_r: %s' % pm[0])
        # print('pm_t: %s' % pm[1])

        # print('\nIs %s with ots?' % ptp)
        # print(ne._is_ots(ptp))
        # print('Is %s with ots?' % '1/5/n')
        # print(ne._is_ots('1/5/n'))

        next_ne = {'ip': None, 'ptp': None}
        ptp_tail_card = ne.ptp_chain[-1]['card']
        ptp_tail_port = ne.ptp_chain[-1]['z_end']
        ptp_tail = ptp_tail_card + '/' + ptp_tail_port
        if ne.is_ots(ptp_tail):
            next_ne['ip'] = ne.get_next_node_ip(ptp_tail)
            next_ne['ptp'] = ne.get_next_node_ots(ptp_tail)
        self.drawProgressBar(1, bar_len)
        print('')
        tail = {'ip': ip, 'ptp': ptp_tail}
        return (tail, next_ne)


    def auto_main(self, ip, ptp, filename, bidi=False):
        rst_file = open(filename, 'a')
        rst_file.write('Start from the filter provided by user...\n')
        tail, next_ne = self.show_ne(ip, ptp, rst_file)
        while next_ne['ip']:
            tail, next_ne = self.show_ne(next_ne['ip'], next_ne['ptp'], rst_file)

        rst_file.write('\n--------------------------------------\n')
        rst_file.write('Reached the end of OMS. Job done. Bye!\n')
        rst_file.close()
        print('\nJob done! Please check %s for the result.' % filename)

        if bidi:
            ip = tail['ip']
            ptp = tail['ptp']
            self.auto_main(ip, ptp, filename)


if __name__ == "__main__":
    app = queryrunner(None)
    app.title('AOS Query POWER')
    app.mainloop()
