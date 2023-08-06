import os
import json
import sys
import shutil
import zipfile
import pkg_resources
import threading
import time
import requests
import random

from pathlib import Path
from mecord import store
from mecord import xy_pb
from mecord import upload
from mecord import utils

h5_name = "h5"
script_name = "script"
def GetWidgetConfig(path):
    #search h5 folder first, netxt search this folder
    if os.path.exists(os.path.join(path, h5_name)):
        for filename in os.listdir(os.path.join(path, h5_name)):
            pathname = os.path.join(path, h5_name, filename) 
            if (os.path.isfile(pathname)) and filename == "config.json":
                with open(pathname, 'r') as f:
                    return json.load(f)
    for filename in os.listdir(path):
        pathname = os.path.join(path, filename) 
        if (os.path.isfile(pathname)) and filename == "config.json":
            with open(pathname, 'r') as f:
                return json.load(f)
    return {}
    
def configInFolder(path):
    for filename in os.listdir(path):
        pathname = os.path.join(path, filename) 
        if (os.path.isfile(pathname)) and filename == "config.json":
            return True
    return False

def PathIsEmpty(path):
    return len(os.listdir(path)) == 0

def checkImportMecordJs(h5Root):
    jsPath = os.path.join(h5Root, "MekongJS.js")
    jsPathTmp = os.path.join(h5Root, "MekongJS.js.py")
    js_res = requests.get(f"https://www.mecordai.com/prod/mecord/commonality/MecordJS/MecordJS.min.js?t={random.randint(100,99999999)}")
    with open(jsPathTmp, "wb") as c:
        c.write(js_res.content)
    if os.path.exists(jsPathTmp):
        if os.path.exists(jsPath):
            os.remove(jsPath)
        os.rename(jsPathTmp, jsPath)


def replaceIfNeed(dstDir, name, subfix):
    newsubfix = subfix + ".py"
    if name.find(newsubfix) != -1:
        os.rename(os.path.join(dstDir, name), os.path.join(dstDir, name.replace(newsubfix, subfix)))

def copyWidgetTemplate(root, name, dirname):
    templateDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)#sys.prefix
    dstDir = os.path.join(root, dirname)
    shutil.copytree(templateDir, dstDir)
    shutil.rmtree(os.path.join(dstDir, "__pycache__"))
    os.remove(os.path.join(dstDir, "__init__.py"))
    for filename in os.listdir(dstDir):
        replaceIfNeed(dstDir, filename, ".json")
        replaceIfNeed(dstDir, filename, ".js")
        replaceIfNeed(dstDir, filename, ".png")
        replaceIfNeed(dstDir, filename, ".html")

def createDemoWidget():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo")
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)
    createWidget(path)
    publishWidget(path)

def createWidget(root):
    if PathIsEmpty(root) == False:
        print("current folder is not empty, create widget fail!")
        return
        
    widgetid = xy_pb.CreateWidgetUUID()
    if len(widgetid) == 0:
        print("create fail! mecord server is not avalid")
        return
    
    copyWidgetTemplate(root, "widget_template", h5_name)
    copyWidgetTemplate(root, "script_template", script_name)
    #h5
    data = GetWidgetConfig(root)
    data["widget_id"] = widgetid
    data["group_id"] = store.groupUUID()
    data["device_keys"] = [
        utils.generate_unique_id()
    ]
    data["cmd"] = os.path.join(root, script_name, "main.py")
    with open(os.path.join(root, h5_name, "config.json"), 'w') as f:
        json.dump(data, f)
    checkImportMecordJs(os.path.join(root, h5_name))
    #script
    with open(os.path.join(root, script_name, "config.json"), 'w') as f:
        json.dump({"widget_id": widgetid}, f)
    addWidget(os.path.join(root, script_name))
    print("create widget success")

def CheckWidgetDataInPath(path):
    data = GetWidgetConfig(path)
    if "widget_id" not in data:
        print("folder is not widget")
        return False

    if "widget_id" in data:
        widget_id = data["widget_id"]
        if len(widget_id) == 0:
            print("widget_id is empty!")
            return False
        
    return True

def addWidget(root):
    if CheckWidgetDataInPath(root) == False:
        return
        
    data = GetWidgetConfig(root)
    widget_id = data["widget_id"]
    mainPythonPath = os.path.join(root, "main.py")
    if os.path.exists(os.path.join(root, script_name)):
        mainPythonPath = os.path.join(root, script_name, "main.py")
    if store.insertWidgets(widget_id, mainPythonPath):
        print(f"add {widget_id.ljust(len(widget_id)+4)} {mainPythonPath}")

def publishWidget(root):
    if CheckWidgetDataInPath(root) == False:
        return
        
    data = GetWidgetConfig(root)
    widget_id = data["widget_id"]

    distname = utils.generate_unique_id() + "_" + widget_id
    dist = os.path.join(os.path.dirname(root), distname + ".zip")
    zip = zipfile.ZipFile(dist, "w", zipfile.ZIP_DEFLATED) 

    #h5 folder
    package_folder = ""
    if configInFolder(root):
        package_folder = root
    elif configInFolder(os.path.join(root, h5_name)):
        package_folder = os.path.join(root, h5_name)

    checkImportMecordJs(package_folder)
    for root,dirs,files in os.walk(package_folder):
        for file in files:
            if str(file).startswith("~$"):
                continue
            filepath = os.path.join(root, file)
            writepath = os.path.relpath(filepath, package_folder)
            zip.write(filepath, writepath)
    zip.close()

    (ossurl, checkid) = upload.uploadWidget(dist, widget_id)
    if checkid > 0:
        checkUploadComplate(checkid, dist)
    else:
        os.remove(dist)

def checkUploadComplate(checkid, dist):
    rst = xy_pb.UploadWidgetCheck(checkid)
    if rst == 1: #success
        print("publish widget success")
        # xy_pb.UploadWidget(widget_id, ossurl)  #暂时不用
        os.remove(dist)
        store.finishCreateWidget()
    elif rst == -1:
        threading.Timer(1, checkUploadComplate, (checkid, dist, )).start()
    else: #fail
        print("publish fail")
        return