from unsplash.api import Api
from unsplash.auth import Auth
from pystray import MenuItem as item
import pystray
from PIL import Image
import pickle
import threading
import logging
import requests
import ctypes
import os
import win32gui, win32con

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class main:
    def __init__(self):
        self.console = win32gui.GetForegroundWindow()
        self.consoles = True
        self.banner()
        self.getauth()
        self.questtime()
        self.timercb()
        self.stray()

    def questtime(self):
        while True:
            min = input("\nSet the timer to how many minutes? ")
            try:
                assert min.isnumeric()
                sec = int(min) * 60
                self.sec = sec
                return
            except:
                logging.error("only number(second)")
    def stray(self):
        image = Image.open("utbc.jpg")
        menu = (item('show/hide', self.stray_hide_show), item('exit', self.stray_exit))
        self.icon = pystray.Icon("UTBackgroundChanger", image, "UTBackgroundChanger", menu)
        self.icon.run()
    def stray_hide_show(self):
        if self.consoles:
            # HIDE
            win32gui.ShowWindow(self.console, win32con.SW_HIDE)
            self.consoles = False
        else:
            # SHOW
            win32gui.ShowWindow(self.console, win32con.SW_SHOW)
            self.consoles = True
    def stray_exit(self):
        if not self.consoles:
            win32gui.ShowWindow(self.console, win32con.SW_SHOW)
            self.icon.visible = False
            self.icon.stop()
        self.closing()
    def changeb(self):
        try:
            rp = self.api.photo.random()
            url = rp[0].links.download
            result = requests.get(url)
            with open("randompic.jpg", "wb") as file:
                file.write(result.content)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.getcwd() + "\\randompic.jpg", 0)
            logging.info(f"background changed to {rp[0].id}")
            threading.Timer(self.sec, self.changeb).start()
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
    def timercb(self):
        logging.info(f"Timer setted to {self.sec} second.")
        print("-"*25, "STARTED", "-"*25)
        threading.Timer(self.sec, self.changeb).start()
    def getauth(self):
        logging.info("starting logging with UTBackgroundAPI.")
        try:
            with open("UTBackgroundAPI.", "rb") as dt:
                api = pickle.load(dt)


            self.randompic = api.photo.random()
            self.api = api
            logging.info("logged successfully")
            return
        except:
            logging.warning("UTBackgroundAPI. not found or OAuth faild")


        logging.info("starting logging with inputs")
        while True:
            print("\n")
            client_id = input("Enter client id: ")
            print("\n")
            client_secret = input("Enter client secret: ")
            print("\n")
            redirect_uri = input("Enter redirect uri: ")
            try:
                auth = Auth(client_id, client_secret, redirect_uri)
                api = Api(auth)
                self.randompic = api.photo.random()
                self.api = api
                logging.info("logged successfully")
                with open("UTBackgroundAPI.", "wb") as dt:
                    pickle.dump(api, dt)
                return
            except:
                logging.error("OAuth faild!!")
    def banner(self):
        bannertext = """
╭╮╱╭┳━━━━╮╭━━╮╱╱╱╱╱╱╭╮╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭╮
┃┃╱┃┃╭╮╭╮┃┃╭╮┃╱╱╱╱╱╱┃┃╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱┃┃
┃┃╱┃┣╯┃┃╰╯┃╰╯╰┳━━┳━━┫┃╭┳━━┳━┳━━┳╮╭┳━╮╭━╯┃
┃┃╱┃┃╱┃┃╱╱┃╭━╮┃╭╮┃╭━┫╰╯┫╭╮┃╭┫╭╮┃┃┃┃╭╮┫╭╮┃
┃╰━╯┃╱┃┃╱╱┃╰━╯┃╭╮┃╰━┫╭╮┫╰╯┃┃┃╰╯┃╰╯┃┃┃┃╰╯┃
╰━━━╯╱╰╯╱╱╰━━━┻╯╰┻━━┻╯╰┻━╮┣╯╰━━┻━━┻╯╰┻━━╯
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╭━╯┃
╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╱╰━━╯\n"""
        print(bannertext)
    def closing(self):
        try:
            input("Enter any key to close app..")
            os._exit(0)
        except KeyboardInterrupt:
            pass
        os._exit(0)

if __name__ == '__main__':
    main()