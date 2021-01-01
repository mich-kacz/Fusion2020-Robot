import rclpy
import sqlite3
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, String


class Automated_driving(Node):
    
    offset = 0
    is_line = 0
    frame = 0
    counter = 0
    fsensor = 0
    count_bd = 0
    last_frames = []

    def __init__(self):
        super().__init__('auto_mode_node')
        self.subscription=self.create_subscription(Float64MultiArray, 'auto_mode_node', self.timer_callback, 10)
        self.subscription
       # self.publisher_=self.create_publisher(Float64, 'manual', 10)
        timer_period=1
        self.timer=self.create_timer(timer_period, self.frame_creation)

    def frame_creation(self): #This is main function to control everything
        # Display_offset
        self.get_logger().info('Offset: "%f"' % self.offset)
        self.get_logger().info('Lines: "%f"' % self.is_line)
        
        # Get info from data base
        self.data_base_info()

        # Building frame from offset
        self.frame=self.frame_from_offset(self.offset)
        
        # When robot cant recognize lanes or is just one
        self.frame=self.numb_of_lanes(self.frame, self.is_line)

        # Update of data base
        self.data_base_update()


    def timer_callback(self, msg):
        self.offset= msg.data[0]
        self.is_line=msg.data[1]
        self.fsensor=msg.data[2]

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

    def data_base_info(self):
        conn=sqlite3.connect('AUTO_LOGS.db')
        count=conn.execute("SELECT COUNT(NR) FROM AUTO_LOGS")
        self.count_db=count.fetchall()[0][0]
        if self.count>5:
            last_5=conn.execute("SELECT FRAME FROM AUTO_LOGS WHERE NR>=('%d'-5)" %self.count_db)
            self.last_frames=last_5.fetchall()
        conn.close()

    def data_base_update(self):
        self.count=self.count+1
        conn=sqlite3.connect('AUTO_LOGS.db')
        conn.execute("INSERT INTO AUTO_LOGS VALUES('?, ?, ?, ?')", (self.count, self.frame, self.is_line, self.fsensor))
        conn.commit()
        conn.close()


def main(args=None):
        conn=sqlite3.connect('AUTO_LOGS.db')
        conn.execute("DROP TABLE AUTO_LOGS")
        conn.commit()
        conn.close()
        rclpy.init(args=args)
        automated_driving=Automated_driving()

        rclpy.spin(automated_driving)

        automated_driving.destroy_node()

        rclpy.shutdown()

if __name__=='__main__':
    main()


