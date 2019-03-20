# utils.py
# A bunch of utility functions

import config
import urllib2
import json
import time
import thread
from time import sleep




def chat(sock, msg):
    sock.send("PRIVMSG #{} :{}\r\n".format(config.CHAN, msg))


def ban(sock, user):
    chat(sock, ".ban {}". format(user))


def timeout(sock, user, seconds = 600):
    chat(sock, ".timeout {}".format(user, seconds))


# http://tmi.twitch.tv/group/user/channel_name/chatters
def threadfillOpList():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/channel_name/chatters"
            req = urllib2.Request(url, headers={"accept": "*/*"})
            response = urllib2.urlopen(req).read()
            if response.find("502 Bad Gateway") == -1:
                config.oplist.clear()
                data = json.loads(response)
                for p in data["chatters"]["moderators"]:
                    config.oplist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    config.oplist[p] = "global_mod"
                for p in data["chatters"]["admins"]:
                    config.oplist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    config.oplist[p] = "staff"
        except:
            "Something went wrong. Do nothing."
    sleep(5)


def isOp(user):
    return user in config.oplist