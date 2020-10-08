import socket
from threading import Thread
import struct
import re
import time
from enum import Enum
time_num =1598419990910

U_ID = b'UAV_3'
client_send_datalist = (b'pose_posin',b'pose_orien',b'set_positn',b'set_orietn',
						b'vel_angula',b'vel_linear',b'set_angula',b'set_linear')
client_send_requflaglist = (b'REQU_ALUAV',b'REQU_UAV_1',b'REQU_UAV_2',b'RE_QUUAV_3',b'REQU_UAV_4',
							b'REQU_UAV_5',b'REQU_UAV_6',b'RE_QUUAV_7',b'REQU_UAV_8',b'REQU_UAV_9',
							b'REQU_UAV_a',b'REQU_UAV_b',b'RE_QUUAV_c',b'REQU_UAV_d',b'REQU_UAV_e')
client_send1_fill = b'MSGTYPEFIL'
client_send2_fill = b'REQURE_FIL'


client_test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('建立客户端套接字{}',client_test.fd)
host = '202.121.181.221'
port = 2333
client_test.connect((host,port))
print('连接到服务器')




while True:
	time_num = time_num+1
	pose_x = 0.000005678
	pose_y = 0.0000012345
	pose_z = 3.24056
	psoe_fill = 0.0
	orientation_w = -0.3456
	orientation_x = -0.09875
	orientation_y = 1.23456
	orientation_z = 0.012345
	for i in range(5):
		client_send_pose = [U_ID,client_send_datalist[0],client_send2_fill,time_num,pose_x,pose_y,pose_z,psoe_fill]
		client_send_orientation = [U_ID,client_send_datalist[1],client_send2_fill,time_num,orientation_w,orientation_x,orientation_y,orientation_z]
		client_send_posepack = struct.pack('!5s10s10sq4f',*client_send_pose)
#		print('发送包长度：',len(client_send_posepack))
		client_send_orientationpack = struct.pack('!5s10s10sq4f',*client_send_orientation)
		client_test.send(client_send_posepack)
		client_test.send(client_send_orientationpack)
		time.sleep(0.5)
	time.sleep(2)
	client_require_send = [U_ID,client_send_datalist[0],client_send_requflaglist[2],0,0.0,0.0,0.0,0.0]
	print('向服务器请求数据',U_ID,client_send_datalist[0],client_send_requflaglist[2])
	client_require_sendpack = struct.pack('!5s10s10sq4f',*client_require_send)
	client_test.send(client_require_sendpack)
	client_recv_msg = client_test.recv(49)
#	print('长度：',client_recv_msg,len(client_recv_msg))
	U_ID_recv,msg_flag_recv,requ_flag_recv,time_num,f_dataa,f_datab,f_datac,f_datad = struct.unpack('!5s10s10sq4f',client_recv_msg)
	print('Request后，接收到的客户端消息：',U_ID_recv,msg_flag_recv,requ_flag_recv,time_num,f_dataa,f_datab,f_datac,f_datad)
#	f_dataa,f_datab,f_datac,f_datad = struct.unpack('!4f',client_recv_msg)
#	print('接收到的客户端消息：',f_dataa,f_datab,f_datac,f_datad)
	time.sleep(5) 


