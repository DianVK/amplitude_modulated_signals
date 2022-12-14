# importing libraries:
# -------------------
import math
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.ticker import FuncFormatter
print("==========================================================")
print('| |------------------------------------------------------|')
print('| |                 Signals and Systems                  |')
print('| |             Amplitude Modulated Signals              |')
print('| |------------------------------------------------------|')
print('| ©   2022 DIAN VELICHKOV KINANEV. All Rights Reserved.  |')
print("==========================================================")

print('-----------------------------------------------')
print(' COMMENTS:                                     ')
print(' Main function Executes on button press in UI  ')
print(' Index in python start from 0 while for matlab start from 1')
print(' calculating 4 graphs depending on the UI inputs data and display them on the UI')
print('-----------------------------------------------')

# -------------------------------------------------------------
# UseFull Function
def RANGING(START, END, STEP):
    # Calculate range between START, END with STEP
    # exmmple:
    # START = 1, END = 2, STEP = 0.2
    # RANGE FISTE ITERATION = 1
    # RANGE FISTE ITERATION = 1.2
    # RANGE FISTE ITERATION = 1.4
    # RANGE FISTE ITERATION = 1.6
    # ...
    # LAST RANGE = [1 1.2 1.4 1.6 1.8 2]
    RANGE = []
    while START <= END:
        RANGE.append(START)
        START += STEP
    return RANGE

def my_formatter(x, pos):
    """
    source: https://stackoverflow.com/questions/8555652/removing-leading-0-from-matplotlib-tick-label-formatting
    Format 1 as 1, 0 as 0, and all values whose absolute values is between
    0 and 1 without the leading "0." (e.g., 0.7 is formatted as .7 and -0.4 is
    formatted as -.4)."""
    val_str = '{:g}'.format(x)
    if np.abs(x) > 0 and np.abs(x) < 1:
        return val_str.replace("0", "", 1)
    else:
        return val_str
# -------------------------------------------------------------
# GET VALUES FROM USER INTERFACE 
ampl  = []
f     = []
phase = []

val       = 2     # get the value from UI pop minue [1, 2, 3, 4] 
ampl.append(3)    # get the value from UI edit text for ampl1
f.append(100)     # get the value from UI edit text for f1
phase.append(100) # get the value from UI edit text for phase1
fsig = f[0]       # Calculate the greatest common divisors

if val >= 2:
    ampl.append(2)    # get the value from UI edit text for ampl2
    f.append(150)     # get the value from UI edit text for f2
    phase.append(30)  # get the value from UI edit text for phase2
    fsig = math.gcd(f[0],f[1]) # Calculate the greatest common divisors

if val >= 3:
    ampl.append(1.5)   # get the value from UI edit text for ampl3
    f.append(200)      # get the value from UI edit text for f3
    phase.append(60)   # get the value from UI edit text for phase3
    fsig = math.gcd(math.gcd(f[0],f[1]),f[2]) # Calculate the greatest common divisors

if val == 4:
    ampl.append(2)   # get the value from UI edit text for ampl4
    f.append(300)    # get the value from UI edit text for f4
    phase.append(45) # get the value from UI edit text for phase4
    fsig = math.gcd(math.gcd(math.gcd(f[0],f[1]),f[2]),f[3]) # Calculate the greatest common divisors

amplc  = 5     # get the value from UI last edit text for amplc
fc     = 5000  # get the value from UI last edit text for fc
phasec = 60    # get the value from UI last edit text for phasec

# change arrays to numpy arrays:
ampl  = np.array(ampl)
f     = np.array(f)
phase = np.array(phase)
# ------------------------------------------------------------------------

# FIRST PLOT # -----------------------------------------------------------
t = np.array(RANGING(0, 2/fsig, 1/fsig/1000))
y = np.array([0 for i in range(t.shape[0])])
for i in range(val):
    y = y + ampl[i] * np.cos(2 * np.pi * f[i] * t + phase[i] * np.pi/180)
# --------------------------------------------------------------------------
# SECOND PLOT --------------------------------------------------------------
tt   = np.array(RANGING(0, 50/fc, 1/fc/25))
sctt = amplc * np.cos(2*np.pi * fc * tt + phasec * np.pi/180)
# --------------------------------------------------------------------------
# THIRD PLOT ---------------------------------------------------------------
sc   = amplc * np.cos(2*np.pi * fc * t + phasec * np.pi/180)
smod = (amplc+y) * np.cos(2*np.pi * fc * t + phasec * np.pi/180)
# --------------------------------------------------------------------------
# FOURTH PLOT --------------------------------------------------------------
a  = [] 
fr = []
for i in range(val):
    a.append(ampl[i]/2)
    fr.append(fc-f[i])
a.append(amplc)
fr.append(fc)
for i in range(val - 1, -1, -1):
    a.append(ampl[i]/2)
    fr.append(fc+f[i])
k = [min(fr)- 3 * fsig, max(fr) + 3 * fsig]
XLim = k # limit axis
# ----------------------------------------------------------------------------

# PLOT SECTION ---------------------------------------------------------------
fig = plt.figure(figsize=(7,6.5),) # Set up figure size
major_formatter = FuncFormatter(my_formatter) # Set up ticks formatter.
plt.subplots_adjust(bottom= 0.04, top= 0.98)  # Set up suplots position

ax1 = plt.subplot(4,1,1) # FIRST PLOT -----------------
ax1.tick_params(direction="in")
ax1.xaxis.set_major_formatter(major_formatter) # Set up suplots position
ax1.yaxis.set_major_formatter(major_formatter) # Set up suplots position
ax1.plot(t, y,    c = 'blue', linestyle = '-', linewidth = 0.7) # Plot 
ax1.grid() # grid plot
ax1.set_xticks([0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04]) # Set up x ticks
ax1.set_xlim([0, t[-1]]) # Set up x limit
ax1.set_ylim([-10, 10])  # Set up y limit

ax2 = plt.subplot(4,1,2) # SEOND PLOT -----------------
ax2.tick_params(direction="in")
ax2.xaxis.set_major_formatter(major_formatter)
ax2.yaxis.set_major_formatter(major_formatter)
ax2.plot(tt, sctt, c = 'blue', linestyle = '-', linewidth = 0.7)
ax2.set_xticks([0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01])
ax2.set_xlim([0, tt[-1]])
ax2.set_ylim([-5, 5])

ax3 = plt.subplot(4,1,3) # THIRD PLOT -----------------
ax3.tick_params(direction="in")
ax3.xaxis.set_major_formatter(major_formatter)
ax3.yaxis.set_major_formatter(major_formatter)
ax3.plot(t,smod,   c = 'blue', linestyle = '-', linewidth = 0.7)
ax3.set_xticks([0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03, 0.035, 0.04])
ax3.set_xlim([0, t[-1]])
ax3.set_ylim([-20, 20])

ax4 = plt.subplot(4,1,4) # FOURTH PLOT -----------------
ax4.tick_params(direction="in")
ax4.xaxis.set_major_formatter(major_formatter)
ax4.yaxis.set_major_formatter(major_formatter)
ax4.stem(fr, a)
ax4.set_xlim(k)
ax4.set_ylim([0, 6])
plt.show()