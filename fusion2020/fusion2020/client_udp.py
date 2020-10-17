import cv2
import numpy as np
import socket
import struct
import math

class Camera_capture():

	def __init__(self):
		#Constructor creates socket, port and gets ip from input
		self.Client_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server_ip=input('Podaj ip serwera - ')
		self.adress=5006
	

	def camera_start(self):
		MAX_DGRAM=2**16
		MAX_IMG_DGRAM=MAX_DGRAM-64
		cap=cv2.VideoCapture(0, cv2.CAP_V4L2)
		while(cap.isOpened()):
			_, frame=cap.read()
			
			#Compress and divide on segments
			comp_frame=cv2.imencode('.jpg', frame)[1]
			data=comp_frame.tostring()
			size=len(data)
			numb_segments=math.ceil(size/(MAX_IMG_DGRAM))
			temp=0
			while numb_segments:
				temp2=min(size, temp + MAX_IMG_DGRAM)
				self.Client_socket.sendto(struct.pack("B", numb_segments) + data[temp:temp2], (self.server_ip, self.adress))
				temp=temp2
				numb_segments-=1
		cap.release()
		cv2.destroyAllWindows()
		self.Client_socket.close()

def main():
    print('Hi from robot.')
    camera_capture=Camera_capture()
    camera_capture.camera_start()
    print('Bye bye')

if __name__ == '__main__':
    main()
