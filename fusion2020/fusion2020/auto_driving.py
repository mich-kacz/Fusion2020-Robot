import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray, String


class Automated_driving(Node):
    
    offset = 0
    is_line = 0
    def __init__(self):
        super().__init__('auto_mode_node')
        self.subscription=self.create_subscription(Float64MultiArray, 'auto_mode_node', self.timer_callback, 10)
        self.subscription
       # self.publisher_=self.create_publisher(Float64, 'manual', 10)
        timer_period=1
        self.timer=self.create_timer(timer_period, self.Display_offset)

    def Display_offset(self):
        self.get_logger().info('Offset: "%f"' % self.offset)
        self.get_logger().info('Lines: "%f"' % self.is_line)


    def timer_callback(self, msg):
        self.offset= msg.data[0]
        self.is_line=msg.data[1]


def main(args=None):
        rclpy.init(args=args)
        automated_driving=Automated_driving()

        rclpy.spin(automated_driving)

        automated_driving.destroy_node()

        rclpy.shutdown()

if __name__=='__main__':
    main()


