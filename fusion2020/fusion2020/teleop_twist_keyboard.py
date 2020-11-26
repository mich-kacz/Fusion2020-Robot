import sys
import socket

import geometry_msgs.msg
import rclpy

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty
print("\tw\na\ts\td\t\n+/- zwiększa prędkość")
Server_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
Server_socket.bind(('192.168.50.240', 5008))

moveBindings = {
    'w': (1, 0, 1, 0),
    'a': (0, 0, 1, 1),
    'd': (0, 0, 1, -1),
    'k': (0, 0, 1, 0),
    's': (-1, 0, 1, 0),
}

speedBindings = {
    '+': (1, 0),
    '-': (-1, 0),
    ##'e': (0, 1, 0),
    ##'c': (0, -1, 0),
    ##'r': (0, 0, 1),
    ##'v': (0, 0, -1),
}


def getKey(settings):
    if sys.platform == 'win32':
        # getwch() returns a string on Windows
        key = msvcrt.getwch()
    else:
        tty.setraw(sys.stdin.fileno())
        # sys.stdin.read() returns a string on Linux
        key, addr=Server_socket.recvfrom(2**16)
        key=key.decode()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def saveTerminalSettings():
    if sys.platform == 'win32':
        return None
    return termios.tcgetattr(sys.stdin)


def restoreTerminalSettings(old_settings):
    if sys.platform == 'win32':
        return
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def vels(speed, control_vel):
    return 'aktualnie:\tpredkosc liniowa: %s\tbieg:  %s' % (speed, control_vel)


def main():
    settings = saveTerminalSettings()

    rclpy.init()

    node = rclpy.create_node('teleop_twist_keyboard')
    pub = node.create_publisher(geometry_msgs.msg.Twist, 'cmd_vel', 10)

    speed = 1.0
    control_vel = 1.0
    x = 0.0
    z = 1.0
    th = 0.0
    status = 0.0

    try:
        print(vels(speed, control_vel))
        while True:
            key = getKey(settings)
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                z = moveBindings[key][2]
                th = moveBindings[key][3]
            elif key in speedBindings.keys():
                speed = speed + speedBindings[key][0]
                if(speed > 9.0):
                    if(control_vel==2.0): #Tu zmiana na 2 bo jest blad gdzies
                        control_vel = 2.0
                        speed = 1.0
                    else:
                        speed=9.0
                if(speed < 1.0):
                    if(control_vel==1.0):
                        speed = 1.0
                    else:
                        speed=9.0
                        control_vel=1.0
                print(vels(speed, control_vel))
                status = (status + 1) % 15
            else:
                if (key == 'q'):
                    sys.exit(0)
                else:
                    continue
               
            twist = geometry_msgs.msg.Twist()
            twist.linear.x = x * speed
            twist.linear.z = z * control_vel 
            twist.angular.z = th * speed
            pub.publish(twist)


    finally:
        twist = geometry_msgs.msg.Twist()
        twist.linear.x = 0.0
        twist.linear.z = 0.0
        twist.angular.z = 0.0

        restoreTerminalSettings(settings)


if __name__ == '__main__':
    main()
