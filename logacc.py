
import asyncio
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import csv
from PyQt5.QtGui import QIcon
from telethon import TelegramClient, client
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import JoinChannelRequest,LeaveChannelRequest
def ReadAccountList():
        list_accs = []
        with open('accounts.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                        if line_count == 0:
                                line_count += 1
                        else:
                                list_accs.append([row[0],row[1],row[2]])
                                line_count += 1
        return list_accs

list_accs = ReadAccountList()
i = 0
for item in list_accs:
        tele_client = TelegramClient(item[2], item[1],item[0])
        tele_client.connect()
        import sys
        from io import StringIO
        sys.stdin = StringIO('test')
        if not tele_client.is_user_authorized():
                print("DIE ACC " + item[2])
        else:
                try:
                        i+=1
                        tele_client.start(item[2],max_attempts=1)
                except Exception as ee:
                        print( str(i) + " FALSE " + item[2] + str(ee))