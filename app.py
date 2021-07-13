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
import pyautogui
import webbrowser   
from bs4 import BeautifulSoup
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
from playsound import playsound
import sys, time
from pynput.keyboard import Key, Listener
import pyautogui
import pyperclip
import re
import asyncio
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import csv
from PyQt5.QtGui import QIcon
from telethon import TelegramClient, client
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import JoinChannelRequest,LeaveChannelRequest
class PyShine_THREADS_APP(QtWidgets.QMainWindow):
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
        self.wd = webdriver.Chrome('chromedriver_91.exe',options=self.options)
        self.wd.set_page_load_timeout(120)
    def __init__(self):
        self.currentPhone = ""
        self.AppOTP = ""
        self.OTP = ""
        QtWidgets.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.ui = uic.loadUi('main.ui',self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("auto.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
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
    # Next button --> Get login code
    def ContinueApp(self):
        self.thread[3].getOTPCode()
    # Open Chrome, Create APP #THREAD3
    def CreateApp(self):
        self.app_data = []
        self.thread[3] = ChromeThreadClass(parent=None,index=1,wd=self.wd)
        self.thread[3].any_signal.connect(self.ChromeResonse)
        self.thread[3].start()
    def ChromeResonse(self,event,data = []):
        print("ChromeResonse")
        if (event == 1):
            self.GetPhone()
            pass
        if (event == 2):
            # Fill number phone(only)
            pass
        if (event == 3):
            # Register, wait for code
            playsound('MXT.mp3')
            pass
        if (event==100):
            # Save data
            print(data)
            self.thread[3] = VerifyAccountThreadClass(parent=None,index=1,app_data=data)
            self.thread[3].start()
            pass
    def GetPhone(self):
        try:
            self.thread[2].stop()
        except :
            pass
        self.thread[2] = PhoneOTPTheadClass(parent=None,index=1)
        self.thread[2].any_signal.connect(self.HandlePHONEEmit)
        self.thread[2].start()
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
            playsound('CODE.mp3')
            self.InputText.setText("")
            self.OTPEdit.setText(str(s))
            try:
                self.wd.find_element_by_id("my_password").send_keys(str(s))
                self.wd.execute_script('$(`button[type="submit"]`).click();')
                self.thread[3].StartCreateApp()
            except Exception as xxxx:
                print(xxxx)
                pass
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
                        print(text)
                        self.any_signal.emit(1)
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
                    self.any_signal.emit(1)
            time.sleep(1)
class PhoneOTPTheadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None,index=0):
        super(PhoneOTPTheadClass, self).__init__(parent)
        self.index=index
        self.is_running = True
    def run(self):
        url = "https://trumotp.com/apiv1/order?apikey=c97fe40e988206184a05e204efd8090&serviceId=269"
        payload={}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        data =  response. json()
        print("CREATE PHONE")
        if data['status'] != 1:
            trying = 1
            isOTP = False
            isPHONE = False
            while trying < 5 and isOTP == False and self.is_running == True:
                # test
                trying += 1
                time.sleep(1)
                id = 773836
                url = "https://trumotp.com/apiv1/ordercheck?apikey=c97fe40e988206184a05e204efd80990&id="+str(id)
                payload={}
                headers = {
                'Cookie': 'ASP.NET_SessionId=5q0ixkfveukforhykvrqkmb4'
                }
                response = requests.request("GET", url, headers=headers, data=payload)
                data =  response. json()
                if data['status'] != 1:
                    isOTP = False
                    playsound('LOI.mp3')
                else:
                    resp = data['data']
                    phone = resp['phone']
                    phone = "+84"+phone[1:10]
                    if (isPHONE == False):
                        pyperclip.copy(phone.strip())
                        self.any_signal.emit(1)
                        isPHONE = True
                        playsound('SDT.mp3')
                    if (resp['code'] == ""):
                        print(resp['code'])
                        isOTP = True
                        pyperclip.copy(resp['code'].strip())
                        self.any_signal.emit(2)
                        playsound('OTP.mp3')
                        return
                    else:
                        print("POLLING" + str(phone))
                time.sleep(1)
        
        else:
            playsound("LOI.mp4")
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
        self.is_running = True
    def run(self):
        self.wd.delete_all_cookies()
        self.wd.get('https://my.telegram.org/auth')
        self.any_signal.emit(1,[])
        self.any_signal.emit(100,[1,2,4])
    def registerPhone(self,phone):
        print("dsads")
        self.wd.find_element_by_xpath('//input[@id="my_login_phone"]').send_keys(phone)
        self.any_signal.emit(2,[])
    def getOTPCode(self):
        self.wd.find_element_by_xpath('//button[@type="submit"]').click()
        self.any_signal.emit(3,[])
    def CheckSuccess(self, trying = 0):
        if (trying > 5):
            return False
        try:
            self.wd.find_element_by_xpath('//button[@id="app_save_btn"]').click()
            self.wd.find_element_by_xpath('//div[@class="app_lock_tt"]')
            return True
        except:
            playsound('ThuLai.mp3')
            time.sleep(10)
            return self.CheckSuccess(trying+1)
    def StartCreateApp(self):
        self.wd.get("https://my.telegram.org/apps")
        time.sleep(1)
        self.wd.find_element_by_xpath('//input[@id="app_title"]').send_keys(names.get_full_name())
        time.sleep(0.5)
        self.wd.find_element_by_xpath('//input[@id="app_shortname"]').send_keys(names.get_full_name())
        time.sleep(0.5)
        self.wd.find_element_by_xpath('//input[@id="app_desc"]').send_keys(names.get_full_name())
        time.sleep(2)
        if (self.CheckSuccess()):
            # GET DATA , then emit
            self.any_signal.emit(100,[])
            pass
        else:
            playsound('LOI.mp3')
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
            f.write(str(self.data[0]),+","+str(self.data[1]),+","+str(self.data[2])+"\n")
    def run(self):
        self.saveCSV()
        apihash = self.data[0]
        api_id = self.data[1]
        phone = self.data[2]
        tele_client = TelegramClient(phone, api_id,apihash)
        tele_client.start()
        self.is_running = False
        self.any_signal.terminal()
app = QtWidgets.QApplication(sys.argv)
mainWindow = PyShine_THREADS_APP()
mainWindow.show()
mainWindow.chrome()
sys.exit(app.exec_())