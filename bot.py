# simple twitch bot v 1.0
# using python 2.7

import config
import utils
import socket
import re
import time
import thread
from time import sleep



def main():
    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN {}\r\n".format(config.CHAN).encode("utf-8"))

    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.mess(s, "What's up, everybody?")

    thread.start_new_thread(utils.fillOpList, ())
    while True:
        response = s.recv(1024).decode(("utf-8"))
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        else:
            username = re.search(r"\w+ ", response).group(0)
            message = chat_message.sub("", response)
            print(response)


            if message.strip() == "!time":
                utils.mess(s, "it's currently" + time.strftime("%I:%M %p %Z on %A %B %d %Y"))
            if message.strip() == "!messages" and utils.isOp(username):
                utils.mess(s, "Hello there!")
                utils.mess(s, "Press follow button! This really helps me :-)")
            sleep(1)




if __name__ == "__main__":
    main()