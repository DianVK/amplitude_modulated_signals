import tkinter
import copy
import math
import time
import customtkinter
import numpy as np
import matplotlib.pyplot as plt
from tkinter import ttk
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import AutoLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
from threading import Thread

print("==========================================================")
print('| |------------------------------------------------------|')
print('| |                 Signals and Systems                  |')
print('| |             Amplitude Modulated Signals              |')
print('| |------------------------------------------------------|')
print('| ©   2023 DIAN VELICHKOV KINANEV. All Rights Reserved.  |')
print('| |      Technical University Sofia - Branch Plovdiv     |')
print('| |                Leader of the project                 |')
print('| |            Dr.   Eng.   Iliya   Petrov               |')
print("==========================================================")


def heaviside(x):
    x[x > 0] = 1
    x[x == 0] = 0.5
    x[x < 0] = 0
    return x


def SetVitessAnimation(IntVal):
    '''
    Handle the animation vitesse
    '''
    global valueInterval
    valueInterval = abs(float(IntVal) - 200)


def RANGING(START, END, STEP):
    '''
    Calculate range between START, END with STEP
    '''
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
    global FirPlot2, fig2, ax2, tt, sctt, FIG2, fig1, ax1, t, y, FIG1, amplc, fc, phasec, combobox, ampl, f, phase, fsig, ax4, fr, a, FIG4
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
    fig1 = plt.figure(figsize=(6.5, 1.5), dpi=100, facecolor='#EBEBEB')
    ax1 = fig1.add_subplot()
    FIG1 = FigureCanvasTkAgg(figure=fig1, master=FRAME_fig_01)
    FIG1.draw()
    FIG1.get_tk_widget().place(x=-45, y=-10)
    ax1.tick_params(direction="in")
    ax1.xaxis.set_major_formatter(FuncFormatter(my_xformatter))  # Set up suplots .0
    ax1.yaxis.set_major_formatter(FuncFormatter(my_yformatter))  # Set up suplots .0
    ax1.plot(t, y, c='blue', linestyle='-', linewidth=0.7)  # Plot
    ax1.grid()  # grid plot
    ax1.xaxis.set_ticks(RANGING(min(t), max(t), (max(t) - min(t)) / 10))
    ax1.yaxis.set_major_locator(AutoLocator())
    ax1.set_xlim([min(t), max(t)])  # Set up x limit
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
    ax2.xaxis.set_ticks(RANGING(min(tt), max(tt) + (max(tt) - min(tt)) / 100, (max(tt) - min(tt)) / 10))
    ax2.yaxis.set_major_locator(AutoLocator())
    ax2.plot(tt, sctt, c='blue', linestyle='-', linewidth=0.7)
    ax2.set_xlim([min(tt), max(tt)])
    # --------------------------------------------------------------------------
    sc = amplc * np.cos(2 * np.pi * fc * t + phasec * np.pi / 180)
    smod = (amplc + y) * np.cos(2 * np.pi * fc * t + phasec * np.pi / 180)
    # THIRD PLOT --------------------------------------------------------------
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
    ax3.yaxis.set_major_locator(AutoLocator())
    ax3.plot(t, smod, c='blue', linestyle='-', linewidth=0.7)
    ax3.set_xlim([min(t), max(t)])
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
    ax4.stem(fr, a, 'blue')
    ax4.set_xlim(k)
    ax4.set_ylim([0, max(a) + 1])


# Function Animation callback
def ANIMATION_BUTTON(fig2, ax2, tt, sctt, FIG2, fig1, ax1, t, y, FIG1, amplc, fc, phasec, val, ampl, f, phase, fsig,
                     fig4, ax4, fr, a, FIG4, valueInterval):
    global FirPlot1, FirPlot2, animation_1, animation_2, k, n
    # Remove the Previous Animation.
    try:
        animation_1, animation_2 = None, None
        ax1.lines.remove(FirPlot1)
        ax2.lines.remove(FirPlot2)
        ax4.stem(fr, a, 'blue')
        FIG4.draw()
    except:
        pass

    # ANIMATION FIGURE 2 ------------------
    def update2(i):
        # Animation Fig 1
        global k, FirPlot2
        k = k + 0.1
        sctti = (heaviside(tt - i) - heaviside(tt - 50 / fc + i)) * amplc * np.cos(
            2 * np.pi * fc * k * tt + phasec * np.pi / 180)
        FirPlot2.set_data(tt, sctti)
        if i == 25 / fc:
            thread1 = Thread(target=AnimationFig_04, daemon=True)
            thread1.start()
            thread2 = Thread(target=CallSecPlot, daemon=True)
            thread2.start()
            return FirPlot2
        return FirPlot2

    def AnimationFig_04():
        # Stop the animation for fig 2 and plot the corespond Fig 4 Animation
        tti = copy.deepcopy(tt)
        index = np.where(tti == np.median(tti))[0][0]
        tti[index + 1] = tti[index]
        sc = np.zeros(sctt.shape[0])
        sc[index] = max(sctt)
        sc[index + 1] = min(sctt)
        FirPlot2.set_data(tti, sc)
        FIG2.draw()
        ind = int(np.floor(len(fr) / 2))
        thirdplot = ax4.stem(fr[ind], a[ind], 'red')
        FIG4.draw()
        time.sleep(1)
        sc = np.zeros(sctt.shape[0])
        FirPlot2.set_data(tti, sc)
        FIG2.draw()

    # Set up figure
    FirPlot2, = ax2.plot(tt, sctt, c='red', linestyle='-', linewidth=0.7)
    frames2 = RANGING(0, 25 / fc, 0.1e-3)
    k = 1
    paused2 = False
    # Create the animation
    animation_2 = FuncAnimation(fig2, update2, frames=frames2, interval=valueInterval, repeat=False)
    FIG2.draw()

    # ------------
    # ANIMATION FIGURE 01 ---------
    def update1(j):
        # Animation fig 1
        global k, n, TARG, END, FirPlot1
        k = k + 1
        yi = (heaviside(t - j) - heaviside(t - 2 / fsig + j)) * ampl[n] * np.cos(
            2 * np.pi * f[n] * k * t + phase[n] * np.pi / 180)
        FirPlot1.set_data(t, yi)
        if j == END - 0.4e-3:
            TARG = copy.deepcopy(yi)
        if j == END and val <= 4:
            thread1 = Thread(target=animationSecondFig4, args=(np.max(TARG), np.min(TARG), n, val), daemon=True)
            thread1.start()
            K = 1
            n += 1
            thread2 = Thread(target=ContinueAnimation, daemon=True)
            thread2.start()
        return FirPlot1

    def animationSecondFig4(maxi, mini, ni, val):
        # Stop the animation and plot the corespond Fig 4 animation
        index = np.where(t == np.median(t))[0][0]
        ti = t
        ti[index + 1] = ti[index]
        yii = np.zeros(t.shape[0])
        yii[index] = maxi
        yii[index + 1] = mini
        FirPlot1.set_data(ti, yii)
        FIG1.draw()
        ind = int(np.floor(len(fr) / 2))
        thirdplot = ax4.stem(fr[n - 1], a[n - 1], 'red')
        thirdplot = ax4.stem(fr[-n], a[-n], 'red')
        FIG4.draw()
        time.sleep(1)
        if n == val:
            yii = np.zeros(ti.shape[0])
            FirPlot1.set_data(ti, yii)
            FIG1.draw()

    def CallSecPlot():
        # Start the Fig 1 Animation
        global k, n, TARG, FirPlot1, animation_1, END
        time.sleep(1.5)
        FirPlot1, = ax1.plot(t, y, c='red', linestyle='-', linewidth=0.7)
        n = 0
        k = 1
        TARG = None
        # Create the animation
        frames1 = RANGING(0, 1 / fsig, 0.4e-3)
        END = frames1[-1]
        animation_1 = FuncAnimation(fig1, update1, frames=frames1, interval=valueInterval, repeat=False)
        FIG1.draw()

    def ContinueAnimation():
        # create 2,3 and 4 animation for the first fig.
        if n == val:
            return
        time.sleep(1.5)
        frames1 = RANGING(0, 1 / fsig, 0.4e-3)
        animation_1 = FuncAnimation(fig1, update1, frames=frames1, interval=valueInterval, repeat=False)
        FIG1.draw()


# -------------------------------------------------------------------------------------------------------------

# Code started ------------------------------------------------------------------------------------------------
# Global Variables
fig2 = None;
ax2 = None;
tt = None;
sctt = None;
FIG2 = None
fig1 = None;
ax1 = None;
t = None;
y = None;
FIG1 = None
fig4 = None;
ax4 = None;
fr = None;
a = None;
FIG4 = None
valueInterval = 50

# Create Tkinter Window
CTKi = customtkinter.CTk()
CTKi.title("Amplitude Modulated Signals by Dian Kinanev")
CTKi.geometry(f"{890}x{560}+{10}+{10}")
CTKi.config(bg="#ebebeb")
print(' ---- CODE  STARTED ---- ')
print(' ----  GUI WORKING  ---- ')

font = tkinter.font.Font(family='Helvetica', size=10, weight='bold')
# RIGHT FRAME
Modulating_Signals = tkinter.LabelFrame(CTKi, labelanchor='n', )
Modulating_Signals.pack(fill='y', expand=True, side='top', anchor='e', padx=4, pady=4)
# RIGHT FRAME TOP FRAME
Modulating_SignalsFR1 = tkinter.LabelFrame(Modulating_Signals, labelanchor='n', borderwidth=0)
Modulating_SignalsFR1.grid(row=0, column=0, padx=4, pady=4)
# RIGHT FRAME TOP FRAME FIRST FRAME Modulating Signal 1
Modulating_Signal_1 = tkinter.LabelFrame(Modulating_SignalsFR1, text='  Modulating \n  Signal 1  ', labelanchor='n',
                                         borderwidth=1.5, relief='solid', font=font)
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
FRAME_fig_04 = tkinter.Frame(CTKi, height=140, width=560)
FRAME_fig_04.place(x=10, y=460)
HZ = tkinter.Label(CTKi, text=' Hz', bg="#ebebeb", font=tkinter.font.Font(family='Helvetica', size=13))
HZ.place(x=570, y=580)
S1 = tkinter.Label(CTKi, text='S', bg="#ebebeb", font=tkinter.font.Font(family='Helvetica', size=13))
S1.place(x=570, y=130)
S2 = tkinter.Label(CTKi, text='S', bg="#ebebeb", font=tkinter.font.Font(family='Helvetica', size=13))
S2.place(x=570, y=280)
S3 = tkinter.Label(CTKi, text='S', bg="#ebebeb", font=tkinter.font.Font(family='Helvetica', size=13))
S3.place(x=570, y=430)


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
    Modulating_Signal_1 = tkinter.LabelFrame(Modulating_SignalsFR1, text='  Modulating \n  Signal 1  ', labelanchor='n',
                                             borderwidth=1.5, relief='solid', font=font)
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
Modulating_Signal_BUTTON = tkinter.LabelFrame(Modulating_Signals, labelanchor='n', borderwidth=0)
Modulating_Signal_BUTTON.grid(row=3, column=0, padx=4, pady=0)
button_Plot = tkinter.Button(Modulating_Signal_BUTTON, text="Plot", command=BUTTON_PRESSED, width=10, height=1,
                             font=tkinter.font.Font(family='Helvetica', size=13, weight='bold'))
button_Plot.grid(sticky='ne', row=0, column=1, padx=(40, 0), pady=4)
Animation = tkinter.Button(Modulating_Signal_BUTTON, text="Animation",
                           command=lambda: ANIMATION_BUTTON(fig2, ax2, tt, sctt, FIG2, fig1, ax1, t, y, FIG1, amplc, fc,
                                                            phasec, combobox, ampl, f, phase, fsig, fig4, ax4, fr, a,
                                                            FIG4, valueInterval), width=10, height=1,
                           font=tkinter.font.Font(family='Helvetica', size=13, weight='bold'))
Animation.grid(sticky='ne', row=0, column=0, padx=(0, 40), pady=4)
TrivalLabel = tkinter.Label(Modulating_Signal_BUTTON, text="")
TrivalLabel.grid(sticky='ne', row=1, column=0, padx=(0, 40), pady=(4, 10))
scale = tkinter.Scale(Modulating_Signal_BUTTON, from_=0, to=200, resolution=10, orient='horizontal',
                      command=SetVitessAnimation, sliderlength=10, length=110, width=10, troughcolor='#008080',
                      font=("Helvetica", 9), showvalue=False)
scale.place(x=1, y=55)
Slow = tkinter.Label(Modulating_Signal_BUTTON, text="Slow", font=("Helvetica", 9, 'bold'))
Slow.place(x=0, y=37)
Fast = tkinter.Label(Modulating_Signal_BUTTON, text="Fast", font=("Helvetica", 9, 'bold'))
Fast.place(x=85, y=37)


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
