import sys
sys.path.insert(1,'./DLL')
import DobotDllType as dType

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#将dll读取到内存中并获取对应的CDLL实例
#Load Dll and get the CDLL object
api = dType.load()
#建立与dobot的连接
#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

if(state == dType.DobotConnect.DobotConnect_NoError):
    dType.SetQueuedCmdClear(api)
    dType.SetHOMEParams(api, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
    dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    
    while True:
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 176, -0.8, 26.4, 0, 1)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 205.3, -8.5, -67, 0, 1)
        dType.SetEndEffectorSuctionCup(api, True, True, isQueued=1)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 210.8, -6, 22.8, 0, 1)

        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 18.1, -252.3, -40.5, 0, 1)
        dType.SetEndEffectorSuctionCup(api, True, False, isQueued=1)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 205.3, -8.5, -42, 0, 1)
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 176, -0.8, 26.4, 0, 1)
        
        break

    dType.SetQueuedCmdStartExec(api)
#断开连接
#Disconnect Dobot
dType.DisconnectDobot(api)
