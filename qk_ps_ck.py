#!/usr/bin/env python3

import psutil
import time
from datetime import datetime

# local modules
import simple_smtp


def getargs():
    import argparse

    parser = argparse.ArgumentParser(
        description="Process monitoring.", epilog="Track a process status",
    )
    parser.add_argument(
        "-n", "--name", required=True, help="Provide a process name to track."
    )
    parser.add_argument(
        "-e",
        "--email",
        required=True,
        help="recipient for email notifications if process fails.",
    )
    parser.add_argument(
        "-u",
        "--live-update",
        action="store_true",
        help="Whether to keep the program on and updating process information each second",
    )
    args = parser.parse_args()

    return args


def checkIfProcessRunning(processName):
    """
    Check if there is any running process that contains the given name processName.
    """
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def findProcessIdByName(processName):
    """
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    """
    listOfProcessObjects = []
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            # Check if process name contains the given name string.
            if processName.lower() in pinfo["name"].lower():
                listOfProcessObjects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return listOfProcessObjects


def main():

    last_emailed = time.time() - 3601
    while True:
        # Only send an email every hour; it's OK to send now

        args = getargs()
        interesting_proc = args.name
        print(f"Checking status of process named: {args.name}")
        downmsgtitle = "Process " + args.name + " is down"
        downmsgbody = (
            "Process "
            + args.name
            + " is down, sending email once every hour to announce the fact. "
        )
        # Check if the process was running or not.
        if checkIfProcessRunning(interesting_proc):
            print(f"{interesting_proc} process - RUNNING")
        else:
            print(f"{interesting_proc} process - NOT RUNNING")
            if int(time.time() - last_emailed) > 3600:
                print(f"Process {interesting_proc} is down, sending message ...")
                # simple_smtp.sendgmailmessage(downmsgtitle, downmsgbody, args.email)
                last_emailed = time.time()
            else:
                print(
                    f"Process {interesting_proc} is down, no message, it's too soon ..."
                )

        if not args.live_update:
            print("Exiting, live updates will not be provided.")
            break
        else:
            time.sleep(10.0)


if __name__ == "__main__":
    main()
