#!/usr/bin/env python3
import requests
import getpass
import os
import time
import sys
from time import sleep
import threading
from utils import *

def youtube_rtmp(key):
    os.system("ffmpeg -re -i http://10.5.5.9:8080/live/amba.m3u8 -c copy -c:a aac -strict experimental -b:a 96k -ac 2 -ar 44100 -f flv rtmp://a.rtmp.youtube.com/live2/%s" % key)


def video():
    os.system(
        "ffplay -fflags nobuffer -f:v hls http://10.5.5.9:8080/live/amba.m3u8")

def keepalive(pwd):
    while True:
        os.system(
            "curl -s -X GET http://10.5.5.9/camera/PV?t=%s&p=%s" % (pwd, "%02"))
        sleep(20)

class keep_alive_thread (threading.Thread):
    def __init__(self, threadID, name, pwd):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        print("Starting " + self.name)
        keepalive(pwd)
        print("Exiting " + self.name)



print("what is the password of your camera?")
if get_prefs("password") != None:
    choice = input(
        "do you want to use the \"%s\" password? [Y/n] " % get_prefs("password"))
    if choice == "y" or choice == "Y" or choice == "":
        pwd = get_prefs("password")
    else:
        pwd = getpass.getpass("password: ")
        choice = input("Do you want to save this password? [Y/n] ")
        if choice == "y" or choice == "Y" or choice == "":
            save_prefs("password", pwd)
else:
    pwd = getpass.getpass("password: ")
    save_prefs("password", pwd)


thread1 = keep_alive_thread(1, "Thread-1", pwd)


thread1.start()
time.sleep(3.0)

choice = input("do you want to stream to youtube? [y/n] ")
if choice == "y":
    print("what is the youtube key?")
    if get_prefs("key") != None:
        choice = input(
            "do you want to use the \"%s\" key? [Y/n] " % get_prefs("key"))
        if choice == "y" or choice == "Y" or choice == "":
            key = get_prefs("key")
        else:
            key = input("key: ")
            choice = input("Do you want to save this key? [Y/n] ")
            if choice == "y" or choice == "Y" or choice == "":
                save_prefs("key", key)
    else:
        key = input("key: ")
        save_prefs("key", key)

    youtube_rtmp(key)
if choice == "n":
    video()


exit(0)
