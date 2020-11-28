import cv2
import numpy as np
import socket
import struct
import math
import rclpy
import serial
from time import process_time
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

class Camera_capture(Node):
	
	sensor='START'
	
	def __init__(self):
		super().__init__('camera_capture')
		self.publisher_=self.create_publisher(Float64MultiArray, 'auto_mode_node', 10 )
		
		try:
			self.ser=serial.Serial("/dev/ttyACM0", 19200)
		except:
			print('Uart not connected')
		
		#Constructor creates socket, port and gets ip from input
		self.Client_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.server_ip=input('Podaj ip serwera - ')
		self.adress=5006
	
		

	
	#Wykrycie konturów na obrazie
	def detect_edges(self, image):
    		image_HSV=cv2.cvtColor(image,cv2.COLOR_BGR2HSV) #Zamiana obrazu na HSV(TEN SAM KOLOR MIMO ODCIENIU)
    		lower_blue = np.array([145, 40, 40]) #Dolna granica koloru na skali HUE
    		upper_blue = np.array([179, 255, 255])#Gorna granica koloru(to jest pierwszy parametr, reszta bez zmian!!)
    		mask = cv2.inRange(image_HSV, lower_blue, upper_blue)#Zostawiam tylko kolory o okreslonych granicach
    		edges = cv2.Canny(mask, 200, 400)#Funkcja znajduje kontury(Parametry zostaja bez zmian!!!)
    		return edges
    		
    		
    	#Wymazanie czesci obrazu ktory nas nie interesuje
	def erased_area(self, image):
    		height, width=image.shape#Wymiary obrazu
    		mask=np.zeros_like(image)#Tablica zer wielkosci obrazu
    		polygon = np.array([[(0, height * 1 / 2), 
                         (width, height * 1 / 2),
                         (width, height), 
                         (0, height),]], np.int32)#Funkcja okresla obszar wymazywania(np.1/2)
    		cv2.fillPoly(mask, polygon, 255)#Dopasowanie obszaru zer do wymiaru
    		cropped_edges = cv2.bitwise_and(image, mask)#Wymazanie obszaru ktory nas nie interesuje
    		return cropped_edges
    		
    		
    	#Wykrywa fragmenty lini 
	def detect_line_segments(self, image):
    		rho=1 #Dystans od poczatku dla transformacji Hough'a
    		angle=np.pi/180 #precyzja kata w radianach
    		min_threshold=20 #minimal number of votes to consider as a line
    		segments=cv2.HoughLinesP(image, rho, angle, min_threshold,
                             np.array([]),  minLineLength=5, maxLineGap=4)
    		return segments
    		
	def make_points(self, image, line):
		height, width, _ = image.shape
		slope, intercept = line
		y1 = height  # bottom of the frame
		y2 = int(y1 * 1 / 2)  # make points from middle of the frame down
		
		if(slope==0):
			slope=0.001
		# bound the coordinates within the frame
		x1=max(-width, min(2*width, int((y1 - intercept)/slope)))
		x2=max(-width, min(2*width, int((y2 - intercept)/slope)))
		return [[x1, y1, x2, y2]]
    		
	def creating_two_lanes(self, image, segments):
		lane_lines = []
		if segments is None:
			#print('No line_segment segments detected')
			return lane_lines
    
		height, width, _ = image.shape
		left_fit = []
		right_fit = []
		#Regions of lines
		boundary = 1/2 #Dziele ekran na czesci w ktorych powinny byc linie
		left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
		right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

		for line_segment in segments:
			for x1, y1, x2, y2 in line_segment:
				if x1 == x2:
					#print('skipping vertical line segment (slope=inf): %s' % line_segment)
					continue
				fit = np.polyfit((x1, x2), (y1, y2), 1)
				slope = fit[0]
				intercept = fit[1]
				if slope < 0:
					if x1 < left_region_boundary and x2 < left_region_boundary:
						left_fit.append((slope, intercept))
				else:
					if x1 > right_region_boundary and x2 > right_region_boundary:
						right_fit.append((slope, intercept))
					
		left_fit_average = np.average(left_fit, axis=0)
		if len(left_fit) > 0:
			lane_lines.append(self.make_points(image, left_fit_average))
			
		right_fit_average = np.average(right_fit, axis=0)
		if len(right_fit) > 0:
			lane_lines.append(self.make_points(image, right_fit_average))
		
		return lane_lines
	
	
	def display_lines(self, image, lines, line_color=(0, 255, 0), line_width=4):
    		line_image = np.zeros_like(image)
    		if lines is not None:
       		 for line in lines:
       		 	if line is not None:
            				for x1, y1, x2, y2 in line:
                				cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    		line_image = cv2.addWeighted(image, 0.8, line_image, 1, 1)
    		return line_image
    		
    	
	def Position_control(self, image, lines, offset=0):
		count=0
		height, width, _ = image.shape
		text_sensor_coordinates= (int(width-width*2/3), int(height-height*5/6))
		for elem in lines:
			count+=1
		if count==2:
			_, _, left_line, _ = lines[0][0]
			_, _, right_line, _ = lines[1][0]
			center_start=(int((left_line+right_line)/2), int(height-height/10))
			center_end=(int((left_line+right_line)/2), int(2*height/3))
			center=(int(width/2), int(4*height/5))
			text_coordinates=(int(width-width/6), int(height-height/10))
		   
			image = cv2.arrowedLine(image, center_start, center_end, (0, 255, 0), 5)
			image=cv2.circle(image, center, 15, (255, 0, 0), 4)
		    
			offset=center[0]-center_start[0] #Dodatni offset->skret w lewo
		    
			if offset>0:
				cv2.putText(image,'Lewo '+ str(offset) , text_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 3)
			else:
				cv2.putText(image,'Prawo '+ str(offset) , text_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 3)
				
		cv2.putText(image, 'Czujnik: ' + str(self.sensor), text_sensor_coordinates, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 3)
			
		return image, offset, count
	
	
	def Read_Uart(self):
		try:	
			if self.ser.in_waiting>0 :
				self.sensor=self.ser.read(self.ser.in_waiting)
				self.sensor=self.sensor.decode()
				print('Odebralem')
		except:
			print('Can not receive data from uart')
	
	
	
	def send_image(self, frame):# funkcja ktora wysyla odebrany obraz
		MAX_DGRAM=2**16
		MAX_IMG_DGRAM=MAX_DGRAM-64
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
	

	def camera_start(self): #Funkcja ktora odbiera obraz z kamery
		cap=cv2.VideoCapture(0, cv2.CAP_V4L2)
		#cap.set(3, 1280)
		#cap.set(4, 720)
		t1=process_time()
		while(cap.isOpened()):
			_, frame=cap.read()
			edges=self.detect_edges(frame) #Zaznaczam kontury
			edges=self.erased_area(edges)
			segments=self.detect_line_segments(edges)
			land_lanes=self.creating_two_lanes(frame, segments)
			ready_image = self.display_lines(frame, land_lanes)
			
			if(process_time()-t1>0.2):
				self.Read_Uart()
				t1=process_time()
			
			(ready_image, offset, is_lines)=self.Position_control(ready_image, land_lanes)
			
			message=Float64MultiArray()
			message.data=[float(offset), float(is_lines)]
			self.publisher_.publish(message)
			self.send_image(ready_image)	

		cap.release()
		cv2.destroyAllWindows()
		self.Client_socket.close()
		
		

def main(args=None):
    print('Hi from robot.')
    rclpy.init(args=args)
    
    camera_capture=Camera_capture()
    
    camera_capture.camera_start()
    
    
    camera_capture.destroy_node()
    rclpy.shutdown()
    print('Bye bye')

if __name__ == '__main__':
    main()
