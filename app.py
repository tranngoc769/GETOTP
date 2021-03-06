
import win32com.client
from os import extsep, path
import names
import requests
import logging
import lxml
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog,QMessageBox
import sys, time
from selenium import webdriver
from pynput.keyboard import Key, Listener
import pywinauto
from pywinauto import Application

import webbrowser   
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
from playsound import playsound
import sys, time
from pynput.keyboard import Key, Listener

import pyperclip
import re
import asyncio
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import csv
from PyQt5.QtGui import QIcon
from telethon import TelegramClient, client
from telethon.tl.functions.account import UpdateProfileRequest
from pywinauto.application import Application
from telethon.tl.functions.channels import JoinChannelRequest,LeaveChannelRequest
from gtts import gTTS
codeFile  = 'otpsound.mp3' 
import os
import win32gui
def codeToSpeech(code):
    try:
        newCode = ""
        for item in code:
            newCode+= " "+str(item)
        myobj = gTTS(text=newCode, lang='vi', slow=False,)
        myobj.save(codeFile)
        playsound(codeFile)
        time.sleep(2)
        playsound(codeFile)
        os.remove(codeFile)
    except:
        pass
    
def myplaysound(file):
    try:
        playsound(file)
    except:
        pass
DCOM_PATH = "C://Program Files (x86)/Mobile Partner/Mobile Partner.exe"
class PyShine_THREADS_APP(QtWidgets.QMainWindow):
    def enumWindowFunc(self,hwnd, windowList):
        text = win32gui.GetWindowText(hwnd)
        className = win32gui.GetClassName(hwnd)
        if 'chromedriver' in text.lower() or 'chromedriver' in className.lower():
            win32gui.ShowWindow(hwnd, False)
    def dcom(self):
        self.com = Application().start(DCOM_PATH, timeout=60)
        time.sleep(5)
        handles = pywinauto.findwindows.find_windows()
        for w_handle in handles:
            wind = self.com.window(handle=w_handle)
            if ('Mobile Partner' in wind.texts()):
                self.connectBtn = wind['DialupUIPlugin_ButtonConnect']
    def chrome(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--ignore-certificate-error")
        self.options.add_argument("--ignore-certificate-errors-spki-list")
        self.options.add_argument("--ignore-ssl-errors")
        self.options.add_argument('-no-sandbox')
        # self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--log-level=3')
        self.options.add_argument('-disable-dev-shm-usage')
        self.wd = webdriver.Chrome('chromedriver2.exe',options=self.options)
        self.wd.set_page_load_timeout(120)
        win32gui.EnumWindows(self.enumWindowFunc, [])
    def readAPI(self):
        f = open("api.bin", "r")
        self.API = f.read()
        self.API = self.API.strip()
    def __init__(self):
        self.currentPhone = ""
        self.AppOTP = ""
        self.OTP = ""
        QtWidgets.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = uic.loadUi('main.ui',self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("telegram.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.thread={}
        self.InputText.textChanged.connect(self.EditTextArea)
        self.CreatePhone.clicked.connect(self.GetPhone)
        self.thread[1] = ClipboardThreadClass(parent=None,index=1)
        self.thread[1].any_signal.connect(self.HandleCopyMessage)
        self.thread[1].start()
        # Create Btn
        self.Create.clicked.connect(self.CreateApp)
        # Continue
        self.Continue.clicked.connect(self.ContinueApp)
        # Change IP
        self.ChangeIP.clicked.connect(self.ChangeIPFunction)
        self.readAPI()
    # Next button --> Get login code
    def ContinueApp(self):
        self.thread[3].getOTPCode()
    # Open Chrome, Create APP #THREAD3
    def CreateApp(self):
        try:
            self.RegPhone.setText("")
            self.ApiHash.setText("")
            self.AppID.setText("")
            self.app_data = []
            self.thread[3] = ChromeThreadClass(parent=None,index=1,wd=self.wd)
            self.thread[3].any_signal.connect(self.ChromeResonse)
            self.thread[3].start()
        except:
            myplaysound('LOI.mp3')
               
    def ChangeIPFunction(self):
        try:
            self.connectBtn.click()
            time.sleep(2)
            self.connectBtn.click()
            time.sleep(4)
            self.Create.click()
        except:
            pass
    def ChromeResonse(self,event,data = []):
        if (event == 1):
            self.GetPhone()
            pass
        if (event == 2):
            # Fill number phone(only)
            pass
        if (event == 3):
            # Register, wait for code
            myplaysound('MXT.mp3')
            pass
        if (event==100):
            # Save data
            self.RegPhone.setText(data[2])
            self.ApiHash.setText(data[0])
            self.AppID.setText(data[1])
            self.thread[4] = VerifyAccountThreadClass(parent=None,index=1,app_data=data)
            self.thread[4].start()
            pass
    def GetPhone(self):
        try:
            try:
                os.system('cls' if os.name=='nt' else 'clear')
                self.InputText.setText("")
                self.OTPEdit.setText("")
                self.thread[2].stop()
            except :
                pass
            self.thread[2] = PhoneOTPTheadClass(parent=None,index=1, API = self.API)
            self.thread[2].any_signal.connect(self.HandlePHONEEmit)
            self.thread[2].start()
        except Exception as er:
            print(er)
    # Handle API Reponse
    def HandlePHONEEmit(self, event):
        s = pyperclip.paste()
        if (event==2):
            self.OTP.setText(str(s))
        else:
            self.Phone.setText(str(s))
            # Pass to chrome
            self.thread[3].registerPhone(str(s))
            
    # Copy message in telegram app
    def HandleCopyMessage(self, code):
        if (code == 1):
            s = pyperclip.paste()
            pyperclip.copy(s)
            myplaysound('CODE.mp3')
            self.InputText.setText("")
            self.OTPEdit.setText(str(s))
            try:
                print("COPY OTP = START APP")
                self.wd.find_element_by_id("my_password").send_keys(str(s))
                self.wd.execute_script('$(`button[type="submit"]`).click();')
                self.thread[3].StartCreateApp()
            except Exception as xxxx:
                print(xxxx)
                pass
        if code == 2:
            s = pyperclip.paste()
    def GetOTP(self):
        text = self.InputText.toPlainText()
        if (text==""):
            return ""
        if ("Web login code" in text):
            text = self.InputText.toPlainText().split('\n')
            try:
                for item in text:
                    if (len(item) == 5 or len(item) == 6 or (len(item) > 8 and len(item) < 13)):
                        return item.strip()
            except:
                pass
            return ""
        if ("Login code:" in text):
            xx = re.findall('\d+', text)
            if (len(xx)> 0):
                return xx[0]
            return ""
        return ""
    def EditTextArea(self):
        code = self.GetOTP()
        if (code != ""):
            pyperclip.copy(code)
            self.InputText.setText("")
            self.OTPEdit.setText(str(code))
class ClipboardThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None,index=0):
        super(ClipboardThreadClass, self).__init__(parent)
        self.index=index
        self.is_running = True
    def run(self):
        while 1:
            text = pyperclip.paste()
            if (text==""):
                pass
            if text.strip().isdecimal():
                if (len(text)==10 ):
                    try:
                        text = "+84"+text[1:10]
                        pyperclip.copy(text)
                        # self.any_signal.emit(1)
                    except:
                        pass
                pass
            if ("Web login code" in text):
                text = text.split('\n')
                try:
                    for item in text:
                        if (len(item) == 5 or len(item) == 6 or (len(item) > 8 and len(item) < 13)):
                            pyperclip.copy(item.strip())
                            self.any_signal.emit(1)
                except:
                    pass
            if ("Login code:" in text):
                xx = re.findall('\d+', text)
                if (len(xx)> 0):
                    pyperclip.copy(str(xx[0]))
                    self.any_signal.emit(2)
                    codeToSpeech(str(xx[0]))
            time.sleep(1)
class PhoneOTPTheadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None,index=0, API = None):
        super(PhoneOTPTheadClass, self).__init__(parent)
        self.API = API
        self.index=index
        self.is_running = True
    def run(self):
        data = None
        response = None  
        url = "https://trumotp.com/apiv1/order?apikey="+self.API+"&serviceId=269"
        myplaysound('GET.mp3')
        try:
            payload={}
            headers = {}
            response = requests.request("GET", url, headers=headers, data=payload)
            data =  response.json()
            if data['status'] == 1:
                trying = 1
                isOTP = False
                isPHONE = False
                id = str(data['id'])
                while trying < 280 and isOTP == False and self.is_running == True:
                    # test
                    trying += 1
                    time.sleep(1)
                    # id = 773836
                    url = "https://trumotp.com/apiv1/ordercheck?apikey="+self.API+"&id="+str(id)
                    payload={}
                    headers = {
                    'Cookie': 'ASP.NET_SessionId=5q0ixkfveukforhykvrqkmb4'
                    }
                    response = requests.request("GET", url, headers=headers, data=payload)
                    data =  response.json()
                    if data['status'] != 1:
                        isOTP = False
                        myplaysound('LOI.mp3')
                    else:
                        try:
                            resp = data['data']
                            phone = resp['phone']
                            phone = "+84"+phone[1:10]
                            if (isPHONE == False):
                                pyperclip.copy(phone.strip())
                                self.any_signal.emit(1)
                                isPHONE = True
                                myplaysound('SDT.mp3')
                            if (resp['code'] != "" and resp['code'] != None):
                                print(resp['code'])
                                isOTP = True
                                pyperclip.copy(resp['code'].strip())
                                self.any_signal.emit(2)
                                myplaysound('OTP.mp3')
                                codeToSpeech(str(resp['code'].strip()))
                                return
                            else:
                                pass
                        except  Exception as codeerr:
                            print(codeerr)
                            print(data)
                            myplaysound('LOI.mp3')
                    time.sleep(1)
            else:
                playsound("LOI.mp3")
        except Exception as xx:
            print(url)
            print(response)
            playsound("TRUMOTP.mp3")
    def stop(self):
        print("Stop")
        self.is_running = False
        self.any_signal.terminal()
class ChromeThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int,list)
    def __init__(self, parent=None,index=0, wd = None, app_data = None):
        super(ChromeThreadClass, self).__init__(parent)
        self.app_data = app_data
        self.index=index
        self.wd = wd
        self.isTry = 0
        self.is_running = True
    def run(self):
        self.wd.delete_all_cookies()
        self.wd.get('https://my.telegram.org/auth')
        self.any_signal.emit(1,[])
    def registerPhone(self,phone):
        self.phone = phone
        self.wd.find_element_by_xpath('//input[@id="my_login_phone"]').send_keys(phone)
        self.any_signal.emit(2,[])
    def getOTPCode(self):
        self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        self.any_signal.emit(3,[])
    def CheckSuccess(self, trying = 0):
        if (trying > 5):
            return False
        try:
            try:
                self.wd.find_element_by_xpath('//button[@id="app_save_btn"]').click()
                time.sleep(2)
            except:
                pass
            self.wd.find_element_by_xpath('//div[@class="app_lock_tt"]')
            return True
        except:
            myplaysound('ThuLai.mp3')
            time.sleep(3)
            return self.CheckSuccess(trying+1)
    def StartCreateApp(self):
        if (self.isTry > 3):
            self.isTry = 0
            return
        try:
            self.wd.get("https://my.telegram.org/apps")
            time.sleep(1)
            self.wd.find_element_by_xpath('//input[@id="app_title"]').send_keys(names.get_full_name())
            time.sleep(0.5)
            self.wd.find_element_by_xpath('//input[@id="app_shortname"]').send_keys(names.get_full_name())
            time.sleep(0.5)
            self.wd.find_element_by_xpath('//textarea[@id="app_desc"]').send_keys(names.get_full_name())
            time.sleep(2)
        except Exception as xxx:
            self.isTry += 1
            self.StartCreateApp()
            pass
        if (self.CheckSuccess()):
            # GET DATA , then emit
            data = self.wd.find_elements_by_css_selector(".uneditable-input")
            appid = data[0].text
            api_hash = data[1].text
            phone = self.phone
            print("API_HASH:  ", str(api_hash))
            print("APP_ID:  ", str(appid))
            print("PHONE:  ", str(self.phone))
            self.any_signal.emit(100,[str(api_hash),str(appid),  self.phone])
            self.any_signal.terminal()
        else:
            myplaysound('LOI.mp3')
            return
    def stop(self):
        print("Stop")
        self.is_running = False
        self.any_signal.terminal()
class VerifyAccountThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None,index=0, app_data = None):
        super(VerifyAccountThreadClass, self).__init__(parent)
        self.index=index
        self.data = app_data
        self.is_running = True
    def saveCSV(self):
        with open('accounts.csv', mode='a') as f:
            f.write(str(self.data[0].strip())+","+str(self.data[1])+","+str(self.data[2])+"\n")
    def run(self):
        print("LOGIN ACC")
        myplaysound('BATDAU.mp3')
        apihash = self.data[0]
        api_id = self.data[1]
        phone = self.data[2]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tele_client = TelegramClient(phone, api_id,apihash)
        tele_client.start(phone=phone)
        self.is_running = False
        self.saveCSV()
        myplaysound('HOANTHANH.mp3')
class ChangeiPThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None,index=0, window = None):
        super(ChangeiPThreadClass, self).__init__(parent)
        self.index=index
        self.is_running = True
        self.window = window
    def run(self):
        self.window.click()
        self.any_signal.terminal()
app = QtWidgets.QApplication(sys.argv)
mainWindow = PyShine_THREADS_APP()
try:
    mainWindow.dcom()
except:
    pass
mainWindow.chrome()
mainWindow.show()
sys.exit(app.exec_())