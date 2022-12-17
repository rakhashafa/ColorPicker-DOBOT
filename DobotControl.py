import sys
sys.path.insert(1,'./DLL')
import DobotDllType as dType
import numpy as np
import cv2
import time


webcam = cv2.VideoCapture(0)

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

def ambilBarang():
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 176, -0.8, 26.4, 0, 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 205.3, -8.5, -67, 0, 1)
    dType.SetEndEffectorSuctionCup(api, True, True, isQueued=1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 210.8, -6, 22.8, 0, 1)

    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 18.1, -252.3, -40.5, 0, 1)
    dType.SetEndEffectorSuctionCup(api, True, False, isQueued=1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 205.3, -8.5, -42, 0, 1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 176, -0.8, 26.4, 0, 1)
    time.sleep(5)

if (state == dType.DobotConnect.DobotConnect_NoError):
    
    #清空队列
    #Clean Command Queued
    dType.SetQueuedCmdClear(api)
    
    #设置运动参数
    #Async Motion Params Setting
    dType.SetHOMEParams(api, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

    #回零
    #Async Home
    dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    #设置ptpcmd内容并将命令发送给dobot
    #Async PTP Motion
    while True:
        _, imageFrame = webcam.read()
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        red_lower = np.array([136, 87, 111], np.uint8)
        red_upper = np.array([180, 255, 255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

        blue_lower = np.array([94, 80, 2], np.uint8)
        blue_upper = np.array([120, 255, 255], np.uint8)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

        kernal = np.ones((5, 5), "uint8")

        red_mask = cv2.dilate(red_mask, kernal)
        res_red = cv2.bitwise_and(imageFrame, imageFrame,mask = red_mask)

        blue_mask = cv2.dilate(blue_mask, kernal)
        res_blue = cv2.bitwise_and(imageFrame, imageFrame,mask = blue_mask)

        contours, hierarchy = cv2.findContours(red_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2. boundingRect(contour)
                if x is not None:
                    ambilBarang()


                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                        (x + w, y + h),
                                        (0, 0, 255), 2)
                
                cv2.putText(imageFrame, "Red Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0,
                            (0, 0, 255))

        contours, hierarchy = cv2.findContours(blue_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area > 300):
                x, y, w, h = cv2.boundingRect(contour)
                imageFrame = cv2.rectangle(imageFrame, (x, y),
                                        (x + w, y + h),
                                        (255, 0, 0), 2)
                
                cv2.putText(imageFrame, "Blue Colour", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1.0, (255, 0, 0))
        # print(contours)
        cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break

        # dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 176, -0.8, 26.4, 0, 1)
        # dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 205.3, -8.5, -67, 0, 1)
        # dType.SetEndEffectorSuctionCup(api, True, True, isQueued=1)
        # dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 210.8, -6, 22.8, 0, 1)

        # dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, 18.1, -252.3, -40.5, 0, 1)
        # dType.SetEndEffectorSuctionCup(api, True, False, isQueued=1)


    #开始执行指令队列
    #Start to Execute Command Queue
    dType.SetQueuedCmdStartExec(api)

    

#断开连接
#Disconnect Dobot
dType.DisconnectDobot(api)
