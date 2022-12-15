import tkinter
import math
import customtkinter
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

print("==========================================================")
print('| |------------------------------------------------------|')
print('| |                 Signals and Systems                  |')
print('| |             Amplitude Modulated Signals              |')
print('| |------------------------------------------------------|')
print('| ©   2022 DIAN VELICHKOV KINANEV. All Rights Reserved.  |')
print('| |      Technical University Sofia - Branch Plovdiv     |')
print('| |                Leader of the project                 |')
print('| |            Dr.   Eng.   Iliya   Petrov               |')
print("==========================================================")


def RANGING(START, END, STEP):
    # Calculate range between START, END with STEP
    RANGE = []
    while START <= END:
        RANGE.append(START)
        START += STEP
    return RANGE


def my_xformatter(x, pos):
    """
    formater xticks plot from 0.00 to .0
    """
    x = round(x, 3)
    val_str = '{:g}'.format(x)
    if np.abs(x) > 0 and np.abs(x) < 1:
        return val_str.replace("0", "", 1)
    else:
        return val_str


def my_yformatter(y, pos):
    """
    formater yticks plot from 0.00 to .0
    """
    x = math.ceil(y)
    val_str = '{:g}'.format(x)
    return val_str


# Function Button callback
def BUTTON_PRESSED():
    # define variables
    ampl = []
    f = []
    phase = []
    fsig = None
    # GET Values
    combobox = float(ComboboxL.get())
    amplc = float(Modulating_Signal_CAE.get())
    fc = int(Modulating_Signal_CFE.get())
    phasec = float(Modulating_Signal_CPHE.get())

    # get the value from UI ampl
    ampl.append(float(Modulating_Signal_1AE.get()))
    f.append(int(Modulating_Signal_1FE.get()))  # get the value from UI f
    # get the value from UI phase
    phase.append(float(Modulating_Signal_1PHE.get()))
    # Calculate the greatest common divisors
    fsig = f[0]
    if combobox >= 2:
        ampl.append(float(Modulating_Signal_2AE.get()))
        f.append(int(Modulating_Signal_2FE.get()))
        phase.append(float(Modulating_Signal_2PHE.get()))
        fsig = math.gcd(f[0], f[1])
    if combobox >= 3:
        ampl.append(float(Modulating_Signal_3AE.get()))
        f.append(int(Modulating_Signal_3FE.get()))
        phase.append(float(Modulating_Signal_3PHE.get()))
        fsig = math.gcd(math.gcd(f[0], f[1]), f[2])
    if combobox >= 4:
        ampl.append(float(Modulating_Signal_4AE.get()))
        f.append(int(Modulating_Signal_4FE.get()))
        phase.append(float(Modulating_Signal_4PHE.get()))
        fsig = math.gcd(math.gcd(math.gcd(f[0], f[1]), f[2]), f[3])

    # change arrays to numpy arrays:
    ampl = np.array(ampl)
    f = np.array(f)
    phase = np.array(phase)
    # ------------------------------------------------------------------------
    t = np.array(RANGING(0, 2 / fsig, 1 / fsig / 1000))
    y = np.array([0 for i in range(t.shape[0])])
    for i in range(int(combobox)):
        y = y + ampl[i] * np.cos(2 * np.pi * f[i] * t + phase[i] * np.pi / 180)
    # FIRST PLOT  ------------------------------------------------------------
    # Set up figure size.
    plt.close('all')
    fig = plt.figure(figsize=(6.5, 1.5), dpi=100, facecolor='#EBEBEB')
    ax1 = fig.add_subplot()
    FIG1 = FigureCanvasTkAgg(figure=fig, master=FRAME_fig_01)
    FIG1.draw()
    FIG1.get_tk_widget().place(x=-45, y=-10)
    ax1.tick_params(direction="in")
    ax1.xaxis.set_major_formatter(
        FuncFormatter(my_xformatter))  # Set up suplots .0
    ax1.yaxis.set_major_formatter(
        FuncFormatter(my_yformatter))  # Set up suplots .0
    ax1.plot(t, y, c='blue', linestyle='-', linewidth=0.7)  # Plot
    ax1.grid()  # grid plot
    ax1.xaxis.set_ticks(RANGING(min(t), max(t), (max(t) - min(t)) / 10))
    ax1.yaxis.set_ticks(RANGING(min(y), max(y), (max(y) - min(y)) / 3))
    ax1.set_xlim([min(t), max(t)])  # Set up x limit
    ax1.set_ylim([min(y), max(y)])  # Set up y limit
    # --------------------------------------------------------------------------
    tt = np.array(RANGING(0, 50 / fc, 1 / fc / 25))
    sctt = amplc * np.cos(2 * np.pi * fc * tt + phasec * np.pi / 180)
    # SECOND PLOT  --------------------------------------------------------------
    # Set up figure size.
    fig2 = plt.figure(figsize=(6.5, 1.5), dpi=100, facecolor='#EBEBEB')
    ax2 = fig2.add_subplot()
    FIG2 = FigureCanvasTkAgg(figure=fig2, master=FRAME_fig_02)
    FIG2.draw()
    FIG2.get_tk_widget().place(x=-45, y=-10)
    ax2.tick_params(direction="in")
    ax2.xaxis.set_major_formatter(FuncFormatter(my_xformatter))
    ax2.yaxis.set_major_formatter(FuncFormatter(my_yformatter))
    ax2.xaxis.set_ticks(RANGING(min(tt), max(tt), (max(tt) - min(tt)) / 10))
    ax2.yaxis.set_ticks(RANGING(min(sctt), max(sctt), (max(sctt) - min(sctt)) / 3))
    ax2.plot(tt, sctt, c='blue', linestyle='-', linewidth=0.7)
    ax2.set_xlim([min(tt), max(tt)])
    ax2.set_ylim([min(sctt), max(sctt)])
    # --------------------------------------------------------------------------
    sc = amplc * np.cos(2 * np.pi * fc * t + phasec * np.pi / 180)
    smod = (amplc + y) * np.cos(2 * np.pi * fc * t + phasec * np.pi / 180)
    # THIRD PLOT  --------------------------------------------------------------
    # Set up figure size.
    fig3 = plt.figure(figsize=(6.5, 1.5), dpi=100, facecolor='#EBEBEB')
    ax3 = fig3.add_subplot()
    FIG3 = FigureCanvasTkAgg(figure=fig3, master=FRAME_fig_03)
    FIG3.draw()
    FIG3.get_tk_widget().place(x=-45, y=-10)
    ax3.tick_params(direction="in")
    ax3.xaxis.set_major_formatter(FuncFormatter(my_xformatter))
    ax3.yaxis.set_major_formatter(FuncFormatter(my_yformatter))
    ax3.xaxis.set_ticks(RANGING(min(t), max(t), (max(t) - min(t)) / 10))
    ax3.yaxis.set_ticks(RANGING(min(smod) - 2, max(smod) + 2, (max(smod) - min(smod)) / 3))
    ax3.plot(t, smod, c='blue', linestyle='-', linewidth=0.7)
    ax3.set_xlim([min(t), max(t)])
    ax3.set_ylim([min(smod) - 2, max(smod) + 2])
    # -------------------------------------------------------------------------
    a = []
    fr = []
    for i in range(int(combobox)):
        a.append(ampl[i] / 2)
        fr.append(fc - f[i])
    a.append(amplc)
    fr.append(fc)
    for i in range(int(combobox) - 1, -1, -1):
        a.append(ampl[i] / 2)
        fr.append(fc + f[i])
    k = [min(fr) - 3 * fsig, max(fr) + 3 * fsig]
    XLim = k  # limit axis
    # FOURTH PLOT --------------------------------------------------------------
    # Set up figure size.
    fig4 = plt.figure(figsize=(6.5, 1.5), dpi=100, facecolor='#EBEBEB')
    ax4 = fig4.add_subplot()
    FIG4 = FigureCanvasTkAgg(figure=fig4, master=FRAME_fig_04)
    FIG4.draw()
    FIG4.get_tk_widget().place(x=-45, y=-10)
    ax4.tick_params(direction="in")
    ax4.xaxis.set_major_formatter(FuncFormatter(my_xformatter))
    ax4.yaxis.set_major_formatter(FuncFormatter(my_yformatter))
    ax4.stem(fr, a)
    ax4.set_xlim(k)
    ax4.set_ylim([0, max(a) + 1])


# Code started ---------------------------------------------------------------------------------
CTKi = customtkinter.CTk()
CTKi.title("Amplitude Modulated Signals by Dian Velichkov")
CTKi.geometry(f"{830}x{550}+{10}+{10}")

# CTKi.resizable(False, False)
print(' ---- CODE  STARTED ---- ')
print(' ----  GUI WORKING  ---- ')

font = tkinter.font.Font(family='Helvetica', size=11, weight='bold')
# RIGHT FRAME
Modulating_Signals = tkinter.LabelFrame(CTKi, labelanchor='n')
Modulating_Signals.pack(fill='y', expand=True, side='top', anchor='e', padx=4, pady=4)
# RIGHT FRAME TOP FRAME
Modulating_SignalsFR1 = tkinter.LabelFrame(Modulating_Signals, labelanchor='n', borderwidth=0)
Modulating_SignalsFR1.grid(row=0, column=0, padx=4, pady=4)
# RIGHT FRAME TOP FRAME FIRST FRAME Modulating Signal 1
Modulating_Signal_1 = tkinter.LabelFrame(Modulating_SignalsFR1, text='  Modulating \n  Signal 1  ', labelanchor='n',
                                         borderwidth=1.5, relief='solid', font=font, )
Modulating_Signal_1.grid(sticky='wn', row=0, column=0, padx=(20, 10), pady=(20, 10))
# RIGHT FRAME TOP FRAME SECOND FRAME Modulating Signal 2
Modulating_Signal_2 = tkinter.LabelFrame(Modulating_SignalsFR1, text='  Modulating \n  Signal 2  ', labelanchor='n',
                                         borderwidth=1.5, relief='solid', font=font)
Modulating_Signal_2.grid(sticky='ne', row=0, column=1, padx=(20, 10), pady=(20, 10))
# RIGHT FRAME TOP FRAME THIRD FRAME Modulating Signal 3
Modulating_Signal_3 = tkinter.LabelFrame(
    Modulating_SignalsFR1, text='  Modulating \n  Signal 3  ', labelanchor='n', borderwidth=1.5, relief='solid',
    font=font)
Modulating_Signal_3.grid(sticky='wn', row=1, column=0, padx=(20, 10), pady=(20, 10))
# RIGHT FRAME TOP FRAME THIRD FRAME Modulating Signal 4
Modulating_Signal_4 = tkinter.LabelFrame(Modulating_SignalsFR1, text='  Modulating \n  Signal 4  ', labelanchor='n',
                                         borderwidth=1.5, relief='solid', font=font)
Modulating_Signal_4.grid(sticky='wn', row=1, column=1, padx=(20, 10), pady=(20, 10))
# RIGHT FRAME CENTRE FRAME
Modulating_SignalsFR2 = tkinter.LabelFrame(Modulating_Signals, labelanchor='n', borderwidth=1.5, relief='solid')
Modulating_SignalsFR2.grid(row=1, column=0, padx=4, pady=10)
# RIGHT FRAME LAST FRAME
Modulating_Signal_C = tkinter.LabelFrame(Modulating_Signals, labelanchor='n', text='  Carrier \n  Signal  ',
                                         borderwidth=1.5, relief='solid', font=font)
Modulating_Signal_C.grid(row=2, column=0, padx=4, pady=10)
# Figures
FRAME_fig_01 = tkinter.Frame(CTKi, height=140, width=550)
FRAME_fig_01.place(x=10, y=10)
FRAME_fig_02 = tkinter.Frame(CTKi, height=140, width=550)
FRAME_fig_02.place(x=10, y=160)
FRAME_fig_03 = tkinter.Frame(CTKi, height=140, width=550)
FRAME_fig_03.place(x=10, y=310)
FRAME_fig_04 = tkinter.Frame(CTKi, height=140, width=550)
FRAME_fig_04.place(x=10, y=460)
HZ = tkinter.Label(CTKi, text='HZ', font=tkinter.font.Font(family='Helvetica', size=13))
HZ.place(x=570, y=570)


# -------------------------------------------------------------------------------------------------------------
def SHOW_FRAME(event=None):
    global Modulating_SignalsFR1, Modulating_Signal_1, Modulating_Signal_2, Modulating_Signal_3, Modulating_Signal_4, \
        Modulating_Signal_1AE, Modulating_Signal_1FE, Modulating_Signal_1PHE, Modulating_Signal_2AE, Modulating_Signal_2FE, \
        Modulating_Signal_2PHE, Modulating_Signal_3AE, Modulating_Signal_3FE, Modulating_Signal_3PHE, Modulating_Signal_4AE, \
        Modulating_Signal_4FE, Modulating_Signal_4PHE
    # ---------------------------------------------------------------------------------------------------------
    # RIGHT FRAME TOP FRAME FIRST FRAME Modulating Signal 1
    for widgets in Modulating_Signal_1.winfo_children():
        widgets.destroy()
    for widgets in Modulating_Signal_2.winfo_children():
        widgets.destroy()
    for widgets in Modulating_Signal_3.winfo_children():
        widgets.destroy()
    for widgets in Modulating_Signal_4.winfo_children():
        widgets.destroy()
    # RIGHT FRAME TOP FRAME FIRST FRAME Modulating Signal 1
    Modulating_Signal_1 = tkinter.LabelFrame(
        Modulating_SignalsFR1, text='  Modulating \n  Signal 1  ', labelanchor='n', borderwidth=1.5, relief='solid',
        font=font)
    Modulating_Signal_1.grid(sticky='wn', row=0, column=0, padx=(20, 10), pady=(20, 10))
    # RIGHT FRAME TOP FRAME SECOND FRAME Modulating Signal 2
    Modulating_Signal_2 = tkinter.LabelFrame(Modulating_SignalsFR1, text='  Modulating \n  Signal 2  ', labelanchor='n',
                                             borderwidth=1.5, relief='solid', font=font)
    Modulating_Signal_2.grid(sticky='ne', row=0, column=1, padx=(20, 10), pady=(20, 10))
    # RIGHT FRAME TOP FRAME THIRD FRAME Modulating Signal 3
    Modulating_Signal_3 = tkinter.LabelFrame(Modulating_SignalsFR1, text='  Modulating \n  Signal 3  ', labelanchor='n',
                                             borderwidth=1.5, relief='solid', font=font)
    Modulating_Signal_3.grid(sticky='wn', row=1, column=0, padx=(20, 10), pady=(20, 10))
    # RIGHT FRAME TOP FRAME THIRD FRAME Modulating Signal 4
    Modulating_Signal_4 = tkinter.LabelFrame(Modulating_SignalsFR1, text='  Modulating \n  Signal 4  ', labelanchor='n',
                                             borderwidth=1.5, relief='solid', font=font)
    Modulating_Signal_4.grid(sticky='wn', row=1, column=1, padx=(20, 10), pady=(20, 10))
    VAL = float(ComboboxL.get())
    if VAL >= 1:
        Modulating_Signal_1AL = tkinter.Label(Modulating_Signal_1, text='A = ', justify='right', anchor="ne",
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_1AL.grid(sticky='ne', row=0, column=0, pady=4)
        Modulating_Signal_1AE = tkinter.Entry(Modulating_Signal_1, width=10, justify='center',
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_1AE.insert(0, '3')
        Modulating_Signal_1AE.grid(sticky='n', row=0, column=1, pady=4)
        Modulating_Signal_1AV = tkinter.Label(Modulating_Signal_1, text='V', justify='left', anchor="w",
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_1AV.grid(sticky='w', row=0, column=2, pady=4)

        Modulating_Signal_1FL = tkinter.Label(Modulating_Signal_1, text='f = ', justify='right', anchor="ne",
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_1FL.grid(sticky='ne', row=1, column=0, pady=4)
        Modulating_Signal_1FE = tkinter.Entry(Modulating_Signal_1, width=10, justify='center',
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_1FE.insert(0, '100')
        Modulating_Signal_1FE.grid(sticky='n', row=1, column=1, pady=4)
        Modulating_Signal_1FHZ = tkinter.Label(Modulating_Signal_1, text='HZ', justify='left', anchor="w",
                                               font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_1FHZ.grid(sticky='w', row=1, column=2, pady=4)

        Modulating_Signal_1PHL = tkinter.Label(Modulating_Signal_1, text='phase = ', justify='right', anchor="ne",
                                               font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_1PHL.grid(sticky='ne', row=2, column=0, pady=4)
        Modulating_Signal_1PHE = tkinter.Entry(Modulating_Signal_1, width=10, justify='center',
                                               font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_1PHE.insert(0, '100')
        Modulating_Signal_1PHE.grid(sticky='n', row=2, column=1, pady=4)
        Modulating_Signal_1PHDEG = tkinter.Label(Modulating_Signal_1, text='deg', justify='left', anchor="w",
                                                 font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_1PHDEG.grid(sticky='w', row=2, column=2, pady=4)
    # ---------------------------------------------------------------------------------------------------------
    # RIGHT FRAME TOP FRAME SECOND FRAME Modulating Signal 2
    if VAL >= 2:
        Modulating_Signal_2AL = tkinter.Label(Modulating_Signal_2, text='A = ', justify='right', anchor="ne",
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_2AL.grid(sticky='ne', row=0, column=0, pady=4)
        Modulating_Signal_2AE = tkinter.Entry(Modulating_Signal_2, width=10, justify='center',
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_2AE.insert(0, '2')
        Modulating_Signal_2AE.grid(sticky='n', row=0, column=1, pady=4)
        Modulating_Signal_2AV = tkinter.Label(Modulating_Signal_2, text='V', justify='left', anchor="w",
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_2AV.grid(sticky='w', row=0, column=2, pady=4)

        Modulating_Signal_2FL = tkinter.Label(Modulating_Signal_2, text='f = ', justify='right', anchor="ne",
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_2FL.grid(sticky='ne', row=1, column=0, pady=4)
        Modulating_Signal_2FE = tkinter.Entry(Modulating_Signal_2, width=10, justify='center',
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_2FE.insert(0, '150')
        Modulating_Signal_2FE.grid(sticky='n', row=1, column=1, pady=4)
        Modulating_Signal_2FHZ = tkinter.Label(Modulating_Signal_2, text='HZ', justify='left', anchor="w",
                                               font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_2FHZ.grid(sticky='w', row=1, column=2, pady=4)

        Modulating_Signal_2PHL = tkinter.Label(Modulating_Signal_2, text='phase = ', justify='right', anchor="ne",
                                               font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_2PHL.grid(sticky='ne', row=2, column=0, pady=4)
        Modulating_Signal_2PHE = tkinter.Entry(Modulating_Signal_2, width=10, justify='center',
                                               font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_2PHE.insert(0, '30')
        Modulating_Signal_2PHE.grid(sticky='n', row=2, column=1, pady=4)
        Modulating_Signal_2PHDEG = tkinter.Label(Modulating_Signal_2, text='deg', justify='left', anchor="w",
                                                 font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_2PHDEG.grid(sticky='w', row=2, column=2, pady=4)
    # ---------------------------------------------------------------------------------------------------------
    # RIGHT FRAME TOP FRAME THIRD FRAME Modulating Signal 3
    if VAL >= 3:
        Modulating_Signal_3AL = tkinter.Label(Modulating_Signal_3, text='A = ', justify='right', anchor="ne",
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_3AL.grid(sticky='ne', row=0, column=0, pady=4)
        Modulating_Signal_3AE = tkinter.Entry(Modulating_Signal_3, width=10, justify='center',
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_3AE.insert(0, '1.5')
        Modulating_Signal_3AE.grid(sticky='n', row=0, column=1, pady=4)
        Modulating_Signal_3AV = tkinter.Label(Modulating_Signal_3, text='V', justify='left', anchor="w",
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_3AV.grid(sticky='w', row=0, column=2, pady=4)

        Modulating_Signal_3FL = tkinter.Label(Modulating_Signal_3, text='f = ', justify='right', anchor="ne",
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_3FL.grid(sticky='ne', row=1, column=0, pady=4)
        Modulating_Signal_3FE = tkinter.Entry(Modulating_Signal_3, width=10, justify='center',
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_3FE.insert(0, '200')
        Modulating_Signal_3FE.grid(sticky='n', row=1, column=1, pady=4)
        Modulating_Signal_3FHZ = tkinter.Label(Modulating_Signal_3, text='HZ', justify='left', anchor="w",
                                               font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_3FHZ.grid(sticky='w', row=1, column=2, pady=4)

        Modulating_Signal_3PHL = tkinter.Label(Modulating_Signal_3, text='phase = ', justify='right', anchor="ne",
                                               font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_3PHL.grid(sticky='ne', row=2, column=0, pady=4)
        Modulating_Signal_3PHE = tkinter.Entry(Modulating_Signal_3, width=10, justify='center',
                                               font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_3PHE.insert(0, '60')
        Modulating_Signal_3PHE.grid(sticky='n', row=2, column=1, pady=4)
        Modulating_Signal_3PHDEG = tkinter.Label(Modulating_Signal_3, text='deg', justify='left', anchor="w",
                                                 font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_3PHDEG.grid(sticky='w', row=2, column=2, pady=4)
    # ---------------------------------------------------------------------------------------------------------
    # RIGHT FRAME TOP FRAME THIRD FRAME Modulating Signal 4
    if VAL >= 4:
        Modulating_Signal_4AL = tkinter.Label(Modulating_Signal_4, text='A = ', justify='right', anchor="ne",
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_4AL.grid(sticky='ne', row=0, column=0, pady=4)
        Modulating_Signal_4AE = tkinter.Entry(Modulating_Signal_4, width=10, justify='center',
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_4AE.insert(0, '2')
        Modulating_Signal_4AE.grid(sticky='n', row=0, column=1, pady=4)
        Modulating_Signal_4AV = tkinter.Label(Modulating_Signal_4, text='V', justify='left', anchor="w",
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_4AV.grid(sticky='w', row=0, column=2, pady=4)

        Modulating_Signal_4FL = tkinter.Label(Modulating_Signal_4, text='f = ', justify='right', anchor="ne",
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_4FL.grid(sticky='ne', row=1, column=0, pady=4)
        Modulating_Signal_4FE = tkinter.Entry(Modulating_Signal_4, width=10, justify='center',
                                              font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_4FE.insert(0, '300')
        Modulating_Signal_4FE.grid(sticky='n', row=1, column=1, pady=4)
        Modulating_Signal_4FHZ = tkinter.Label(Modulating_Signal_4, text='HZ', justify='left', anchor="w",
                                               font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_4FHZ.grid(sticky='w', row=1, column=2, pady=4)

        Modulating_Signal_4PHL = tkinter.Label(Modulating_Signal_4, text='phase = ', justify='right', anchor="ne",
                                               font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_4PHL.grid(sticky='ne', row=2, column=0, pady=4)
        Modulating_Signal_4PHE = tkinter.Entry(Modulating_Signal_4, width=10, justify='center',
                                               font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_4PHE.insert(0, '45')
        Modulating_Signal_4PHE.grid(sticky='n', row=2, column=1, pady=4)
        Modulating_Signal_4PHDEG = tkinter.Label(Modulating_Signal_4, text='deg', justify='left', anchor="w",
                                                 font=tkinter.font.Font(family='Helvetica', size=11))
        Modulating_Signal_4PHDEG.grid(sticky='w', row=2, column=2, pady=4)


# ---------------------------------------------------------------------------------------------------------------
# RIGHT FRAME CENTRE FRAME
Modulating_Signal_L = tkinter.Label(Modulating_SignalsFR2, text=' Number of\nModulating\nSignal ', justify='center',
                                    anchor="ne", font=font)
Modulating_Signal_L.grid(sticky='ne', row=0, column=0, pady=10)
ComboboxLi = tkinter.StringVar()
ComboboxL = ttk.Combobox(Modulating_SignalsFR2, values=['1', '2', '3', '4'], width=10, textvariable=ComboboxLi,
                         font=tkinter.font.Font(family='Helvetica', size=11))
ComboboxL.current(3)
SHOW_FRAME()
ComboboxL.bind('<<ComboboxSelected>>', SHOW_FRAME)
ComboboxL.grid(row=0, column=1, padx=4, pady=4)
# ---------------------------------------------------------------------------------------------------------------
# RIGHT FRAME LAST FRAME
Modulating_Signal_CAL = tkinter.Label(Modulating_Signal_C, text='A = ', justify='right', anchor="ne",
                                      font=tkinter.font.Font(family='Helvetica', size=11))
Modulating_Signal_CAL.grid(sticky='ne', row=0, column=0, pady=4)
Modulating_Signal_CAE = tkinter.Entry(Modulating_Signal_C, width=10, justify='center',
                                      font=tkinter.font.Font(family='Helvetica', size=11))
Modulating_Signal_CAE.insert(0, '5')
Modulating_Signal_CAE.grid(sticky='n', row=0, column=1, pady=4)
Modulating_Signal_CAV = tkinter.Label(Modulating_Signal_C, text='V', justify='left', anchor="w",
                                      font=tkinter.font.Font(family='Helvetica', size=11))
Modulating_Signal_CAV.grid(sticky='w', row=0, column=2, pady=4)

Modulating_Signal_CFL = tkinter.Label(Modulating_Signal_C, text='f = ', justify='right', anchor="ne",
                                      font=tkinter.font.Font(family='Helvetica', size=11))
Modulating_Signal_CFL.grid(sticky='ne', row=1, column=0, pady=4)
Modulating_Signal_CFE = tkinter.Entry(Modulating_Signal_C, width=10, justify='center',
                                      font=tkinter.font.Font(family='Helvetica', size=11))
Modulating_Signal_CFE.insert(0, '5000')
Modulating_Signal_CFE.grid(sticky='n', row=1, column=1, pady=4)
Modulating_Signal_CFHZ = tkinter.Label(Modulating_Signal_C, text='HZ', justify='left', anchor="w",
                                       font=tkinter.font.Font(family='Helvetica', size=11))
Modulating_Signal_CFHZ.grid(sticky='w', row=1, column=2, pady=4)

Modulating_Signal_CPHL = tkinter.Label(Modulating_Signal_C, text='phase = ', justify='right', anchor="ne",
                                       font=tkinter.font.Font(family='Helvetica', size=11))
Modulating_Signal_CPHL.grid(sticky='ne', row=2, column=0, pady=4)
Modulating_Signal_CPHE = tkinter.Entry(Modulating_Signal_C, width=10, justify='center',
                                       font=tkinter.font.Font(family='Helvetica', size=11))
Modulating_Signal_CPHE.insert(0, '60')
Modulating_Signal_CPHE.grid(sticky='n', row=2, column=1, pady=4)
Modulating_Signal_CPHDEG = tkinter.Label(Modulating_Signal_C, text='deg', justify='left', anchor="w",
                                         font=tkinter.font.Font(family='Helvetica', size=11))
Modulating_Signal_CPHDEG.grid(sticky='w', row=2, column=2, pady=4)
# ---------------------------------------------------------------------------------------------------------------
# RIGHT FRAME LAST FRAME
Modulating_Signal_BUTTON = tkinter.LabelFrame(
    Modulating_Signals, labelanchor='n', borderwidth=0)
Modulating_Signal_BUTTON.grid(row=3, column=0, padx=4, pady=10)
button_Plot = tkinter.Button(Modulating_Signal_BUTTON, text="Plot", command=BUTTON_PRESSED,
                             width=10, height=1, font=tkinter.font.Font(family='Helvetica', size=13, weight='bold'))
button_Plot.grid(sticky='ne', row=0, column=0, padx=(200, 0), pady=4)


# ---------------------------------------------------------------------------------------------------------------
def callback():
    var.set(var.get() + 1)
    CTKi.after(500, callback)


def quit():
    """Cancel all scheduled callbacks and quit."""
    for after_id in CTKi.tk.eval('after info').split():
        CTKi.after_cancel(after_id)
    CTKi.destroy()
    print(' ----   CODE ENDS   ---- ')


var = customtkinter.IntVar()
callback()
CTKi.protocol('WM_DELETE_WINDOW', quit)
CTKi.mainloop()
