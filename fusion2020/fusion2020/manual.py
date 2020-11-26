import rclpy
from rclpy.node import Node
import serial
from std_msgs.msg import Float64
from time import sleep
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

    def __init__(self):
        super().__init__('manual_control')
        self.subscription = self.create_subscription(Float64, 'manual', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning
        try:
            self.ser=serial.Serial("/dev/ttyACM0", 19200)
        except:
            print("Uart not connected")

    def listener_callback(self, msg):
        global val_x, itemp, right_motor_pwm, left_motor_pwm, tright_motor_pwm, tleft_motor_pwm, tright_motor_direction, tleft_motor_direction, lmd_pwm_r, lmd_pwm_l, lmd_dir_r, lmd_dir_l, flag
        val_x=int(msg.data)
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
                if(lmd_pwm_r==lmd_pwm_l==1 or lmd_pwm_r==lmd_pwm_l==2):
                    right_motor_pwm=lmd_pwm_r+1
                    left_motor_pwm=lmd_pwm_l-1
                else:
                    right_motor_pwm=lmd_pwm_r+2
                    left_motor_pwm=lmd_pwm_l-2
                right_motor_direction=lmd_dir_r
                left_motor_direction=lmd_dir_l
                flag=1
            elif(tright_motor_direction==0 and tleft_motor_direction==1):
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

        frame=str(controls)
        print(frame)
        try:
            self.ser.write(frame.encode())
        except:
            print("UART error!\n")

        self.Read_Uart()

    def Read_Uart(self):
        try:
            ser_bytes=self.ser.readline()
            print('Dane z Uartu: ')
            print(str(ser_bytes.decode())+'\n')
                
        except:
            print('Can not receive data from Uart')


def main(args=None):
    rclpy.init(args=args)
    manual_control = ManualControl()
    rclpy.spin(manual_control)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
