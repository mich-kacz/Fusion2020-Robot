import rclpy
import pymysql
import serial
import os.path
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, Float64


class Automated_driving(Node):
    
    offset = 0
    is_line = 0
    frame = 0
    counter = 0
    fsensor = 0
    count_bd = 0
    last_frames = []
    flag=0

    def __init__(self):
        super().__init__('auto_mode_node')
        self.subscription=self.create_subscription(Float64MultiArray, 'auto_mode_node', self.timer_callback, 10)
        self.subscription
        self.subscription_2=self.create_subscription(Float64, 'manual', self.driving_mode,10)
        self.subscription_2
        

        try:
            self.ser=serial.Serial("/dev/ttyUSB0", 19200)
        except:
            print("Uart not connected")
    
        timer_period=1
        self.timer=self.create_timer(timer_period, self.frame_creation)

    def frame_creation(self): #This is main function to control everything

        if self.flag==0:
            return

        # Display_offset
        self.get_logger().info('Offset: "%f"' % self.offset)
        self.get_logger().info('Lines: "%f"' % self.is_line)
        
        # Get info from data base
        self.data_base_info()

        # Building frame from offset
        self.frame=self.frame_from_offset(self.offset)
        
        # When robot cant recognize lanes or is just one
        self.frame=self.numb_of_lanes(self.frame, self.is_line)

        # When sensor shows critical value
        self.frame=self.sensor_frame(self.frame, self.fsensor)

        # Sending frame by UART
        self.send_frame(self.frame)
    
        # Update of data base
        self.data_base_update()


    def timer_callback(self, msg): # Function is recieving data from subscriber
        self.offset= msg.data[0]
        self.is_line=msg.data[1]
        self.fsensor=msg.data[2]

    def driving_mode(self, msg):
        flag=msg.data
        if flag >19999:
          self.flag=1
        else:
          self.flag=0

    def frame_from_offset(self, offset):
        pre_frame=0

        # Drive forward
        if offset<5 and offset >-5:
            pre_frame=13300
        
        # Drive almost forward
        if (offset >5 and offset < 10) or (offset <-5 and offset >-10):
            if offset<0:
                pre_frame=12300
            else:
                pre_frame=13200

        # Just Turning
        if offset >=10 or offset <=-10:
            if offset <0:
                pre_frame=10200
            else:
                pre_frame=12000

        # When camera is detecting bullshit
        if offset > 50 or offset < -50:
            pre_frame=10000

        return pre_frame

    def numb_of_lanes(self, pre_frame, lanes_numb):
        
        # No lines detected
        if lanes_numb==0:
            pre_frame=10000
        # Just one line detected
        elif lanes_numb==1:
            if self.count_bd<5:
                self.last_frames[4][0]=10000
                self.last_frames[3][0]=10000
                self.last_frames[2][0]=10000
                self.last_frames[1][0]=10000
            last=self.last_frames[4][0]
            if (self.last_frames[3][0] == last and self.last_frames[2][0]!= last) or self.last_frames[3][0] != last:
                pre_frame=last
            else:
                frame=10000
        # 2 lines detected
        elif lanes_numb==2:
            pre_frame=pre_frame
        else:
            pre_frame=10000

        return pre_frame

    def sensor_frame(self, pre_frame, fsensor): # Function is making frame depends from sensors value
        if fsensor<45:
            pre_frame=10000
        else:
            pre_frame=pre_frame

        return pre_frame


    def data_base_info(self): # Function is downloading data from data base
        try:
           # conn=sqlite3.connect('/home/ubuntu/dev_ws/src/fusion2020/fusion2020/auto_logs.db')
           conn=pymysql.connect(host='178.219.136.30', user='admin', passwd='fusion2020', database='HCR')
        except:
            print("TUTAJ")
        c=conn.cursor()
        count=c.execute('SELECT COUNT(NR) FROM AUTO_LOGS')
        self.count_db=count
        if self.count_bd>5:
            last_5=c.execute("SELECT FRAME FROM AUTO_LOGS WHERE NR>=('%d'-5)" %self.count_db)
            self.last_frames=last_5
        conn.close()

    def data_base_update(self): # Function is uploading data to data base
        self.count_bd=self.count_bd+1
        #conn=sqlite3.connect('/home/ubuntu/dev_ws/src/fusion2020/fusion2020/auto_logs.db')
        conn=pymysql.connect(host='178.219.136.30', user='admin', passwd='fusion2020', database='HCR')
        c=conn.cursor()
        c.execute("INSERT INTO AUTO_LOGS VALUES(%s, %s, %s, %s, CURRENT_TIMESTAMP)",(self.count_bd, self.frame, self.is_line, self.fsensor))
        conn.commit()
        conn.close()

    def send_frame(self, frame):
        try:
            self.ser.write(frame.encode())
            print (frame)
        except:
            print("UART error!\n")


def main(args=None):

        #conn=sqlite3.connect('/home/ubuntu/dev_ws/src/fusion2020/fusion2020/auto_logs.db')
        conn=pymysql.connect(host='178.219.136.30', user='admin', passwd='fusion2020', database='HCR')
        c=conn.cursor()
        c.execute("DELETE FROM AUTO_LOGS")
        conn.commit()
        conn.close()
        rclpy.init(args=args)
        automated_driving=Automated_driving()

        rclpy.spin(automated_driving)

        automated_driving.destroy_node()

        rclpy.shutdown()

if __name__=='__main__':
    main()


