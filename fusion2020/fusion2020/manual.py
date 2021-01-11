import rclpy
from rclpy.node import Node
import serial
from std_msgs.msg import Float64, String
from time import sleep
import pymysql
## global variables
val_x=0
itemp=0
base_speed=0
tleft_motor_pwm=0
tright_motor_pwm=0
tleft_motor_direction=0
tright_motor_direction=0
right_motor_pwm=0
left_motor_pwm=0
flag=0
lmd_pwm_r=0
lmd_pwm_l=0
lmd_dir_l=0
lmd_dir_r=0
up=0


class ManualControl(Node):

    frame_bd=0
    count_bd = 0
    last_frames = []
    

    def __init__(self):
        super().__init__('manual_control')
        self.subscription = self.create_subscription(Float64, 'manual', self.listener_callback, 10)
        self.publisher_=self.create_publisher(String, 'sensors', 10)
       # timer_period=0.5
       # self.timer = self.create_timer(timer_period, self.Read_Uart)
        self.subscription  # prevent unused variable warning
        try:
            self.ser=serial.Serial("/dev/ttyUSB0", 19200)
        except:
            print("Uart not connected")

    def listener_callback(self, msg):
        global val_x, itemp, right_motor_pwm, left_motor_pwm, tright_motor_pwm, tleft_motor_pwm, tright_motor_direction, tleft_motor_direction, lmd_pwm_r, lmd_pwm_l, lmd_dir_r, lmd_dir_l, flag
        val_x=int(msg.data)

        if val_x>19999:
            return

        itemp=int(val_x/10000)
        tright_motor_pwm=int(val_x/1000 - itemp*10)
        tleft_motor_pwm=int(val_x/100 - itemp*100 - tright_motor_pwm*10)
        tright_motor_direction=int(val_x/10 - itemp*1000 - tright_motor_pwm*100 - tleft_motor_pwm*10)
        tleft_motor_direction=int(val_x - itemp*10000 - tright_motor_pwm*1000 - tleft_motor_pwm*100 - tright_motor_direction*10)
        if(flag==0):
            if(tright_motor_direction==tleft_motor_direction):
                flag=1
            else:
                flag=0
            right_motor_pwm=tright_motor_pwm
            left_motor_pwm=tleft_motor_pwm
            right_motor_direction=tright_motor_direction
            left_motor_direction=tleft_motor_direction
            lmd_pwm_r=right_motor_pwm
            lmd_pwm_l=left_motor_pwm
            lmd_dir_r=right_motor_direction
            lmd_dir_l=left_motor_direction
        if(flag==1):
            if(tright_motor_direction==1 and tleft_motor_direction==1):
                right_motor_pwm=tright_motor_pwm
                left_motor_pwm=tleft_motor_pwm
                right_motor_direction=tright_motor_direction
                left_motor_direction=tleft_motor_direction
                lmd_pwm_r=tright_motor_pwm
                lmd_pwm_l=tleft_motor_pwm
                lmd_dir_r=right_motor_direction
                lmd_dir_l=left_motor_direction               
                flag=1
            elif(tright_motor_direction==0 and tleft_motor_direction==0):
                right_motor_pwm=tright_motor_pwm
                left_motor_pwm=tleft_motor_pwm
                right_motor_direction=tright_motor_direction
                left_motor_direction=tleft_motor_direction
                flag=0
            elif(tright_motor_direction==1 and tleft_motor_direction==0):
                if(tright_motor_pwm!=lmd_pwm_l):
                    lmd_pwm_r=lmd_pwm_l=tright_motor_pwm

                if (right_motor_pwm==1 or right_motor_pwm==2):
                    left_motor_pwm=0
                if (right_motor_pwm==3 or right_motor_pwm==4):
                    left_motor_pwm=1
                if (right_motor_pwm==5 or right_motor_pwm==6):
                    left_motor_pwm=2
                if (right_motor_pwm==7 or right_motor_pwm==8):
                    left_motor_pwm=3
                if (right_motor_pwm==9):
                    left_motor_pwm=4
                
                right_motor_pwm=lmd_pwm_r

                right_motor_direction=lmd_dir_r
                left_motor_direction=lmd_dir_l
                flag=1
            elif(tright_motor_direction==0 and tleft_motor_direction==1):
                if(tleft_motor_pwm!=lmd_pwm_r):
                    lmd_pwm_l=lmd_pwm_r=tleft_motor_pwm

                if (left_motor_pwm==1 or left_motor_pwm==2):
                    right_motor_pwm=0
                if (left_motor_pwm==3 or left_motor_pwm==4):
                    right_motor_pwm=1
                if (left_motor_pwm==5 or left_motor_pwm==6):
                    right_motor_pwm=2
                if (left_motor_pwm==7 or left_motor_pwm==8):
                    right_motor_pwm=3
                if (left_motor_pwm==9):
                    right_motor_pwm=4

                left_motor_pwm=lmd_pwm_l

                right_motor_direction=lmd_dir_r
                left_motor_direction=lmd_dir_l
                flag=1
            elif(tright_motor_direction==2 and tleft_motor_direction==2):
                left_motor_pwm=tleft_motor_pwm
                right_motor_pwm=tright_motor_pwm
                left_motor_direction=tleft_motor_direction
                right_motor_direction=tright_motor_direction
                lmd_dir_r=right_motor_direction
                lmd_dir_l=left_motor_direction 
                flag=1
            elif(tright_motor_direction==0 and tleft_motor_direction==2):
                if(tleft_motor_pwm!=lmd_pwm_r):
                    lmd_pwm_l=lmd_pwm_r=tleft_motor_pwm
                if(lmd_pwm_r==lmd_pwm_l==1 or lmd_pwm_r==lmd_pwm_l==2):
                    right_motor_pwm=lmd_pwm_r-1
                    left_motor_pwm=lmd_pwm_l+1
                else:
                    right_motor_pwm=lmd_pwm_r-2
                    left_motor_pwm=lmd_pwm_l+2
                right_motor_direction=lmd_dir_r
                left_motor_direction=lmd_dir_l
                flag=1
            elif(tright_motor_direction==2 and tleft_motor_direction==0):
                if(tright_motor_pwm!=lmd_pwm_r):
                    lmd_pwm_r=lmd_pwm_r=tleft_motor_pwm
                if(lmd_pwm_r==lmd_pwm_l==1 or lmd_pwm_r==lmd_pwm_l==2):
                    right_motor_pwm=lmd_pwm_r+1
                    left_motor_pwm=lmd_pwm_l-1
                else:
                    right_motor_pwm=lmd_pwm_r+2
                    left_motor_pwm=lmd_pwm_l-2
                right_motor_pwm=lmd_pwm_r
                left_motor_pwm=lmd_pwm_l+tleft_motor_pwm
                right_motor_direction=lmd_dir_r
                left_motor_direction=lmd_dir_l
                flag=1
        print("bieg = ", itemp)
        print("predkosc prawego silnika = ", right_motor_pwm)
        print("predkosc lewego silnika = ", left_motor_pwm)
        print("polowa = ", (right_motor_pwm+left_motor_pwm)/2)
        print("kierunek prawego silnika = ", right_motor_direction)
        print("kierunek lewego silnika = ", left_motor_direction)
        print("flag = ", flag)
        controls = itemp*10000 + right_motor_pwm*1000 + left_motor_pwm*100 + right_motor_direction*10 + left_motor_direction
        
        #Data base part
        self.frame_bd=controls
        self.data_base_info()
        self.data_base_update()


        frame=str(controls)
        print(frame)
        try:
            self.ser.write(frame.encode())
        except:
            print("UART error!\n")



    def data_base_info(self): # Function is downloading data from data base
        try:
           # conn=sqlite3.connect('/home/ubuntu/dev_ws/src/fusion2020/fusion2020/auto_logs.db')
           conn=pymysql.connect(host='178.219.136.30', user='admin', passwd='fusion2020', database='HCR')
        except:
            print("TUTAJ")
        c=conn.cursor()
        count=c.execute('SELECT COUNT(NR) FROM MANUAL_LOGS')
        self.count_db=count
        if self.count_bd>5:
            last_5=c.execute("SELECT FRAME FROM MANUAL_LOGS WHERE NR>=('%d'-5)" %self.count_db)
            self.last_frames=last_5
        conn.close()

    def data_base_update(self): # Function is uploading data to data base
        self.count_bd=self.count_bd+1
        #conn=sqlite3.connect('/home/ubuntu/dev_ws/src/fusion2020/fusion2020/auto_logs.db')
        conn=pymysql.connect(host='178.219.136.30', user='admin', passwd='fusion2020', database='HCR')
        c=conn.cursor()
        c.execute("INSERT INTO MANUAL_LOGS VALUES(%s, %s, CURRENT_TIMESTAMP)",(self.count_bd, self.frame_bd))
        conn.commit()
        conn.close()



def main(args=None):
    conn=pymysql.connect(host='178.219.136.30', user='admin', passwd='fusion2020', database='HCR')
    c=conn.cursor()
    c.execute("DELETE FROM MANUAL_LOGS")
    conn.commit()
    conn.close()
    rclpy.init(args=args)
    manual_control = ManualControl()
    rclpy.spin(manual_control)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
