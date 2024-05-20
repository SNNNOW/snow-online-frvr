import os
import sys
import json
import time
import requests
import websocket
from keep_alive import keep_alive

status = os.getenv("status") #online/dnd/idle

custom_status = os.getenv("custom_status") #If you don't need a custom status on your profile, just put "" instead of "youtube.com/@SealedSaucer"

# Custom activity with large image and buttons
custom_activity = {
    "name": "Hunain Store",
    "type": 1,  # 0 for playing
    "assets": {
        "large_image": "https://images-ext-1.discordapp.net/external/9ODrxPezNtClbm-tKUfEujZwa5vSMgMhakM0OpHU5Ow/%3Fsize%3D1024%26width%3D0%26height%3D320/https/cdn.discordapp.com/icons/1178390363027816619/a_4bdc0cb13ba8c32293831f96cfb717fb.gif?width=450&height=450",
        "large_text": "Hunain Store | .gg/hunainstore"
    },
    "buttons": [
        {
            "label": "❗❗ Store Join NOW !!",
            "url": "https://discord.gg/hunain store"
        },
    ]
}


usertoken = os.getenv("token")
if not usertoken:
    print("[ERROR] Please add a token inside Secrets.")
    sys.exit()

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers)
if validate.status_code != 200:
    print("[ERROR] Your token might be invalid. Please check it again.")
    sys.exit()

userinfo = requests.get("https://canary.discordapp.com/api/v9/users/@me", headers=headers).json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def onliner(token, status):
    ws = websocket.WebSocket()
    ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")
    start = json.loads(ws.recv())
    heartbeat = start["d"]["heartbeat_interval"]
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows",
            },
            "presence": {"status": status, "afk": False},
        },
        "s": None,
        "t": None,
    }
    ws.send(json.dumps(auth))
    cstatus = {
        "op": 3,
        "d": {
            "since": 0,
            "activities": [
                {
                    "type": 4,
                    "state": custom_status,
                    "name": "Custom Status",
                    "id": "custom",
                    #Uncomment the below lines if you want an emoji in the status
                    "emoji": {
                        "name": "NITRO_BOOST",
                        "id": "1191976619418603590",
                        "animated": True,
                    },
                }
            ],
            "status": status,
            "afk": False,
        },
    }
    ws.send(json.dumps(cstatus))
    online = {"op": 1, "d": "None"}
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps(online))

def run_onliner():
    os.system("clear")
    print(f"Logged in as {username}#{discriminator} ({userid}).")
    while True:
        onliner(usertoken, status)
        time.sleep(30)

keep_alive()
run_onliner()
