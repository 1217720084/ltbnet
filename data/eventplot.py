import matplotlib.pyplot as plt
import time
import numpy as np

from andes_addon.dime import Dime
dimec = Dime('EventPlot', 'tcp://192.168.1.200:5000')
dimec.start()

# mng = plt.get_current_fig_manager()
# mng.full_screen_toggle()

# make interactive
fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot
plt.ion()
ax.axis('off')
ax.set_aspect(1)
ax.set_xlim([0, 2])
ax.set_ylim([0, 2])

circle1 = plt.Circle((0, 0.6), 0.3, color='g',clip_on=False)
circle2 = plt.Circle((1, 0.6), 0.3, color='g')
circle3 = plt.Circle((2, 0.6), 0.3, color='g', clip_on=False)

artist1 = ax.add_artist(circle1)
artist2 = ax.add_artist(circle2)
artist3 = ax.add_artist(circle3)

ax.text(-0.25, 1.75, 'Event Detection', fontsize=18)

ax.text(1.3, 1.75, 'Time', fontsize=18)
time_var = ax.text(1.7, 1.75, '', fontsize=18)

ax.text(-0.25, 1.25, 'Generator \nTrip', fontsize=18)
ax.text(0.75, 1.25, 'Load \nShedding', fontsize=18)
ax.text(1.75, 1.25, 'Line \nTrip', fontsize=18)

light_last = np.array([0, 0, 0])
plt.show()
plt.pause(0.1)


while True:
    var = dimec.sync()

    if var:
        if var == 'EventResult':
            val = dimec.workspace[var]

            time_stamp = val['t']
            light_m = val['vars'].reshape((-1,))

            if light_m[0] == 1 and light_last[0] == 0:
                artist1.update({'color': 'r'})
            if light_m[1] == 1 and light_last[1] == 0:
                artist2.update({'color': 'r'})
            if light_m[2] == 1 and light_last[2] == 0:
                artist3.update({'color': 'r'})

            if light_m[0] == 0 and light_last[0] == 1:
                artist1.update({'color': 'g'})
            if light_m[1] == 0 and light_last[1] == 1:
                artist2.update({'color': 'g'})
            if light_m[2] == 0 and light_last[2] == 1:
                artist3.update({'color': 'g'})

            light_last = light_m

            time_var.set_text('{:.2f} s'.format(time_stamp))

            plt.draw()
            plt.pause(0.01)
            plt.show()
    else:
        time.sleep(0.02)


