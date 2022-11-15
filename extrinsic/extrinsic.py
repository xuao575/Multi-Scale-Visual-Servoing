from sift.sift import sift
from PID import PID
import time
import numpy as np


def extrinsic_optimize():
    P = 0.5  # weight current errors more
    I = 0.1
    D = 0.01  # ignore future potential errors

    # In[3]:

    L = 50  # number of iterations

    # In[4]:

    pid = PID(P, I, D)

    pid.SetPoint = 0.0
    pid.setSampleTime(0.01)

    END = L
    feedback = 0

    feedback_list = []
    time_list = []
    setpoint_list = []

    for i in range(1, END):
        pid.update(feedback)
        output = pid.output
        if pid.SetPoint > 0:
            feedback += (output - (1 / i))
            print(feedback)
        if i > 9:
            pid.SetPoint = 1
        time.sleep(0.02)

        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)
        time_list.append(i)

    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)