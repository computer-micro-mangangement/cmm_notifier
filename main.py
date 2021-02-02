import sys
import tempfile
import platform
import base64
import requests
import json
import os
import time
from win10toast_persist import ToastNotifier
from PIL import Image
import config


def notificationClick():
    print("hi")


def base64Encode(toEncode):
    return base64.b64encode(toEncode.encode('utf-8')).decode('utf-8')


def base64Decode(toDecode):
    return base64.b64decode(toDecode.encode("utf-8")).decode("utf-8")


# notify.init('E:/tommy/Programming/Python/Notifier/python/icon.ico', notificationClick)
toaster = ToastNotifier()
with tempfile.TemporaryDirectory() as directory:
    # if True:
    while True:
        pcName = platform.node()
        encodedName = base64Encode(pcName)
        r = requests.get(f'http://{config.getServerAddress()}/api/modules/notifications/handle',
                         {"devicesecret": config.getDeviceSecret()})
        notifications = r.json()

        for notifi in notifications:
            # decode json data
            receiverUUID = base64Decode(notifi["recieverUUID"])
            iconData = base64Decode(notifi["iconData"])
            title = base64Decode(notifi["title"])
            content = base64Decode(notifi["content"])
            id = base64Decode(notifi["id"])
            sender = base64Decode(notifi["sender"])

            # download and save picture
            filename = "picture.ico"
            filePath = directory + "\\" + filename
            writeData = "".encode("utf-8")
            if iconData[:4] == "http":
                writeData = requests.get(iconData).content
                if "png" in iconData:
                    pngFile = "temp.png"
                    pngPath = directory + "\\" + pngFile
                    open(pngPath, 'wb').write(writeData)
                    img = Image.open(pngPath)
                    img.save(filePath)
                    os.remove(pngPath)
                else:
                    # delete file when existing
                    if os.path.exists(filePath):
                        os.remove(filePath)
                    # write image in file
                    open(filePath, 'wb').write(writeData)
            elif iconData != "":
                utfDecoded = iconData.decode("utf-8")
                if "," in utfDecoded:
                    beginDataIndex = utfDecoded.rindex(",") + 1
                    description = utfDecoded[:beginDataIndex]
                    print(description + "(" + content + ")")
                    data = utfDecoded[beginDataIndex:]
                    if "icon" in description:
                        writeData = base64.b64decode(data)
                    # delete file when existing
                    if os.path.exists(filePath):
                        os.remove(filePath)
                    # write image in file
                    open(filePath, 'wb').write(writeData)

            # set filepath to NUll if no image is written
            if writeData == "".encode("utf-8"):
                filePath = None

            # if filePath is not None:
            # send notification
            title = title + " by " + sender
            toaster.show_toast(title=title,
                               msg=content,
                               icon_path=filePath,
                               duration=None)
            os.remove(filePath)
        time.sleep(config.waitDelayInSec)

# notify.uninit()
