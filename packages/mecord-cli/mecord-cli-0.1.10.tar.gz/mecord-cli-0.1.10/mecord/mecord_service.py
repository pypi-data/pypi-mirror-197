import os
import sys
import time
import signal
import subprocess
import json
from pathlib import Path
from urllib.parse import *

from mecord import xy_socket
from mecord import store
from mecord import xy_pb
from mecord import xy_user 
from mecord import utils

class BaseService:
    def __init__(self, name, pid_file=None):
        self.name = name
        self.pid_file = pid_file
        self.running = False
        self.halt = False

    def start(self):
        store.writeDeviceInfo(utils.deviceInfo())
        self.halt = False
        if self.pid_file:
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
        self.running = True
        signal.signal(signal.SIGTERM, self.stop)
        self.run()

    def run(self):
        pass

    def stop(self, signum=None, frame=None):
        self.running = False
        if self.pid_file and os.path.exists(self.pid_file):
            os.remove(self.pid_file)

    def restart(self):
        self.stop()
        time.sleep(1)
        self.start()

    def is_running(self):
        if self.pid_file and os.path.exists(self.pid_file):
            with open(self.pid_file, 'r') as f:
                pid = int(f.read())
                try:
                    os.kill(pid, 0)
                except OSError:
                    return False
                else:
                    return True
        else:
            return self.running

class MecordService(BaseService):
    def __init__(self):
        pid_file = '/var/run/MecordService.pid' if sys.platform != 'win32' else None
        super().__init__("MecordService", pid_file)
        # self.socket = MecordSocket(self.receiveData)
        # self.socket.start()

    def receiveData(self, s):
        print(s)

    def executeLocalPython(self, taskUUID, cmd, param):
        inputArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{taskUUID}.in")
        if os.path.exists(inputArgs):
            os.remove(inputArgs)
        with open(inputArgs, 'w') as f:
            json.dump(param, f)
        outArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{taskUUID}.out")
        if os.path.exists(outArgs):
            os.remove(outArgs)
            
        command = f'{sys.executable} "{cmd}" --run "{inputArgs}" --out "{outArgs}"'
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        print(result.stdout.decode(encoding="utf8", errors="ignore"))
        if os.path.exists(outArgs):
            with open(outArgs, 'r') as f:
                outData = json.load(f)
        else:
            print(f"task {taskUUID} result is empty!, please check {cmd}")
            outData = {}
        os.remove(inputArgs)
        os.remove(outArgs)
        return outData

    def hasValue(self, data, type, key):
        if "type" not in data:
            print("result is not avalid")
        if data["type"] == type and "extension" in data and key in data["extension"] and len(data["extension"][key]) > 0:
            return True
        return False
             
    def checkResult(self, data):
        for it in data["result"]:
            if self.hasValue(it, "text", "cover_url") == False:
                it["extension"]["cover_url"] = ""
            if self.hasValue(it, "audio", "cover_url") == False:
               it["extension"]["cover_url"] = ""
               
            if "extension" in it and "cover_url" in it["extension"] and len(it["extension"]["cover_url"]) > 0:
                w, h = utils.getOssImageSize(it["extension"]["cover_url"])
                if w > 0 and h > 0:
                    if "?" in str(it["extension"]["cover_url"]):
                        it["extension"]["cover_url"] += f"&width={w}&height={h}"
                    else:
                        it["extension"]["cover_url"] = urljoin(it["extension"]["cover_url"], f"?width={w}&height={h}")


    def cmdWithWidget(self, widget_id):
        map = store.widgetMap()
        if widget_id in map and len(map[widget_id]) > 0:
            return map[widget_id]
        return None

    def run(self):
        try:
            while self.running:
                datas = xy_pb.GetTask(store.token())
                for it in datas:
                    taskUUID = it["taskUUID"]
                    pending_count = it["pending_count"]
                    config = json.loads(it["config"])
                    params = json.loads(it["data"])
                    widget_id = config["widget_id"]
                    group_id = config["group_id"]
                    #cmd
                    local_cmd = self.cmdWithWidget(widget_id)
                    cmd = ""
                    if local_cmd:
                        cmd = local_cmd
                    else:
                        cmd = str(Path(config["cmd"]))
                    #params
                    params["task_id"] = taskUUID
                    params["pending_count"] = pending_count
                    #run
                    result_obj = self.executeLocalPython(taskUUID, cmd, params)
                    #result                    
                    is_ok = result_obj["status"] == 0
                    msg = result_obj["message"]
                    if is_ok:
                        self.checkResult(result_obj)
                    else:
                        if len(msg) == 0:
                            msg = "Unknow Error"
                    if xy_pb.TaskNotify(taskUUID, 
                                is_ok, 
                                msg, 
                                json.dumps(result_obj["result"], separators=(',', ':'))):
                        print(f"you are complate task : {taskUUID}")
                
                time.sleep(1)
        except Exception as e:
            print(e)
            return

    def status_ok(self):
        service_running = super()._is_running()
        socket_running = True #self.socket.isRunning()
        is_login =xy_user.User().isLogin()
        return socket_running and service_running and is_login
    

#python xxxxxx\main.py --run "{\"task_id\":1,\"widget_id\":1,\"pending_count\":1,\"fn_name\":\"test\",\"param\":{\"text\":\"Hello World\"}}"
# MecordService.executeLocalPython(None, "asdasdlasasdasdasdas", r"E:\mecord_sd\3333333333333333333333\script\main.py", {"task_id":1,"widget_id":1,"pending_count":1,"fn_name":"test","param":{"text":"Hello World"}})