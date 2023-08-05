import datetime
import time 
import sys, os
import requests
import logging
import socket
from tabulate import tabulate
from pathlib import Path
from pprint import pprint
from ..utils import dumps, abort, get_datafile
from subprocess import check_call, call
from P4 import P4, P4Exception
import shutil
from typing import Optional
log = logging.getLogger(__name__)

from typer import Context, launch, echo, secho, Option, Typer, confirm, prompt, style, progressbar

app = Typer()

hostname = socket.gethostname().lower()
SUBST_DRIVE = "S:"
path = f"{SUBST_DRIVE}\\sn2-main\\"
BASE_STREAM = "//Project/SN2-Main"
UE_STREAM = "//project/sn2-main-ue"

p4 = None

def connect_p4():
    p4_conn = P4()
    try:
        p4_conn.connect()
    except Exception as e:
        abort(f"Cannot establish connection with Perforce server: {e}...")
    return p4_conn


@app.callback()
def main():
    """
    Manage task streams.
    
    This tool is highly opinionated and expects you to be using the //Project/SN2-Main-UE stream and be working in a workspace called <username>_<label>_sn2-main
    """
    global p4
    p4 = connect_p4()
    ret = get_current_stream()
    client = get_current_client()
    
    if "Stream" not in ret:
        abort("Invalid workspace. You must be working in Streams to use this tool")
    stream_name = ret["Stream"]
    parent = ret["Parent"]
    secho(f"You are currently working in stream: {stream_name}", fg="blue")
    if parent.lower() != UE_STREAM and stream_name.lower() != UE_STREAM:
        abort(f"To use this tool you must be working in the {UE_STREAM} stream but your workspace is set on {stream_name}. Please change your workspace in p4v")

def get_task_streams():
    lst = p4.run_streams("-F", f"Owner=jonb Type=task baseParent={BASE_STREAM}")
    return lst

def get_current_stream():
    try:
        ret = p4.run_stream("-o")[0]
    except P4Exception as e:
        abort(f"Unable to get a stream from your current workspace. Make sure you are working in the {BASE_STREAM} stream.")
    return ret

def get_current_client():
    ret = p4.run_client("-o")[0]
    return ret

def get_clients():
    try:
        specs = p4.run_clients("-u", p4.user)
    except Exception as e:
        abort(str(e))
    ret = {}
    for s in specs:
        if "Stream" not in s:
            continue
        host = s["Host"].lower()
        if host == hostname or not host:
            ret[s["Stream"].lower()] = s
    return ret

def sync():
    s = confirm("Sync latest?")

    if not s:
        return
    
    secho(f"Syncing latest...")
    try:
        ret = p4.run_sync("-q", f"{path}UE/Subnautica2/...")
    except P4Exception as e:
        print(e)

@app.command()
def create(label: str = Option(None, prompt="Task branch label")):
    """
    Create a new task branch
    """
    if not label:
        abort("Aborted.")
    clients = get_clients()
    if get_current_stream()["Stream"].lower() != UE_STREAM:
        abort(f"Please switch to the {UE_STREAM} before creating a new task stream")

    ue_stream_client = None
    for k, c in clients.items():
        if k == UE_STREAM:
            ue_stream_client = c
    if not ue_stream_client:
        abort(f"You have no workspace mapped to the {UE_STREAM} stream. Please set one up.")

    ret = p4.run_opened()
    if (len(ret)):
        abort("You have opened files. Please revert or submit before creating new task stream.")


    #print(ue_stream_client)
    #task_client_name = ue_stream_client["client"] + "_task"
    #task_client = None
    #for k, c in clients.items():
    #    if c["client"] == task_client_name:
    #        echo(f"Reusing existin workspace {k}")
    #        task_client = c
    #        break
    # sync latest from parent
    echo("Syncing parent branch...")
    try:
        ret = p4.run_sync("-q", f"{path}...")
    except P4Exception as e:
        secho(str(e), fg="yellow")
        abort("Please fix the issues above before continuing")

    d = datetime.datetime.utcnow().isoformat().split("T")[0]
    label = label.replace(" ", "_").lower()
    stream_name = f"{p4.user}-{d}-{label}"
    full_stream_name = f"//Project/{stream_name}"
    secho(f"Creating task stream {stream_name} from {UE_STREAM}...")
    args = f"""
Stream: {full_stream_name}
Owner:  {p4.user}
Name:   {stream_name}
Parent: {UE_STREAM}
Type:   task
Description:
    Created by {p4.user}.
Options:        allsubmit unlocked toparent fromparent mergedown
ParentView:     inherit
Paths:
    share ...
"""
    p4.input = args
    ret = p4.run_stream("-i", "-t", "task")
    #print(ret[0])

    secho(f"Populating stream {full_stream_name}...")
    try:
        ret = p4.run_populate("-o", "-S", full_stream_name, "-r", "-d", "Initial branch")
    except P4Exception as e:
        if e.errors:
            secho(e.errors[0], fg="yellow")


    if 0:#not task_client:
        root = f"{ue_stream_client['Root']}_task"
        echo("Creating new workspace {task_client_name} -> {root}...")
        client_spec = f"""
Client: {task_client_name}
Owner:  {ue_stream_client['Owner']}
Host:   {ue_stream_client['Host']}
Description:
    Automatically created task workspace for {ue_stream_client['Owner']}

Root:   {root}
Options:        noallwrite noclobber nocompress unlocked nomodtime normdir
SubmitOptions:  submitunchanged
LineEnd:        local
Stream: {full_stream_name}"""
        p4.input = client_spec
        p4.run_client("-i")

    #p4.client = task_client_name
    secho(f"Switching current workspace {p4.client} to {full_stream_name}...")
    p4.run_client("-s", "-S", full_stream_name)
    ret = p4.run_client("-o")[0]
    root_path = ret["Root"]

#    if not task_client:
#        secho("Force syncing your new workspace folder to latest")
#        ret = p4.run_sync(f"{root}...#head")
#    else:
#        sync()


    ret = p4.run_stream("-o")[0]
    stream_name = ret["Stream"]
    parent = ret["Parent"]

    if ret["Type"] != "task":
        abort(f"Something went wrong. Current stream {stream_name} is not a task stream")

    # update the server without syncing
    ret = p4.run_sync("-q", "-k", f"{path}...")

    secho(f"You are now working in task stream {stream_name} from parent {parent}", bold=True, fg="green")

@app.command()
def switch():
    """
    Lists your current task streams and lets you switch between them
    """
    task_streams = get_task_streams()
    stream = get_current_stream()
    parent = None
    if stream["Type"] == "task":
        parent = stream["Parent"]
    for i, t in enumerate(task_streams):
        secho(f"{i+1} : {t['Stream']}")
    if parent:
        secho(f"0 : {parent}")
    
    if not task_streams:
        abort("You have no task streams. You can create one with the 'create' command")
    n = prompt("\nSelect a stream to work in")
    if n is None:
        abort("No stream selected")
    try:
        n = int(n)
    except:
        abort("Aborted.")
    if n == 0:
        new_stream = parent
    else:
        try:
            new_stream = task_streams[n-1]["Stream"]
        except:
            abort("Aborted.")
    
    secho(f"\nSwitching to stream {new_stream}", bold=True)
    try:
        p4.run_client("-s", "-S", new_stream)
    except P4Exception as e:
        abort(e)

    p4.run_sync("-q")


@app.command()
def mergedown():
    """
    Merge from parent into your current task branch
    """
    ret = p4.run_stream("-o")[0]
    stream_name = ret["Stream"]
    parent = ret["Parent"]
    if ret["Type"] != "task":
        abort(f"Current stream {stream_name} is not a task stream")

    ret = p4.run_client("-o")[0]
    root_path = ret["Root"]
    client = ret["Client"]

    ret = p4.run_opened()
    if (len(ret)):
        abort("Your default pending changelist must be empty.")

    secho(f"Integrating latest from parent {parent} to task stream {stream_name}...", bold=True)

    p4.input = f"""
Change: new
Client:	{client}
User:	{p4.user}

Description:
	Automatically merge {UE_STREAM} to {stream_name}

"""

    try:
        cmd = ["-Af", "-S", stream_name, "-r", f"{stream_name}/..."]
        ret = p4.run_merge(*cmd)
    except P4Exception as e:
        if e.errors:
            secho(e.errors[0], fg="red")
        if e.warnings:
            secho(e.warnings[0], fg="yellow")
        if "already integrated" in str(e):
            secho(f"Your task stream is already up to date with {UE_STREAM}", fg="green")
        return
    #ret = p4.run_opened()
    #for f in ret:
    try:
        ret = p4.run_resolve("-f", "-am", "-as", f"{root_path}/...")
    except P4Exception as e:
        echo(str(e))
    
    # p4 fstat -Olhp -Rco -e default //jonb_work_sn2-main/...
    try:
        ret = p4.run_fstat("-Olhp", "-Rco", "-e", "default", f"{root_path}/...")
    except P4Exception as e:
        echo(str(e))
    if not ret:
        abort("Your task stream is up to date.")

    unresolved = []
    for r in ret:
        if "unresolved" in r:
            unresolved.append(r)
            secho(f"  {r['clientFile']}... conflict", fg="yellow")
        else:
            secho(f"  {r['clientFile']}... ok", fg="green")
    
    if unresolved:
        y = confirm(f"\nOverwrite conflicting files in your task stream from {UE_STREAM}?")
        if not y:
            abort("Please resolve remaining files in p4v")
        for r in unresolved:
            ret = p4.run_resolve("-f", "-at", f"{r['clientFile']}")
        secho("Unresolved files have been overwritten by parent stream")

    try:
        ret = p4.run_fstat("-Olhp", "-Rco", "-e", "default", f"{root_path}/...")
    except P4Exception as e:
        echo(str(e))
    filelist = ""
    for r in ret:
        if "unresolved" in r:
            abort("There are still unresolved files in your pending changelist. Please resolve them in p4v")
        filelist += f"    {r['depotFile']}\n"

    mr = ""
    if unresolved:
        mr = f"{len(unresolved)} unresolvable files were overwritten."

    txt = f"""
Change: new
Client:	{client}
User:	{p4.user}

Description:
	Automatically merge {UE_STREAM} to {stream_name}. {mr}
Files:
{filelist}
"""
    p4.input = txt
    p4.run_submit('-i')

    try:
        ret = p4.run_resolve("-f", "-am", "-as", f"{root_path}/...")
    except P4Exception as e:
        if "no file(s) to resolve" not in str(e):
            raise
    try:
        ret = p4.run_fstat("-Olhp", "-Rco", "-e", "default", f"{root_path}/...")
    except P4Exception as e:
        if 'not opened on this client.' in str(e):
            secho(f"Your task stream is now up to date with {UE_STREAM}", fg="green")
            return
        else:
            echo(str(e))
    if not ret:
        secho(f"Your task stream is now up to date with {UE_STREAM}", fg="green")
    else:
        abort("Something is amiss. Your task stream is not up to date after the merge. Take a look at p4v")

@app.command()
def copyup():
    """
    Finish the task and copy into the parent stream
    """
    ret = p4.run_opened()
    if ret:
        abort("There are unsubmitted files in your workspace")

## p4 copy -Af -S //Project/jonb-2023-03-03-plugin_functional_tests //Project/SN2-Main/...
    ret = get_current_stream()
    stream_name = ret["Stream"]
    parent = ret["Parent"]
    if ret["Type"] != "task":
        abort(f"Current stream {stream_name} is not a task stream")
    
    echo(f"Switching to parent stream {parent}...")
    p4.run_client("-s", "-S", parent)

    p4.run_sync("-q")
    echo(f"Performing copy from {stream_name} to {ret['baseParent']}...")
    try:
        copy_ret = p4.run_copy("-Af", "-S", stream_name, ret["baseParent"] + "/...")
    except P4Exception as e:
        if "up-to-date" in str(e):
            secho(f"Nothing to do. Parent {parent} is identical to task stream {stream_name}", fg="green")
            return
        else:
            raise
    else:
        echo("Adding files...")
        for r in copy_ret:
            echo(f"  {r['fromFile']} -> {r['depotFile']}")

    secho(f"You can now submit your changelist to {parent} in p4v", fg="green")

@app.command()
def delete(current: Optional[bool] = Option(False, help="Delete the current task stream")):
    """
    Permanently delete a named task stream or your current one"""
    if current:
        ret = p4.run_stream("-o")[0]
        stream_name = ret["Stream"]
        parent = ret["Parent"]
        if ret["Type"] != "task":
            abort(f"Current stream {stream_name} is not a task stream")

        delete = confirm("Are you sure you want to delete the current task stream?")
    else:
        task_streams = get_task_streams()
        parent = None
        for i, t in enumerate(task_streams):
            secho(f"{i+1} : {t['Stream']}")
        
        if not task_streams:
            abort("You have no task streams.")
        n = prompt("\nSelect a stream to delete")
        try:
            n = int(n)
        except:
            abort("Aborted.")
        stream_name = task_streams[n-1]["Stream"]
        delete = confirm(f"Are you sure you want to delete the task stream {stream_name}?") 

    if delete:
        if current:
            secho(f"Switching to {parent}...")
            p4.run_client("-s", "-S", parent)
            ret = p4.run_sync("-q", f"{path}...")

        secho(f"Deleting task stream {stream_name}...")
        try:
            p4.run_stream("--obliterate", "-y", stream_name)
        except P4Exception as e:
            abort(str(e))
    else:
        abort("Aborted")
    ret = p4.run_sync("-q", "-k", f"{path}...")
    #sync()

