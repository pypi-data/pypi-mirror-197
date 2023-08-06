import sys
import os
import argparse
import threading

from mecord import xy_pb 
from mecord import utils
from mecord import xy_user
from mecord import mecord_service
from mecord import mecord_widget
from mecord import store

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
subparsers = parser.add_subparsers()
parser_widget = subparsers.add_parser("deviceid", help="获取当前设备ID")
parser_widget = subparsers.add_parser("show_token", help="展示当前设备token")
parser_widget = subparsers.add_parser("add_token", help="填入其他设备token")
parser_widget = subparsers.add_parser("widget", help="widget模块")
parser_widget.add_argument("init", type=str, default=None, help="创建widget, 注意: 需要在空目录调用")
parser_widget.add_argument("public", type=str, default=None, help="发布模块")
parser_widget.add_argument("list", type=str, default=None, help="本地支持的widget列表")
parser_widget.add_argument("add", type=str, default=None, help="添加新的本地widget执行库")
parser_service = subparsers.add_parser("service", help="service模块")
parser_service.add_argument("start", type=str, default=None, help="start task loop service")

def service():
    if xy_user.User().isLogin() == False:
        print('please login first! \nUsage: mecord deviceid & Use Mecord Application scan it')
        return
    map = store.widgetMap()
    if len(map) == 0:
        print("please add widget first! \nUsage: mecord widget add [widget python path]")
        return
    if len(sys.argv) <= 2:
        print('please set command! Usage: mecord service start')
        return

    command = sys.argv[2]
    service = mecord_service.MecordService()
    if command == 'start':
        if service.is_running():
            print('Service is already running.')
        else:
            print('Starting service...')
            service.start()
    elif command == 'stop':
        if not service.is_running():
            print('Service is not running.')
        else:
            print('Stopping service...')
            service.stop()
    elif command == 'restart':
        print('Restarting service...')
        service.restart()
    elif command == 'status':
        if service.is_running():
            print('Service is running.')
        else:
            print('Service is not running.')
    else:
        print("Unknown command:", command)
        print("Usage: python service.py [start|stop|restart|status]")
        
def widget():
    if xy_user.User().isLogin() == False:
        print('please login first! \nUsage: mecord deviceid & Use Mecord Application scan it')
        return
    if len(sys.argv) <= 2:
        print('please set command! Usage: mecord widget [init|publish]')
        return

    command = sys.argv[2] 
    work_path = os.getcwd()
    if len(sys.argv) > 3:
        work_path = sys.argv[3]
    if command == 'init':
        mecord_widget.createWidget(work_path)
    elif command == 'publish':
        mecord_widget.publishWidget(work_path)
    elif command == 'list':
        map = store.widgetMap()
        if len(map) == 0:
            print("local widget is empty")
        maxJust = 20
        for it in map:
            if len(it) > maxJust:
                maxJust= len(it)
        for it in map:
            print(f"{it.ljust(maxJust + 4)} {map[it]}")
    elif command == 'add':
        mecord_widget.addWidget(work_path)
    else:
        print("Unknown command:", command)
        print("Usage: mecord widget [init|publish]")

_max_checkdevice_count = 300 #loop waiting 5min
_cur_checkdevice_count = 0
def checkDeviceInfo():
    global _max_checkdevice_count
    global _cur_checkdevice_count
    if _cur_checkdevice_count > _max_checkdevice_count:
        return
    if xy_pb.GetAigcDeviceInfo():
        if store.isCreateWidget():
            mecord_widget.createDemoWidget()
    else:
        _cur_checkdevice_count += 1
        threading.Timer(1, checkDeviceInfo, ()).start()
        
def deviceid():
    global _cur_checkdevice_count
    xy_user.User().loginIfNeed()
    uuid = utils.generate_unique_id()
    utils.displayQrcode(f"https://main_page.html?action=scanbind&deviceId={uuid}")
    print(f"your deviceid is : {uuid}")
    _cur_checkdevice_count = 0
    checkDeviceInfo()
        
def joinToken():
    sp = store.Store()
    data = sp.read()

    if len(sys.argv) <= 2:
        print('can not found token! Usage: mecord add_token {token}')
        return
    if "token" in data and len(data["token"]) > 0:
        print('warning! token has been override!')
        
    store.clear()
    token = sys.argv[2] 
    data["token"] = token
    sp.write(data)

def showToken():
    t = store.token()
    print(f"your token is : {t}")
    utils.displayQrcode(t)

module_func = {
    "widget": widget,
    "service": service,
    "deviceid": deviceid,
    "show_token": showToken,
    "add_token": joinToken,
}

def main():
    if len(sys.argv) < 2:
        return

    module = sys.argv[1]
    if module in module_func:
        module_func[module]()
    else:
        print("Unknown command:", module)
        print("Usage: mecord [deviceid|show_token|add_token|service|widget]")
        sys.exit(0)
        
if __name__ == '__main__':
        main()
