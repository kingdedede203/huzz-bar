#!/usr/bin/env python

import os
import socket
import subprocess

from json import loads, dumps


def get_workspaces(active_workspace_id):
    return [
        {
            "id": workspace_id,
            "active": active_workspace_id == workspace_id,
        }
        for workspace in sorted(
            loads(subprocess.check_output("hyprctl -j workspaces", shell=True)),
            key=lambda x: x["id"],
        )
        if (workspace_id := workspace["id"]) > 0 # ignore magic workspace
    ]


SOCKET_PATH = (
    f"{os.getenv('XDG_RUNTIME_DIR')}/hypr/"
    f"{os.getenv('HYPRLAND_INSTANCE_SIGNATURE')}/.socket2.sock"
)

initial_active_workspace = loads(subprocess.check_output("hyprctl -j activeworkspace", shell=True))["id"]
initial_workspaces = get_workspaces(initial_active_workspace)
print(dumps(initial_workspaces), flush=True)

with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
    sock.connect(SOCKET_PATH)
    while True:
        data = sock.recv(1024).decode()
        if not data:
            continue
        for event in data.splitlines():
            if event:
                event_type, event_data = event.split(">>")
                match event_type, event_data:
                    case "workspace", _:
                        workspaces = get_workspaces(int(event_data))
                        print(dumps(workspaces), flush=True)
                    case "createworkspace", "special:magic":
                        subprocess.run(
                            "eww update magic_workspace_active=true",
                            shell=True,
                        )
                    case "destroyworkspace", "special:magic":
                        subprocess.run(
                            "eww update magic_workspace_active=false",
                            shell=True,
                        )
