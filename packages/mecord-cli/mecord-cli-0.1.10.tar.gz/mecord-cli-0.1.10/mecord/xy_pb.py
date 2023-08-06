import json
import hashlib
import time
import requests

from mecord import uauth_common_pb2 
from mecord import uauth_ext_pb2 
from mecord import common_ext_pb2 
from mecord import aigc_ext_pb2 
from mecord import rpcinput_pb2 
from mecord import store 
from mecord import utils 
from mecord import constant 

uuid = utils.generate_unique_id()

def _aigc_post(request, function):
    return _post(url="https://mecord-beta.2tianxin.com/proxymsg", 
                 objStr="mecord.aigc.AigcExtObj", 
                 request=request, 
                 function=function)
    
def _common_post(request, function):
    return _post(url="https://beta.xiaohuxi.cn/proxymsg", 
                 objStr="mizacommon.uauth.AuthExtObj", 
                 request=request, 
                 function=function)
    
def _post(url, objStr, request, function):
    req = request.SerializeToString()
    opt = {
        "lang": "zh-Hans",
        "region": "CN",
        "appid": "80",
        "application": "mecord",
        "version": "1.0",
        "X-Token": store.token(),
        "uid": "1",
    }
    input_req = rpcinput_pb2.RPCInput(obj=objStr, func=function, req=req, opt=opt)
    res = requests.post(url=url, data=input_req.SerializeToString())
    pb_rsp = rpcinput_pb2.RPCOutput()
    pb_rsp.ParseFromString(res.content)
    if pb_rsp.ret == 0:
        return 0, "", pb_rsp.rsp
    else:
        # print(pb_rsp)
        return pb_rsp.ret, pb_rsp.desc, "" 
    

def GetQrcodeLoginCode():
    req = uauth_ext_pb2.GetQrcodeLoginCodeReq()
    req.login_type = uauth_common_pb2.UauthLoginType.LT_QRCODE_SCAN
    req.device_type = uauth_common_pb2.UauthDeviceType.DT_WINDOWS_PC
    req.device_id = uuid
    req.u_meng_device_id = ""

    rsp = uauth_ext_pb2.GetQrcodeLoginCodeRes()
    r1, r2, r3 = _common_post(req, "GetQrcodeLoginCode")
    if r1 != 0:
        print(r2)
        return None
    rsp.ParseFromString(r3)
    s = rsp.login_code
    return s

def CheckLoginLoop(code):
    req = uauth_ext_pb2.GetQrcodeLoginStatusReq()
    req.login_code = code
    req.device_id = uuid
    req.u_meng_device_id = ""

    rsp = uauth_ext_pb2.GetQrcodeLoginStatusRes()
    r1, r2, r3 = _common_post(req, "GetQrcodeLoginStatus")
    if r1 != 0:
        print(r2)
        return 0
    rsp.ParseFromString(r3)
    if rsp.status == uauth_ext_pb2.GetQrcodeLoginStatus.SUCCESS:
        sp = store.Store()
        data = sp.read()
        data["uid"] = rsp.commonSignInRes.user_id
        data["token"] = rsp.commonSignInRes.login_token
        data["nickname"] = rsp.userNickname
        data["icon"] = rsp.userIconUrl
        sp.write(data)
        return 1
    elif rsp.status == uauth_ext_pb2.GetQrcodeLoginStatus.EXPIRED or rsp.status == uauth_ext_pb2.GetQrcodeLoginStatus.CANCEL:
        return 0
    else:
        return -1
    
def GetTask(token):
    req = aigc_ext_pb2.GetTaskReq()
    req.DeviceKey = uuid
    map = store.widgetMap()
    for it in map:
        req.widgets.append(it)
    req.token = token
    req.limit = 1
    extInfo = store.readDeviceInfo()
    extInfo["app_version"] = constant.app_version
    extInfo["app_bulld_number"] = constant.app_bulld_number
    extInfo["app_name"] = constant.app_name
    req.extend = json.dumps(extInfo)

    rsp = aigc_ext_pb2.GetTaskRes()
    r1, r2, r3 = _aigc_post(req, "GetTask")
    if r1 != 0:
        print(r2)
        return []
    rsp.ParseFromString(r3)
    datas = []
    for it in rsp.list:
        datas.append({
            "taskUUID": it.taskUUID,
            "pending_count": rsp.count - rsp.limit,
            "config": it.config,
            "data": it.data,
        })
    return datas

def TaskNotify(taskUUID, status, msg, dataStr):
    req = aigc_ext_pb2.TaskNotifyReq()
    req.taskUUID = taskUUID
    if status:
        req.taskStatus = common_ext_pb2.TaskStatus.TS_Success
    else:
        req.taskStatus = common_ext_pb2.TaskStatus.TS_Failure
    req.failReason = msg
    req.data = dataStr

    rsp = aigc_ext_pb2.TaskNotifyRes()
    r1, r2, r3 = _aigc_post(req, "TaskNotify")
    if r1 != 0:
        print(r2)
        return False
    rsp.ParseFromString(r3)
    return True

def GetAigcDeviceInfo():
    req = aigc_ext_pb2.AigcDeviceInfoReq()
    req.deviceKey = uuid

    rsp = aigc_ext_pb2.AigcDeviceInfoRes()
    r1, r2, r3 = _aigc_post(req, "DeviceInfo")
    if r1 != 0:
        print(r2)
        return False
    rsp.ParseFromString(r3)
    print(f"====={rsp}")
    if len(rsp.groupUUID) > 0:
        sp = store.Store()
        data = sp.read()
        data["groupUUID"] = rsp.groupUUID
        data["token"] = rsp.token
        if rsp.isCreateWidget == True:
            data["isCreateWidget"] = rsp.isCreateWidget
        sp.write(data)
        return True
    return False

def CreateWidgetUUID():
    req = aigc_ext_pb2.CreateWidgetReq()
    rsp = aigc_ext_pb2.CreateWidgetRes()
    r1, r2, r3 = _aigc_post(req, "CreateWidget")
    if r1 != 0:
        print(r2)
        return ""
    rsp.ParseFromString(r3)
    return rsp.widgetUUID

def GetOssUrl(ext):
    req = aigc_ext_pb2.UploadFileUrlReq()
    req.token = store.token()
    req.version = constant.app_bulld_number
    req.fileExt = ext

    rsp = aigc_ext_pb2.UploadFileUrlRes()
    r1, r2, r3 = _aigc_post(req, "UploadFileUrl")
    if r1 != 0:
        print(r2)
        return ""
    rsp.ParseFromString(r3)
    return rsp.url, rsp.contentType
    
def GetWidgetOssUrl(widgetid):
    req = aigc_ext_pb2.UploadWidgetUrlReq()
    req.widgetUUID = widgetid

    rsp = aigc_ext_pb2.UploadWidgetUrlRes()
    r1, r2, r3 = _aigc_post(req, "UploadWidgetUrl")
    if r1 != 0:
        print(r2)
        return ""
    rsp.ParseFromString(r3)
    return rsp.url, rsp.contentType

def WidgetUploadEnd(url):
    req = aigc_ext_pb2.UploadWidgetReq()
    req.fileUrl = url
    
    rsp = aigc_ext_pb2.UploadWidgetRes()
    r1, r2, r3 = _aigc_post(req, "UploadWidget")
    if r1 != 0:
        print(r2)
        return 0
    rsp.ParseFromString(r3)
    return rsp.checkId

# def PublishWidget(widgetid, oss_path):
#     req = aigc_ext_pb2.UploadWidgetReq()
#     req.fileUrl = oss_path

#     rsp = aigc_ext_pb2.UploadWidgetRes()
#     rsp.ParseFromString(_aigc_post(req, "UploadWidget"))
#     return rsp.uploadId
    
def UploadWidgetCheck(checkId):
    req = aigc_ext_pb2.UploadWidgetCheckReq()
    req.checkId = checkId

    rsp = aigc_ext_pb2.UploadWidgetCheckRes()
    r1, r2, r3 = _aigc_post(req, "UploadWidgetCheck")
    if r1 != 0:
        print(r2)
        return 0
    rsp.ParseFromString(r3)
    if rsp.status == aigc_ext_pb2.UploadWidgetStatus.UWS_SUCCESS:
        return 1
    elif rsp.status == aigc_ext_pb2.UploadWidgetStatus.UWS_FAILURE:
        print(f"failReason = {rsp.failReason}")
        return 0
    else:
        return -1
