#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os		#发送adb命令
import time
#from PIL import Image
import cv2
#from matplotlib import pyplot as plt

#定义一些数据
yScanStart = 600	#从20%处开始扫描
xMiddle = 720		#横轴中位线
maxDist = 20		#颜色变化阈值
coef = 1.2			#系数	
width = 1440
height = 2560		#宽高

#小人模板的处理
player = cv2.imread("player.png")


#开始啦
for i in range(0,50):	
	#截屏
	os.popen("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
	time.sleep(2)		#+1s
	#图片复制到电脑
	os.popen("adb pull /sdcard/screenshot.png D:\\jump")
	time.sleep(2)		#+1s
	#删除手机上的截屏
	#os.popen("adb shell rm /sdcard/screenshot.png")

	##区域匹配，获取小人位置
	wPlayer = 0
	img = cv2.imread("screenshot.png")	#读取图像
	# 调用匹配函数
	# 第一个参数是原图
	# 第二个参数是模板
	# 第三个参数是匹配算法
	# 返回的结果是一个二维的float类型的数组,大小为W-w+1 * H-h+1
	res = cv2.matchTemplate(img, player, cv2.TM_CCOEFF)
	# 获取返回结果中最值及其在res中的位置
	min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	wPlayer = max_loc[0]
	print("max =",cv2.minMaxLoc(res))

	##图像处理，获得目标位置

	exitFlag = False				#跳出两层循环用的
	holding = 0						#长按时间
	wLeft = 0
	wRight = 0						#为处理好圆形弄的他
	w = 0							#横坐标
	##这里可以优化：先粗略查找，确定范围后精细查找
	for h in range(yScanStart//10,height//10):
		for w in range(0,width//10):
			(b1,g1,r1) = img[h*10,w*10]			#获取像素点
			(b2,g2,r2) = img[(h+1)*10,w*10]		#下面的点
			b1 = int(b1)
			b2 = int(b2)
			g1 = int(g1)
			g2 = int(g2)
			r1 = int(r1)
			r2 = int(r2)
			if (b1-b2)*(b1-b2)+(g1-g2)*(g1-g2)+(r1-r2)*(r1-r2) > maxDist:
				if abs(w*10 - wPlayer) > 100:	#不然会把小人当成目标
					print('wLeft =',w*10)
					wLeft = w
					#继续找wRight
					for w in range(wLeft,width//10):
						(b1,g1,r1) = img[h*10,w*10]			#获取像素点
						(b2,g2,r2) = img[(h+1)*10,w*10]		#下面的点
						b1 = int(b1)
						b2 = int(b2)
						g1 = int(g1)
						g2 = int(g2)
						r1 = int(r1)
						r2 = int(r2)
						if (int(b1)-b2)*(b1-b2)+(g1-g2)*(g1-g2)+(r1-r2)*(r1-r2) < maxDist:
							wRight = w - 1
							print('wRight =',wRight*10)
							w = (wLeft + wRight)/2
							print('w =',w*10)
							exitFlag = True						#跳出两层循环要立flag
							break
			if exitFlag:
				break
		if exitFlag:
			break
	
	

	holding = abs(wPlayer - w*10)*coef
	#执行
	string = "adb shell input touchscreen swipe 367 469 367 469 " + str(int(holding))
	os.popen(string)
	time.sleep(2)
