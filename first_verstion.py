#!/usr/bin/env python3


import psutil
from datetime import datetime
import pandas as pd
import time
import os

for process in psutil.process_iter():
    # get all process info in one shot
    with process.oneshot():
        # get the process id
        pid = process.pid
        if pid == 0:
            # System Idle Process for Windows NT, useless to see anyways
            continue
        # get the name of the file executed
        name = process.name()

        # get the time the process was spawned
        try:
            create_time = datetime.fromtimestamp(process.create_time())
        except OSError:
            # system processes, using boot time instead
            create_time = datetime.fromtimestamp(psutil.boot_time())
        print(f"NAME: {name}, PID: {pid}")
