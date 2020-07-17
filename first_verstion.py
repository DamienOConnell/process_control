#!/usr/bin/env python3

import psutil
from datetime import datetime
import pandas as pd
import time
import os
from pprint import pprint


def printproc(proc: dict):

    print(f"name: {proc['name']}")
    print(f"pid: {proc['pid']}")
    print(f"cores: {proc['cores']}")
    print(f"cpu_usage: {proc['cpu_usage']}")


def getargs():
    import argparse

    # parser = argparse.ArgumentParser(prog='PROCMON')
    parser = argparse.ArgumentParser(
        description="Process monitoring.", epilog="Track a process status",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-p", "--pid", type=int, help="Provide a pid to track.")
    group.add_argument("-n", "--name", help="Provide a process name to track.")
    parser.add_argument(
        "-u",
        "--live-update",
        action="store_true",
        help="Whether to keep the program on and updating process information each second",
    )
    args = parser.parse_args()

    return args


def getproclist():
    proclist = []
    for process in psutil.process_iter():

        # nextproc = {}
        # get all process info in one shot
        with process.oneshot():
            # get the process id
            if process.pid == 0:
                # System Idle Process for Windows NT, useless to see anyways
                continue
            pid = process.pid

            # get the name of the file executed
            name = process.name()

            # get the time the process was spawned
            try:
                create_time = datetime.fromtimestamp(process.create_time())
            except OSError:
                # system processes, using boot time instead
                create_time = datetime.fromtimestamp(psutil.boot_time())

            # get the number of CPU cores that can execute this process
            try:
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0

            # get the CPU usage percentage
            cpu_usage = process.cpu_percent()

            # get the status of the process (running, idle, etc.)
            status = process.status()

            proclist.append(
                {
                    "pid": pid,
                    "name": name,
                    "create_time": create_time,
                    "cores": cores,
                    "cpu_usage": cpu_usage,
                    "status": status,
                }
            )

    print("Finished populating the proclist")
    return proclist


def getprocbyname(proclist, procname):
    #
    # There can be multiple processes with the same name.
    # Need to return a list of matches, not a single match.
    #
    foundlist = []
    for proc in proclist:
        if proc["name"] == procname:
            printproc(proc)
            foundlist.append(proc)
    return None


def getprocbypid(proclist, procpid):
    for proc in proclist:
        if proc["pid"] == procpid:
            return proc
    return None


def printproclist(proclist: list) -> None:

    if len(proclist) > 0:
        print(f"Processes with name: {proc['name']}")
        for p in proclist:
            print(f"pid: {proc['pid']}")
            print(f"cores: {proc['cores']}")
            print(f"cpu_usage: {proc['cpu_usage']}\n\n")


# def construct_dataframe(processes):
#     # convert to pandas dataframe
#     df = pd.DataFrame(processes)
#     # set the process id as index of a process
#     df.set_index("pid", inplace=True)
#     # sort rows by the column passed as argument
#     df.sort_values(sort_by, inplace=True, ascending=not descending)
#     # pretty printing bytes
#     df["memory_usage"] = df["memory_usage"].apply(get_size)
#     df["write_bytes"] = df["write_bytes"].apply(get_size)
#     df["read_bytes"] = df["read_bytes"].apply(get_size)
#     # convert to proper date format
#     df["create_time"] = df["create_time"].apply(
#         datetime.strftime, args=("%Y-%m-%d %H:%M:%S",)
#     )
#     # reorder and define used columns
#     df = df[columns.split(",")]
#     return df


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
