#!/usr/bin/env python3


def get_processes_info():

    for process in psutil.process_iter():
      # get all process info in one shot
        with process.oneshot():
            # get the process id
            pid = process.pid
            if pid == 0:
                # System Idle Process for Windows NT, useless to see anyways
                continue
