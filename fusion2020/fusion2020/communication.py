import rclpy
from rclpy.node import Node
import geometry_msgs.msg as geometry
from std_msgs.msg import Float64

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('pubsub')
        self.subscription = self.create_subscription(geometry.Twist, 'cmd_vel', self.listener_callback, 10)
        self.publisher_ = self.create_publisher(Float64, 'manual', 10)

    def listener_callback(self, msg):
       
        ## STEROWANIE
        
        print("x =",msg.linear.x,", z =", msg.angular.z, ", control_vel =", msg.linear.z)
        control_vel=msg.linear.z
        if(msg.angular.z==0): ##liniowo
            if(msg.linear.x>0): ##przód
                right_motor_vel=left_motor_vel=msg.linear.x
                right_motor_dir=left_motor_dir=1
            elif(msg.linear.x<0): ##tył
                right_motor_vel=left_motor_vel=abs(msg.linear.x)
                right_motor_dir=left_motor_dir=2
            else:
                right_motor_vel=left_motor_vel=0
                right_motor_dir=left_motor_dir=0
        elif(msg.angular.z>0):##lewo (w miejscu)
            right_motor_vel=msg.angular.z
            left_motor_vel=0
            right_motor_dir=1
            left_motor_dir=0
        elif(msg.angular.z<0):##prawo (w miejscu)
            right_motor_vel=0
            left_motor_vel=abs(msg.angular.z)
            right_motor_dir=0
            left_motor_dir=1
        data_to_arduino = control_vel*10000 + right_motor_vel*1000 + left_motor_vel*100 + right_motor_dir*10 + left_motor_dir
        print(data_to_arduino)
        message = Float64()
        message.data = data_to_arduino
        self.publisher_.publish(message) 
def main(args=None):
    rclpy.init(args=args)

    pubsub = MinimalSubscriber()

    rclpy.spin(pubsub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
