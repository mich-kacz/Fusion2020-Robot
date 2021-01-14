# -*- coding: utf-8 -*-
import numpy as np
import cv2
import struct
import socket
import _thread
import keyboard
from time import sleep

class Udp_robot_app():
   
    def __init__(self):
        self.MAX_DGRAM = 2**16
        self.Server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def dump_buffer(self, Server_socket):
    
        while True:
            seg, addr = Server_socket.recvfrom(self.MAX_DGRAM)
            print(seg[0])
            if struct.unpack("B", seg[0:1])[0] == 1:
                print('finish emptying buffer')
                break
         
    def img_show(self):
        # Set up socket
        print('Dzialam')
        try:
            self.Server_socket.bind(('192.168.50.63', 5006))
        except:
            print('Server bind failed')
            return
        dat = b''
        self.dump_buffer(self.Server_socket)
        while True:
            seg, addr = self.Server_socket.recvfrom(self.MAX_DGRAM)
            if struct.unpack('B', seg[0:1])[0] > 1:
                dat += seg[1:]
            else:
                dat += seg[1:]
                img = cv2.imdecode(np.fromstring(dat, dtype=np.uint8), 1)
                try:
                    cv2.imshow('frame', img)
                except:
                    print('Popsulo sie')
                if cv2.waitKey(1) & 0xFF == 27:
                    break
                dat = b''
            sleep(0.02)
        # cap.release()
        cv2.destroyAllWindows()
        self.Server_socket.close()
        
    def Control(self):
        flag=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        Client_port=5008
        Raspberry_ip='192.168.50.240'
        while(True):
            # Forward moving
            if keyboard.is_pressed('w') and flag[0] ==0 and flag[3]==0:    
                print('w nacisniete\n')
                flag[0]=1
                data_to_send='w'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))                                      
            # Turn left
            if keyboard.is_pressed('a') and flag[1] ==0 and flag[2]==0:    
                print('a nacisniete\n')
                flag[1]=1
                data_to_send='a'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))   
            # Turn right
            if keyboard.is_pressed('d') and flag[2] ==0 and flag[1]==0:    
                print('d nacisniete\n')
                flag[2]=1
                data_to_send='d'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
             # Backward moving
            if keyboard.is_pressed('s') and flag[3] ==0 and flag[0]==0:    
                print('s nacisniete\n')
                flag[3]=1
                data_to_send='s'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
             # Speed up 
            if keyboard.is_pressed('8') and flag[4] ==0:    
                print('8 nacisniete\n')
                flag[4]=1
                data_to_send='8'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
             # Slow down 
            if keyboard.is_pressed('2') and flag[5] ==0:    
                print('2 nacisniete\n')
                flag[5]=1
                data_to_send='2'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
             # Turning speed down
            if keyboard.is_pressed('4') and flag[6] ==0:    
                print('4 nacisniete\n')
                flag[6]=1
                data_to_send='4'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
             # Turning speed up
            if keyboard.is_pressed('6') and flag[7] ==0:    
                print('6 nacisniete\n')
                flag[7]=1
                data_to_send='6'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
            # Gear up
            if keyboard.is_pressed('+') and flag[8] ==0:    
                print('+ nacisniete\n')
                flag[8]=1
                data_to_send='+'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
            # Gear down
            if keyboard.is_pressed('-') and flag[9] ==0:    
                print('- nacisniete\n')
                flag[9]=1
                data_to_send='-'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
             # Quit 
            if keyboard.is_pressed('esc') and flag[10] ==0:
                flag[10]=1
                print('Terminate Control')
                data_to_send='q'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
                break
            # Driving mode
            if keyboard.is_pressed('m') and flag[11] ==0:
                flag[11]=1
                print('Driving mode')
                data_to_send='m'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
            # Refresh
            if keyboard.is_pressed('r') and flag[12] ==0:
                flag[12]=1
                print('Pc stream')
                data_to_send='001'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,5006))
            # Flask server stream
            if keyboard.is_pressed('t') and flag[13] ==0:
                flag[13]=1
                print('Stream start')
                data_to_send='011'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,5006))
            # Flas server stream stop
            if keyboard.is_pressed('y') and flag[14] ==0:
                flag[14]=1
                print('Stream close')
                data_to_send='010'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,5006))  
            #Close options
            if keyboard.is_pressed('q') and flag[15] ==0:
                flag[15]=1
                print('Stop')
                data_to_send='000'
                data_to_send=data_to_send.encode()
                self.Server_socket.sendto(data_to_send,(Raspberry_ip,5006))                 
                
            
            
            #Forward stop or next button
            if not keyboard.is_pressed('w') and flag[0]==1:               
                if flag[1]==1:
                    flag[0]=0
                    print('Wysylam a')
                    data_to_send='a'
                    data_to_send=data_to_send.encode()
                    self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
                elif flag[2]==1:
                    flag[0]=0
                    print('Wysylam d')
                    data_to_send='d'
                    data_to_send=data_to_send.encode()
                    self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
                else:
                    flag[0]=0
                    print('Wysylam k')
                    data_to_send='k'
                    data_to_send=data_to_send.encode()
                    self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
                
             #Left stop or next button    
            if not keyboard.is_pressed('a') and flag[1]==1:
                if flag[0]==1:
                    flag[1]=0
                    print('Wysylam w')
                    data_to_send='w'
                    data_to_send=data_to_send.encode()
                    self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
                elif flag[3]==1:
                    flag[1]=0
                    print('Wysylam s')
                    data_to_send='s'
                    data_to_send=data_to_send.encode()
                    self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
                else:
                    flag[1]=0
                    print('Wysylam k')
                    data_to_send='k'
                    data_to_send=data_to_send.encode()
                    self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
                    
                    
            #Right stop or next button
            if not keyboard.is_pressed('d') and flag[2]==1:
                if flag[0]==1:
                    flag[2]=0
                    print('Wysylam w')
                    data_to_send='w'
                    data_to_send=data_to_send.encode()
                    self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
                elif flag[3]==1:
                    flag[2]=0
                    print('Wysylam s')
                    data_to_send='s'
                    data_to_send=data_to_send.encode()
                    self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
                else:
                    flag[2]=0
                    print('Wysylam k')
                    data_to_send='k'
                    data_to_send=data_to_send.encode()
                    self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
            #Backward stop or next button
            if not keyboard.is_pressed('s') and flag[3]==1:
                if flag[1]==1:
                    flag[0]=0
                    print('Wysylam a')
                    data_to_send='a'
                    data_to_send=data_to_send.encode()
                    self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
                elif flag[2]==1:
                    flag[0]=0
                    print('Wysylam d')
                    data_to_send='d'
                    data_to_send=data_to_send.encode()
                    self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
                else:
                    flag[3]=0
                    print('Wysylam k')
                    data_to_send='k'
                    data_to_send=data_to_send.encode()
                    self.Server_socket.sendto(data_to_send,(Raspberry_ip,Client_port))
                    

            #Speed up stop
            if not keyboard.is_pressed('8') and flag[4]==1:
                flag[4]=0
            #Slow down
            if not keyboard.is_pressed('2') and flag[5]==1:
                flag[5]=0
             #Turning speed down
            if not keyboard.is_pressed('4') and flag[6]==1:
                flag[6]=0
            #Turning speed up
            if not keyboard.is_pressed('6') and flag[7]==1:
                flag[7]=0
            #Gear up
            if not keyboard.is_pressed('+') and flag[8]==1:
                flag[8]=0
            #Gear down
            if not keyboard.is_pressed('-') and flag[9]==1:
                flag[9]=0
            #Quit
            if not keyboard.is_pressed('esc') and flag[10]==1:
                flag[10]=0
            #Driving mode
            if not keyboard.is_pressed('m') and flag[11]==1:
                flag[11]=0
            #Refresh
            if not keyboard.is_pressed('r') and flag[12]==1:
                flag[12]=0
            #Flask server start
            if not keyboard.is_pressed('t') and flag[13]==1:
                flag[13]=0
            #Flask server stop
            if not keyboard.is_pressed('y') and flag[14]==1:
                flag[14]=0
            #Close options
            if not keyboard.is_pressed('q') and flag[15]==1:
                flag[15]=0
            
            sleep(0.1)
    
def main():
    app=Udp_robot_app()
    try:
        _thread.start_new_thread( app.img_show, ())
        _thread.start_new_thread( app.Control, () )
    except:
            print ("Error: unable to start thread")
    
if __name__ == '__main__': 
    main()    