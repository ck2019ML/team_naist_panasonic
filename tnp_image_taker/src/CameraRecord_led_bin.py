#
# Version:  2017.07.31
# Authors:  Members of the Team NAIST-Panasonic at the Amazon Robotics Challenge 2017:
#           Gustavo A. Garcia R. <garcia-g at is.naist.jp> (Captain), 
#           Lotfi El Hafi, Felix von Drigalski, Wataru Yamazaki, Viktor Hoerig, Arnaud Delmotte, 
#           Akishige Yuguchi, Marcus Gall, Chika Shiogama, Kenta Toyoshima, Pedro Uriguen, 
#           Rodrigo Elizalde, Masaki Yamamoto, Yasunao Okazaki, Kazuo Inoue, Katsuhiko Asai, 
#           Ryutaro Futakuchi, Seigo Okada, Yusuke Kato, and Pin-Chu Yang
#####################
# Copyright 2017 Team NAIST-Panasonic 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at 
#     http://www.apache.org/licenses/LICENSE-2.0 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#####################

import time
import rospy
import os.path
import cv2
from cv_bridge import CvBridge, CvBridgeError
import numpy as np
from geometry_msgs.msg import PoseStamped, Point, Quaternion, Vector3
from iiwa_msgs.msg import CartesianEulerPose, CartesianQuantity, ControlMode

from sensor_msgs.msg import Image, CameraInfo
#for led
from std_msgs.msg import String

Savename = "hand_weight_horizontal_front_bin"
SavePath = './' + Savename
#rgb
SavePath_rgb = SavePath + '/' + Savename +'_rgb_image/'
SavePath_rgb_led050 = SavePath_rgb + '/' + Savename +'_rgb_image_led050/'
SavePath_rgb_led150 = SavePath_rgb + '/' + Savename +'_rgb_image_led150/'
SavePath_rgb_led100 = SavePath_rgb + '/' + Savename +'_rgb_image_led100/'
#led050
SavePath_rgb_led050_high = SavePath_rgb_led050 + '/' + Savename + '_rgb_image_led050_high/'
SavePath_rgb_led050_middle = SavePath_rgb_led050 + '/' + Savename + '_rgb_image_led050_middle/'
SavePath_rgb_led050_low = SavePath_rgb_led050 + '/' + Savename + '_rgb_image_led050_low/'
#led150
SavePath_rgb_led150_high = SavePath_rgb_led150 + '/' + Savename + '_rgb_image_led150_high/'
SavePath_rgb_led150_middle = SavePath_rgb_led150 + '/' + Savename + '_rgb_image_led150_middle/'
SavePath_rgb_led150_low = SavePath_rgb_led150 + '/' + Savename + '_rgb_image_led150_low/'
#led100
SavePath_rgb_led100_high = SavePath_rgb_led100 + '/' + Savename + '_rgb_image_led100_high/'
SavePath_rgb_led100_middle = SavePath_rgb_led100 + '/' + Savename + '_rgb_image_led100_middle/'
SavePath_rgb_led100_low = SavePath_rgb_led100 + '/' + Savename + '_rgb_image_led100_low/'
#depth_image
SavePath_depth_image = SavePath + '/' + Savename +'_depth_image/'
SavePath_depth_image_led050 = SavePath_depth_image + '/' + Savename +'_depth_image_led050/'
SavePath_depth_image_led150 = SavePath_depth_image + '/' + Savename +'_depth_image_led150/'
SavePath_depth_image_led100 = SavePath_depth_image + '/' + Savename +'_depth_image_led100/'
#led050
SavePath_depth_image_led050_high = SavePath_depth_image_led050 + '/' + Savename + '_depth_image_led050_high/'
SavePath_depth_image_led050_middle = SavePath_depth_image_led050 + '/' + Savename + '_depth_image_led050_middle/'
SavePath_depth_image_led050_low = SavePath_depth_image_led050 + '/' + Savename + '_depth_image_led050_low/'
#led150
SavePath_depth_image_led150_high = SavePath_depth_image_led150 + '/' + Savename + '_depth_image_led150_high/'
SavePath_depth_image_led150_middle = SavePath_depth_image_led150 + '/' + Savename + '_depth_image_led150_middle/'
SavePath_depth_image_led150_low = SavePath_depth_image_led150 + '/' + Savename + '_depth_image_led150_low/'
#led100
SavePath_depth_image_led100_high = SavePath_depth_image_led100 + '/' + Savename + '_depth_image_led100_high/'
SavePath_depth_image_led100_middle = SavePath_depth_image_led100 + '/' + Savename + '_depth_image_led100_middle/'
SavePath_depth_image_led100_low = SavePath_depth_image_led100 + '/' + Savename + '_depth_image_led100_low/'
#depth_image_registered
SavePath_depth_image_registered = SavePath + '/' + Savename +'_depth_image_registered/'
SavePath_depth_image_registered_led050 = SavePath_depth_image_registered + '/' + Savename +'_depth_image_registered_led050/'
SavePath_depth_image_registered_led150 = SavePath_depth_image_registered + '/' + Savename +'_depth_image_registered_led150/'
SavePath_depth_image_registered_led100 = SavePath_depth_image_registered + '/' + Savename +'_depth_image_registered_led100/'
#led050
SavePath_depth_image_registered_led050_high = SavePath_depth_image_registered_led050 + '/' + Savename + '_depth_image_registered_led050_high/'
SavePath_depth_image_registered_led050_middle = SavePath_depth_image_registered_led050 + '/' + Savename + '_depth_image_registered_led050_middle/'
SavePath_depth_image_registered_led050_low = SavePath_depth_image_registered_led050 + '/' + Savename + '_depth_image_registered_led050_low/'
#led150
SavePath_depth_image_registered_led150_high = SavePath_depth_image_registered_led150 + '/' + Savename + '_depth_image_registered_led150_high/'
SavePath_depth_image_registered_led150_middle = SavePath_depth_image_registered_led150 + '/' + Savename + '_depth_image_registered_led150_middle/'
SavePath_depth_image_registered_led150_low = SavePath_depth_image_registered_led150 + '/' + Savename + '_depth_image_registered_led150_low/'
#led100
SavePath_depth_image_registered_led100_high = SavePath_depth_image_registered_led100 + '/' + Savename + '_depth_image_registered_led100_high/'
SavePath_depth_image_registered_led100_middle = SavePath_depth_image_registered_led100 + '/' + Savename + '_depth_image_registered_led100_middle/'
SavePath_depth_image_registered_led100_low = SavePath_depth_image_registered_led100 + '/' + Savename + '_depth_image_registered_led100_low/'
#depth_data
SavePath_depth_data = SavePath + '/' + Savename +'_depth_data/'
SavePath_depth_data_led050 = SavePath_depth_data + '/' + Savename +'_depth_data_led050/'
SavePath_depth_data_led150 = SavePath_depth_data + '/' + Savename +'_depth_data_led150/'
SavePath_depth_data_led100 = SavePath_depth_data + '/' + Savename +'_depth_data_led100/'
#led050
SavePath_depth_data_led050_high = SavePath_depth_data_led050 + '/' + Savename + '_depth_data_led050_high/'
SavePath_depth_data_led050_middle = SavePath_depth_data_led050 + '/' + Savename + '_depth_data_led050_middle/'
SavePath_depth_data_led050_low = SavePath_depth_data_led050 + '/' + Savename + '_depth_data_led050_low/'
#led150
SavePath_depth_data_led150_high = SavePath_depth_data_led150 + '/' + Savename + '_depth_data_led150_high/'
SavePath_depth_data_led150_middle = SavePath_depth_data_led150 + '/' + Savename + '_depth_data_led150_middle/'
SavePath_depth_data_led150_low = SavePath_depth_data_led150 + '/' + Savename + '_depth_data_led150_low/'
#led100
SavePath_depth_data_led100_high = SavePath_depth_data_led100 + '/' + Savename + '_depth_data_led100_high/'
SavePath_depth_data_led100_middle = SavePath_depth_data_led100 + '/' + Savename + '_depth_data_led100_middle/'
SavePath_depth_data_led100_low = SavePath_depth_data_led100 + '/' + Savename + '_depth_data_led100_low/'
#camera_info
SavePath_camera_info = SavePath + '/' + Savename +'_camera_info/'
SavePath_camera_info_rgb = SavePath_camera_info + '/' + Savename +'_rgb/'
SavePath_camera_info_depth = SavePath_camera_info + '/' + Savename +'_depth/'

class Camera:
	def __init__(self):
		self.bridge = CvBridge()
		#item_place_combination_Counter
		self.CombinationCount_high=1
		self.CombinationCount_middle=0
		self.CombinationCount_low=0		
		#Trigger
		self.high_Trigger = False
		self.middle_Trigger = False
		self.low_Trigger = False
		self.Count_Trigger_high = True
		self.Count_Trigger_middle = False
		self.Count_Trigger_low = False
		#
		self.CaptureTrigger_rgb = False
		self.CaptureTrigger_depth = False
		self.CaptureTrigger_depth_registered =False
		self.CaptureTrigger_depth_data = False
		#info_Trigger
		self.Camera_info_rgb_Trigger = False
		self.Camera_info_depth_Trigger = False
		#camerainfo
		self.camera_information_rgb = CameraInfo()
		self.camera_information_depth = CameraInfo()
		
	def CreateFolder(self,SavePath):
		if not SavePath.endswith('/'):
			SavePath = SavePath + '/'
		if not os.path.exists(SavePath):
			os.makedirs(SavePath)
		#rgb_image
		if not os.path.exists(SavePath_rgb):
			os.makedirs(SavePath_rgb)
		if not os.path.exists(SavePath_rgb_led050):
			os.makedirs(SavePath_rgb_led050)
		if not os.path.exists(SavePath_rgb_led150):
			os.makedirs(SavePath_rgb_led150)
		if not os.path.exists(SavePath_rgb_led100):
			os.makedirs(SavePath_rgb_led100)
		#led050
		if not os.path.exists(SavePath_rgb_led050_high):
			os.makedirs(SavePath_rgb_led050_high)
		if not os.path.exists(SavePath_rgb_led050_middle):
			os.makedirs(SavePath_rgb_led050_middle)
		if not os.path.exists(SavePath_rgb_led050_low):
			os.makedirs(SavePath_rgb_led050_low)
		#led150
		if not os.path.exists(SavePath_rgb_led150_high):
			os.makedirs(SavePath_rgb_led150_high)
		if not os.path.exists(SavePath_rgb_led150_middle):
			os.makedirs(SavePath_rgb_led150_middle)
		if not os.path.exists(SavePath_rgb_led150_low):
			os.makedirs(SavePath_rgb_led150_low)
		#led100
		if not os.path.exists(SavePath_rgb_led100_high):
			os.makedirs(SavePath_rgb_led100_high)
		if not os.path.exists(SavePath_rgb_led100_middle):
			os.makedirs(SavePath_rgb_led100_middle)
		if not os.path.exists(SavePath_rgb_led100_low):
			os.makedirs(SavePath_rgb_led100_low)
		#depth_image
		if not os.path.exists(SavePath_depth_image):
			os.makedirs(SavePath_depth_image)
		if not os.path.exists(SavePath_depth_image_led050):
			os.makedirs(SavePath_depth_image_led050)
		if not os.path.exists(SavePath_depth_image_led150):
			os.makedirs(SavePath_depth_image_led150)
		if not os.path.exists(SavePath_depth_image_led100):
			os.makedirs(SavePath_depth_image_led100)
		#led050
		if not os.path.exists(SavePath_depth_image_led050_high):
			os.makedirs(SavePath_depth_image_led050_high)
		if not os.path.exists(SavePath_depth_image_led050_middle):
			os.makedirs(SavePath_depth_image_led050_middle)
		if not os.path.exists(SavePath_depth_image_led050_low):
			os.makedirs(SavePath_depth_image_led050_low)
		#led150
		if not os.path.exists(SavePath_depth_image_led150_high):
			os.makedirs(SavePath_depth_image_led150_high)
		if not os.path.exists(SavePath_depth_image_led150_middle):
			os.makedirs(SavePath_depth_image_led150_middle)
		if not os.path.exists(SavePath_depth_image_led150_low):
			os.makedirs(SavePath_depth_image_led150_low)
		#led100
		if not os.path.exists(SavePath_depth_image_led100_high):
			os.makedirs(SavePath_depth_image_led100_high)
		if not os.path.exists(SavePath_depth_image_led100_middle):
			os.makedirs(SavePath_depth_image_led100_middle)
		if not os.path.exists(SavePath_depth_image_led100_low):
			os.makedirs(SavePath_depth_image_led100_low)
		#depth_image_registered
		if not os.path.exists(SavePath_depth_image_registered):
			os.makedirs(SavePath_depth_image_registered)
		if not os.path.exists(SavePath_depth_image_registered_led050):
			os.makedirs(SavePath_depth_image_registered_led050)
		if not os.path.exists(SavePath_depth_image_registered_led150):
			os.makedirs(SavePath_depth_image_registered_led150)
		if not os.path.exists(SavePath_depth_image_registered_led100):
			os.makedirs(SavePath_depth_image_registered_led100)
		#led050
		if not os.path.exists(SavePath_depth_image_registered_led050_high):
			os.makedirs(SavePath_depth_image_registered_led050_high)
		if not os.path.exists(SavePath_depth_image_registered_led050_middle):
			os.makedirs(SavePath_depth_image_registered_led050_middle)
		if not os.path.exists(SavePath_depth_image_registered_led050_low):
			os.makedirs(SavePath_depth_image_registered_led050_low)
		#led150
		if not os.path.exists(SavePath_depth_image_registered_led150_high):
			os.makedirs(SavePath_depth_image_registered_led150_high)
		if not os.path.exists(SavePath_depth_image_registered_led150_middle):
			os.makedirs(SavePath_depth_image_registered_led150_middle)
		if not os.path.exists(SavePath_depth_image_registered_led150_low):
			os.makedirs(SavePath_depth_image_registered_led150_low)
		#led100
		if not os.path.exists(SavePath_depth_image_registered_led100_high):
			os.makedirs(SavePath_depth_image_registered_led100_high)
		if not os.path.exists(SavePath_depth_image_registered_led100_middle):
			os.makedirs(SavePath_depth_image_registered_led100_middle)
		if not os.path.exists(SavePath_depth_image_registered_led100_low):
			os.makedirs(SavePath_depth_image_registered_led100_low)
		#depth_data
		if not os.path.exists(SavePath_depth_data):
			os.makedirs(SavePath_depth_data)
		if not os.path.exists(SavePath_depth_data_led050):
			os.makedirs(SavePath_depth_data_led050)
		if not os.path.exists(SavePath_depth_data_led150):
			os.makedirs(SavePath_depth_data_led150)
		if not os.path.exists(SavePath_depth_data_led100):
			os.makedirs(SavePath_depth_data_led100)
		#led050
		if not os.path.exists(SavePath_depth_data_led050_high):
			os.makedirs(SavePath_depth_data_led050_high)
		if not os.path.exists(SavePath_depth_data_led050_middle):
			os.makedirs(SavePath_depth_data_led050_middle)
		if not os.path.exists(SavePath_depth_data_led050_low):
			os.makedirs(SavePath_depth_data_led050_low)
		#led150
		if not os.path.exists(SavePath_depth_data_led150_high):
			os.makedirs(SavePath_depth_data_led150_high)
		if not os.path.exists(SavePath_depth_data_led150_middle):
			os.makedirs(SavePath_depth_data_led150_middle)
		if not os.path.exists(SavePath_depth_data_led150_low):
			os.makedirs(SavePath_depth_data_led150_low)
		#led100
		if not os.path.exists(SavePath_depth_data_led100_high):
			os.makedirs(SavePath_depth_data_led100_high)
		if not os.path.exists(SavePath_depth_data_led100_middle):
			os.makedirs(SavePath_depth_data_led100_middle)
		if not os.path.exists(SavePath_depth_data_led100_low):
			os.makedirs(SavePath_depth_data_led100_low)
		#camera_info
		if not os.path.exists(SavePath_camera_info):		
			os.makedirs(SavePath_camera_info)
		if not os.path.exists(SavePath_camera_info_rgb):		
			os.makedirs(SavePath_camera_info_rgb)
		if not os.path.exists(SavePath_camera_info_depth):		
			os.makedirs(SavePath_camera_info_depth)

	def record_callback(self,CartesianPose):
		height = CartesianPose.pose.position.z	
		#z=0.65m
		if  0.645<height and height<0.654:
			self.high_Trigger = True
			self.middle_Trigger = False
			self.low_Trigger = False
		#z=0.60m
		if 0.595<height and height<0.604:
			self.high_Trigger = False
			self.middle_Trigger = True
			self.low_Trigger = False
		#z=0.55m
		if 0.545<height and height<0.554:
			self.high_Trigger = False
			self.middle_Trigger = False
			self.low_Trigger = True
	def rgb_callback(self,Image_rgb):
		try:
			self.rgb_image_cv2 = self.bridge.imgmsg_to_cv2(Image_rgb,"bgr8")
			self.CaptureTrigger_rgb = True
		except CvBridgeError,e:
			print e

	def depth_callback(self,Image_depth):
		try:
			self.depth_image_cv2 = self.bridge.imgmsg_to_cv2(Image_depth,"16UC1")
			self.CaptureTrigger_depth = True
		except CvBridgeError,e:
			print e

	def depth_registered_callback(self,Image_depth_registered):
		try:
			self.depth_image_registered_cv2 = self.bridge.imgmsg_to_cv2(Image_depth_registered,"16UC1")
			self.CaptureTrigger_depth_registered = True
			
		except CvBridgeError,e:
			print e

	def depth_data_callback(self,depth_data):
		try:
			self.depth_data_cv2 = self.bridge.imgmsg_to_cv2(depth_data,"16UC1")
			self.depth_array = np.array(self.depth_data_cv2, dtype=np.int16)
			self.CaptureTrigger_depth_data = True	
		except CvBridgeError,e:
			print e

	def camera_information_rgb_callback(self,Camera_information_rgb):
		self.camera_information_rgb = Camera_information_rgb
		self.Camera_info_rgb_Trigger = True

	def camera_information_depth_callback(self,Camera_information_depth):
		self.camera_information_depth = Camera_information_depth
		self.Camera_info_depth_Trigger = True

	def main(self):
		rospy.init_node('camera_service')
		self.CreateFolder(SavePath)
		height_sub = rospy.Subscriber('/iiwa/state/CartesianPose', PoseStamped, self.record_callback, queue_size=1)
		rgb = rospy.Subscriber("/camera/rgb/image_raw",Image,self.rgb_callback)
		depth = rospy.Subscriber("/camera/depth/image_raw",Image,self.depth_callback)
		depth_registered = rospy.Subscriber("/camera/depth_registered/sw_registered/image_rect_raw",Image,self.depth_registered_callback)		
		depth_data = rospy.Subscriber("/camera/depth/image_raw",Image,self.depth_data_callback)
		camera_information_color = rospy.Subscriber("/camera/rgb/camera_info",CameraInfo,self.camera_information_rgb_callback)
		camera_information_depth = rospy.Subscriber("/camera/depth/camera_info",CameraInfo,self.camera_information_depth_callback)
		#led_publisher
		led_pub = rospy.Publisher('LEDchatter', String, queue_size=10)
		str = "00L1" # Channel 00, switch ON
		led_pub.publish(str)
		rospy.sleep(1.)
		###
		led_intensity=[]
		led_intensity=["_led150","_led100","_led050"]
		led_str=[]
		led_str=["00F150","00F100","00F050"]
		SavePath_rgb_high=[]
		SavePath_rgb_high=[SavePath_rgb_led150_high,SavePath_rgb_led100_high,SavePath_rgb_led050_high]
		SavePath_rgb_middle=[]
		SavePath_rgb_middle=[SavePath_rgb_led150_middle,SavePath_rgb_led100_middle,SavePath_rgb_led050_middle]
		SavePath_rgb_low=[]
		SavePath_rgb_low=[SavePath_rgb_led150_low,SavePath_rgb_led100_low,SavePath_rgb_led050_low]

		SavePath_depth_image_high=[]
		SavePath_depth_image_high=[SavePath_depth_image_led150_high,SavePath_depth_image_led100_high,SavePath_depth_image_led050_high]
		SavePath_depth_image_middle=[]
		SavePath_depth_image_middle=[SavePath_depth_image_led150_middle,SavePath_depth_image_led100_middle,SavePath_depth_image_led050_middle]
		SavePath_depth_image_low=[]
		SavePath_depth_image_low=[SavePath_depth_image_led150_low,SavePath_depth_image_led100_low,SavePath_depth_image_led050_low]

		SavePath_depth_image_registered_high=[]
		SavePath_depth_image_registered_high=[SavePath_depth_image_registered_led150_high,SavePath_depth_image_registered_led100_high,SavePath_depth_image_registered_led050_high]
		SavePath_depth_image_registered_middle=[]
		SavePath_depth_image_registered_middle=[SavePath_depth_image_registered_led150_middle,SavePath_depth_image_registered_led100_middle,SavePath_depth_image_registered_led050_middle]
		SavePath_depth_image_registered_low=[]
		SavePath_depth_image_registered_low=[SavePath_depth_image_registered_led150_low,SavePath_depth_image_registered_led100_low,SavePath_depth_image_registered_led050_low]

		SavePath_depth_data_high=[]
		SavePath_depth_data_high=[SavePath_depth_data_led150_high,SavePath_depth_data_led100_high,SavePath_depth_data_led050_high]
		SavePath_depth_data_middle=[]
		SavePath_depth_data_middle=[SavePath_depth_data_led150_middle,SavePath_depth_data_led100_middle,SavePath_depth_data_led050_middle]
		SavePath_depth_data_low=[]
		SavePath_depth_data_low=[SavePath_depth_data_led150_low,SavePath_depth_data_led100_low,SavePath_depth_data_led050_low]
		rate = rospy.Rate(10)

		#camera_info_rgb
		if self.Camera_info_rgb_Trigger == True:
			Filename_camera_information_rgb = Savename + "_" + "camera_information_rgb_"
			np.savetxt(SavePath_camera_info_rgb+Filename_camera_information_rgb+"D.txt" ,self.camera_information_rgb.D)
			np.savetxt(SavePath_camera_info_rgb+Filename_camera_information_rgb+"K.txt" ,self.camera_information_rgb.K)
			np.savetxt(SavePath_camera_info_rgb+Filename_camera_information_rgb+"R.txt" ,self.camera_information_rgb.R)
			np.savetxt(SavePath_camera_info_rgb+Filename_camera_information_rgb+"P.txt" ,self.camera_information_rgb.P)
		#camera_info_depth
		if self.Camera_info_depth_Trigger == True:
			Filename_camera_information_depth = Savename + "_" + "camera_information_depth_"
			np.savetxt(SavePath_camera_info_depth+Filename_camera_information_depth+"D.txt" ,self.camera_information_depth.D)
			np.savetxt(SavePath_camera_info_depth+Filename_camera_information_depth+"K.txt" ,self.camera_information_depth.K)
			np.savetxt(SavePath_camera_info_depth+Filename_camera_information_depth+"R.txt" ,self.camera_information_depth.R)
			np.savetxt(SavePath_camera_info_depth+Filename_camera_information_depth+"P.txt" ,self.camera_information_depth.P)

		for j in range(0,9):
			while self.high_Trigger == False:
				print("wait for high trigger")
				rospy.sleep(1.0)
			if self.high_Trigger == True:
				print("high")
				while self.CaptureTrigger_rgb == False:
					rospy.sleep(1.0)
				#change led_intensity
				for i in range(3):
					rospy.sleep(1.)
					print("high_rgb")
					str = led_str[i] # Channel 00, power 100
					led_pub.publish(str)
					rospy.sleep(1.)
					if self.CaptureTrigger_rgb == True:	
						Filename_rgb = Savename + "_" +'{0:0>3}'.format(self.CombinationCount_high)+led_intensity[i]+"_high"+"_rgb"+".png"
						cv2.imwrite(SavePath_rgb_high[i]+"/"+Filename_rgb,self.rgb_image_cv2)
						print(led_intensity[i])
					if self.CaptureTrigger_depth == True:
						Filename_depth = Savename + "_" +'{0:0>3}'.format(self.CombinationCount_high)+led_intensity[i]+"_high"+"_depth"+".png"
						cv2.imwrite(SavePath_depth_image_high[i]+"/"+Filename_depth,self.depth_image_cv2)
						print('depth_image')
					if self.CaptureTrigger_depth_registered == True:
						Filename_depth_registered = Savename+"_"+'{0:0>3}'.format(self.CombinationCount_high)+led_intensity[i]+"_high"+"_depth_registered"+".png"
						cv2.imwrite(SavePath_depth_image_registered_high[i]+"/"+Filename_depth_registered,self.depth_image_registered_cv2)
						print('depth_registered')
					if self.CaptureTrigger_depth_data == True:
						Filename_depth_data = Savename + "_" +'{0:0>3}'.format(self.CombinationCount_high)+led_intensity[i]+"_high"+"_depth_data_"+".dat"
						self.depth_array.dump(SavePath_depth_data_high[i]+"/"+Filename_depth_data)
						print('depth_data')
				#update counter
				if self.Count_Trigger_high ==  True:
					self.CombinationCount_middle += 1
					self.Count_Trigger_middle = True
				print(self.CombinationCount_high)
				self.high_Trigger = False
				self.Count_Trigger_high = False
			while self.middle_Trigger == False:
				print("wait for middle trigger")
				rospy.sleep(1.0)
		#middle_height
			if self.middle_Trigger == True:
				print("middle")
				while self.CaptureTrigger_rgb == False:
					rospy.sleep(1.0)
				#change led_intensity
				for i in range(3):
					rospy.sleep(1.)
					print("middle_rgb")
					str = led_str[i] # Channel 00, power 100
					led_pub.publish(str)
					rospy.sleep(1.)
					if self.CaptureTrigger_rgb == True:	
						Filename_rgb = Savename + "_" +'{0:0>3}'.format(self.CombinationCount_middle)+led_intensity[i]+"_middle"+"_rgb"+".png"
						cv2.imwrite(SavePath_rgb_middle[i]+"/"+Filename_rgb,self.rgb_image_cv2)
						print(led_intensity[i])
					if self.CaptureTrigger_depth == True:
						Filename_depth = Savename + "_" +'{0:0>3}'.format(self.CombinationCount_middle)+led_intensity[i]+"_middle"+"_depth"+".png"
						cv2.imwrite(SavePath_depth_image_middle[i]+"/"+Filename_depth,self.depth_image_cv2)
						print('depth_image')
					if self.CaptureTrigger_depth_registered == True:
						Filename_depth_registered = Savename+"_"+'{0:0>3}'.format(self.CombinationCount_middle)+led_intensity[i]+"_middle"+"_depth_registered"+".png"
						cv2.imwrite(SavePath_depth_image_registered_middle[i]+"/"+Filename_depth_registered,self.depth_image_registered_cv2)
						print('depth_registered')
					if self.CaptureTrigger_depth_data == True:
						Filename_depth_data = Savename + "_" +'{0:0>3}'.format(self.CombinationCount_middle)+led_intensity[i]+"_middle"+"_depth_data_"+".dat"
						self.depth_array.dump(SavePath_depth_data_middle[i]+"/"+Filename_depth_data)
						print('depth_data')
				#update counter
				if self.Count_Trigger_middle == True:
					self.CombinationCount_low += 1
					self.Count_Trigger_low = True
				print(self.CombinationCount_middle)
				self.middle_Trigger = False
				self.Count_Trigger_middle = False
			while self.low_Trigger == False:
				print("wait for low_Trigger")
				rospy.sleep(1.0)
		#low_height
			if self.low_Trigger == True:
				print("low")
				while self.CaptureTrigger_rgb == False:
					rospy.sleep(1.0)
				#change led_intensity
				for i in range(3):
					rospy.sleep(1.)
					print("low_rgb")
					str = led_str[i] # Channel 00, power 100
					led_pub.publish(str)
					rospy.sleep(1.)
					if self.CaptureTrigger_rgb == True:	
						Filename_rgb = Savename + "_" +'{0:0>3}'.format(self.CombinationCount_low)+led_intensity[i]+"_low"+"_rgb"+".png"
						cv2.imwrite(SavePath_rgb_low[i]+"/"+Filename_rgb,self.rgb_image_cv2)
						print(led_intensity[i])
					if self.CaptureTrigger_depth == True:
						Filename_depth = Savename + "_" +'{0:0>3}'.format(self.CombinationCount_low)+led_intensity[i]+"_low"+"_depth"+".png"
						cv2.imwrite(SavePath_depth_image_low[i]+"/"+Filename_depth,self.depth_image_cv2)
						print('depth_image')
					if self.CaptureTrigger_depth_registered == True:
						Filename_depth_registered = Savename+"_"+'{0:0>3}'.format(self.CombinationCount_low)+led_intensity[i]+"_low"+"_depth_registered"+".png"
						cv2.imwrite(SavePath_depth_image_registered_low[i]+"/"+Filename_depth_registered,self.depth_image_registered_cv2)
						print('depth_registered')
					if self.CaptureTrigger_depth_data == True:
						Filename_depth_data = Savename + "_" +'{0:0>3}'.format(self.CombinationCount_low)+led_intensity[i]+"_low"+"_depth_data_"+".dat"
						self.depth_array.dump(SavePath_depth_data_low[i]+"/"+Filename_depth_data)
						print('depth_data')
				#update counter
				if self.Count_Trigger_low == True:
					self.CombinationCount_high += 1
					self.Count_Trigger_high = True
				print(self.CombinationCount_low)
				self.low_Trigger = False
				self.Count_Trigger_low = False
				rate.sleep()
			j=j+1

Camera= Camera()
Camera.main()
rospy.spin()