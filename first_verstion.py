#!/usr/bin/env python3

import psutil
from datetime import datetime
import pandas as pd
import time
import os
from pprint import pprint

def getargs():
    import argparse

    # parser = argparse.ArgumentParser(prog='PROCMON')
    parser = argparse.ArgumentParser(
        description="Process monitoring.",
        epilog="Track a process status",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--pid", type=int, help="Provide a pid to track.")
    group.add_argument("-n", "--name", help="Provide a process name to track.")
    args = parser.parse_args()

    return args


def getproclist():
    proclist = []
    for process in psutil.process_iter():

        nextproc = {}
        # get all process info in one shot
        with process.oneshot():
            # get the process id
            if process.pid == 0:
                # System Idle Process for Windows NT, useless to see anyways
                continue
            nextproc['pid'] = process.pid
            # get the name of the file executed
            nextproc['name'] = process.name()
            
            # get the time the process was spawned
            try:
                nextproc['create_time'] = datetime.fromtimestamp(process.create_time())
            except OSError:
                # system processes, using boot time instead
                nextproc['create_time'] = datetime.fromtimestamp(psutil.boot_time())
            try:
                # get the number of CPU cores that can execute this process
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0
            nextproc['cores'] = cores
            # get the CPU usage percentage
            nextproc['cpu_usage'] = process.cpu_percent()

        proclist.append(nextproc)
    print("Finished populating the proclist")
    return proclist

def getprocbyname(proclist, procname):
    #
    # There can be multiple processes with the same name. 
    # Need to return a list of matches, not a single match.
    #
    foundlist = []
    for proc in proclist:
        if proc['name'] == procname:
            print(f"proc['name'] is {proc['name']}")
            print(f"procname is {procname}")
            foundlist.append(proc)
    return None

def getprocbypid(proclist, procpid):
    for proc in proclist:
        if proc['pid'] == procpid:
            return proc
        else:
            print(f"no match:  proc['pid']")
    return None
    
def printproclist(proclist: list) -> None:
    for p in proclist: 
        pprint(p)

def main():
    args = getargs()
    pidofinterest = {}
    proclist = getproclist()

    # breakpoint()

    if args.name:
        print(f"looking for name: {args.name}")
        pidofinterest = getprocbyname(proclist, args.name)
    elif args.pid:
        print(f"looking for pid: {args.pid}")
        pidofinterest = getprocbypid(proclist, args.pid)
    
    pprint(pidofinterest)

    
if __name__ == "__main__":
    main()
