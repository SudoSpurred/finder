import os
import sys
import time
import requests
from telethon import TelegramClient, sync
from telethon.errors import FloodWaitError
from telethon.tl.functions.messages import GetPeerDialogsRequest as check

aLongTimeAgo = True
otherStatus = False
dateAsStatus = True


def file_exists(file):
    return file in os.listdir()


def file_put_contents(file, contents):
    open(file, "w+").write(contents)


def getUsers(file):
    users = []
    file = open(file, "r")
    for user in file.read().split('\n'):
        if user != "":
            users.append(user)
    return users


def putUsers(users, File):
    file = open(File, "w")
    if len(users) == 0:
        file_put_contents(File, "")
        return
    for user in users:
        file.write(user + "\n")


def valid_user(user):
    if len(user) > 4:
        req = requests.get(f"https://t.me/{user}").text
        if "tgme_page_extra" in req and "subscribers" not in req and "members" not in req and "subscriber" not in req and "member" not in req:
            return True
    return False


if not file_exists("in.txt"):
    os.system("nano in.txt")

if file_exists("in.txt"):
    if len(getUsers("in.txt")) == 0:
        os.system("nano in.txt")

try:
    os.remove('finder.session')
except Exception as e:
    print(e)


with TelegramClient("finder.session", 1306017, '3fc2875ef8b2baefc7764eba474606fe') as client:
    token = input("add a bot to a channel and make it admin then send me it's token\nEnter Token: ")
    channelToSend = input("chant id of that channel (without -100): ")
    usernames = getUsers("in.txt")
    client.send_message('me', "starting...")
    for username in usernames:
        if valid_user(username):
            print(f"trying: @{username}")
            try:
                wtf = client(check([username]))
                data = wtf.users[0].status
                if len(wtf.users) <= 1:
                    raise Exception("username unreachable")
                if "UserStatusOffline" in str(data):
                    res = data.was_online
                    if not dateAsStatus:
                        res += " False"
                elif "None" in str(data):
                    res = "a long time ago"
                    if not aLongTimeAgo:
                        res += " False"
                else:
                    res = (str(data).replace("(", "").replace(")", ""))
                    if not otherStatus:
                        res += " False"
            except FloodWaitError as error:
                sec = int(error.seconds)
                print(f"floodWait occurred - sleeping {int(sec/60)} minutes")
                time.sleep(sec)
            except Exception as e:
                res = "Error - " + str(e) + " - False"
            print(f"@{username} - {res}")
            if "False" not in str(res):
                client.send_message('me', f"@{username} - {res}")
                requests.post('https://api.telegram.org/bot{}/sendMessage'.format(token), data={
                        'chat_id': int("-100" + channelToSend) ,
                        'text': f"@{username} - {res}"
                    })
        else:
            print(f"bad: @{username}")
        edit = getUsers("in.txt")
        edit.remove(username)
        putUsers(edit, "in.txt")
    client.send_message('me', "Done")
