#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" read data from a log file using numpy.loadtxt()
then make a plot using matplotlib.pyplot
 """

import numpy as np
import matplotlib.pyplot as plt

filename_r1 = '/home/sit/share/rfw_out/il_p1.log'
psm1_opr_filename = '/home/sit/share/rfw_out/psm1_opr.png'
psm1_il2_filename = '/home/sit/share/rfw_out/psm1_il2.png'
psm1_opt_filename = '/home/sit/share/rfw_out/psm1_opt.png'
psm1_il3_filename = '/home/sit/share/rfw_out/psm1_il3.png'

data1 = np.loadtxt(filename_r1)
x = range(data1[:, 0].size)

# for psm#1
fig_psm1_opr = plt.figure()
ax_psm1_opr = fig_psm1_opr.add_subplot(111)
ax_psm1_opr.plot(x, data1[:, 0], 'r.', label="psm1_opr")
ymin, ymax = ax_psm1_opr.get_ylim()
if ymax - ymin < 1.0:
    ymid = (ymax + ymin) / 2
    ax_psm1_opr.set_ylim(ymid - 0.5, ymid + 0.5)
ax_psm1_opr.legend(loc='best', numpoints=1)
fig_psm1_opr.savefig(psm1_opr_filename, bbox_inches='tight')

fig_psm1_il2 = plt.figure()
ax_psm1_il2 = fig_psm1_il2.add_subplot(111)
ax_psm1_il2.plot(x, data1[:, 2], 'k.', label="psm1_opt2")
ax_psm1_il2.plot(x, data1[:, 3], 'r.', label="p1_opr2")
ax_psm1_il2.legend(loc='best', numpoints=1)
fig_psm1_il2.savefig(psm1_il2_filename, bbox_inches='tight')

fig_psm1_opt, ax_psm1_opt = plt.subplots(1, 1)
ax_psm1_opt.plot(x, data1[:, 1], 'k.', label='psm1_opt')
ymin, ymax = ax_psm1_opt.get_ylim()
if ymax - ymin < 1.0:
    ymid = (ymax + ymin) / 2
    ax_psm1_opt.set_ylim(ymid - 0.5, ymid + 0.5)
ax_psm1_opt.legend(loc='best', numpoints=1)
fig_psm1_opt.savefig(psm1_opt_filename, bbox_inches='tight')

fig_psm1_il3, ax_psm1_il3 = plt.subplots(1, 1)
ax_psm1_il3.plot(x, data1[:, 4], 'k.', label='psm1_opt3')
ax_psm1_il3.plot(x, data1[:, 5], 'r.', label='p1_opr3')
ax_psm1_il3.legend(loc='best', numpoints=1)
fig_psm1_il3.savefig(psm1_il3_filename, bbox_inches='tight')
