import socket
from threading import Thread
import struct
import re
from enum import Enum

client_conn_pool = [] #客户端连接的线程池
main_socket_server = None #负责监听的socket
ADDRESS = ('192.168.1.102',2333)

client_data_all = {'UAV_1': {'pose_posin':[0,0.0,0.0,0.0,0.0],'pose_orien':[0,0.0,0.0,0.0,0.0],
							'set_positn':[0,0.0,0.0,0.0,0.0],'set_orietn':[0,0.0,0.0,0.0,0.0],
							'vel_angula':[0,0.0,0.0,0.0,0.0],'vel_linear':[0,0.0,0.0,0.0,0.0],
							'set_angula':[0,0.0,0.0,0.0,0.0],'set_linear':[0,0.0,0.0,0.0,0.0],},
				   'UAV_2': {'pose_posin':[0,0.0,0.0,0.0,0.0],'pose_orien':[0,0.0,0.0,0.0,0.0],
							'set_positn':[0,0.0,0.0,0.0,0.0],'set_orietn':[0,0.0,0.0,0.0,0.0],
							'vel_angula':[0,0.0,0.0,0.0,0.0],'vel_linear':[0,0.0,0.0,0.0,0.0],
							'set_angula':[0,0.0,0.0,0.0,0.0],'set_linear':[0,0.0,0.0,0.0,0.0],},
				   'UAV_3': {'pose_posin':[0,0.0,0.0,0.0,0.0],'pose_orien':[0,0.0,0.0,0.0,0.0],
							'set_positn':[0,0.0,0.0,0.0,0.0],'set_orietn':[0,0.0,0.0,0.0,0.0],
							'vel_angula':[0,0.0,0.0,0.0,0.0],'vel_linear':[0,0.0,0.0,0.0,0.0],
							'set_angula':[0,0.0,0.0,0.0,0.0],'set_linear':[0,0.0,0.0,0.0,0.0],},
				   'UAV_4': {'pose_posin':[0,0.0,0.0,0.0,0.0],'pose_orien':[0,0.0,0.0,0.0,0.0],
							'set_positn':[0,0.0,0.0,0.0,0.0],'set_orietn':[0,0.0,0.0,0.0,0.0],
							'vel_angula':[0,0.0,0.0,0.0,0.0],'vel_linear':[0,0.0,0.0,0.0,0.0],
							'set_angula':[0,0.0,0.0,0.0,0.0],'set_linear':[0,0.0,0.0,0.0,0.0],},}
new_client_add = {'pose_posin':[0,0.0,0.0,0.0,0.0],'pose_orien':[0,0.0,0.0,0.0,0.0],
				  'set_positn':[0,0.0,0.0,0.0,0.0],'set_orietn':[0,0.0,0.0,0.0,0.0],
				  'vel_angula':[0,0.0,0.0,0.0,0.0],'vel_linear':[0,0.0,0.0,0.0,0.0],
				  'set_angula':[0,0.0,0.0,0.0,0.0],'set_linear':[0,0.0,0.0,0.0,0.0],}
msg_flag_list = ['pose_posin','pose_orien','set_positn','set_orietn','vel_angula','vel_linear','set_angula','set_linear']
client_send_requflaglist = (b'REQU_ALUAV',b'REQU_UAV_1',b'REQU_UAV_2',b'REQU_UAV_3',b'REQU_UAV_4',
							b'REQU_UAV_5',b'REQU_UAV_6',b'REQU_UAV_7',b'REQU_UAV_8',b'REQU_UAV_9',
							b'REQU_UAV_a',b'REQU_UAV_b',b'REQU_UAV_c',b'REQU_UAV_d',b'REQU_UAV_e')

def init():
	global main_socket_server
	main_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	main_socket_server.bind((ADDRESS))
	main_socket_server.listen(5) #最大等待数 不是连接数
	print('服务端已经启动，等待客户端的连接......')

def accept_client():
	while True:
		client,c_addr = main_socket_server.accept() #阻塞，等待客户端连接
		client_conn_pool.append(client)
		thread = Thread(target=message_handle,args=(client,))
		thread.setDaemon(True)
		thread.start()

def message_handle(client):
#	client.sendall('连接服务器`成功'.encode(encoding='utf-8'))
	while True:
		re_bytes = client.recv(49)
		U_ID,msg_flag,requ_flag,time_num,f_dataa,f_datab,f_datac,f_datad = struct.unpack('!5s10s10sq4f',re_bytes)
		print('客户端消息：',U_ID,msg_flag,requ_flag,time_num,f_dataa,f_datab,f_datac,f_datad)
		U_ID_str = str(U_ID,encoding = 'utf-8')
		msg_flag_str = str(msg_flag,encoding = 'utf-8')
		requ_flag_str = str(requ_flag,encoding = 'utf-8')
		data_frame_list = [time_num,f_dataa,f_datab,f_datac,f_datad]
		if U_ID_str in client_data_all.keys():
			if msg_flag_str in client_data_all[U_ID_str].keys() and requ_flag_str == 'REQUFILL':
				client_data_all[U_ID_str][msg_flag_str] = data_frame_list
			elif msg_flag_str in msg_flag_list and requ_flag_str == 'REQURE_FIL':
				client_data_all[U_ID_str][msg_flag_str] = data_frame_list
			elif requ_flag_str == 'REQURE_FIL':
				print('这是一个请求指令')
			elif requ_flag_str not in client_send_requflaglist:
				print('接收的信息类别不在消息定义列表（pose/vel/set）中')
#			print('received',client_data_all)
			if requ_flag_str == 'REQU_ALUAV':
				print('给客户端'+U_ID_str+'发送所有在线客户端的信息')
			elif requ_flag_str[5:] in client_data_all.keys():
				print('all_message',requ_flag_str[5:])
				if msg_flag_str in client_data_all[requ_flag_str[5:]].keys():
					timeof_datalist = client_data_all[requ_flag_str[5:]][msg_flag_str][0]
					frdataof_datalist = client_data_all[requ_flag_str[5:]][msg_flag_str][1]
					sedataof_datalist = client_data_all[requ_flag_str[5:]][msg_flag_str][2]
					thdataof_datalist = client_data_all[requ_flag_str[5:]][msg_flag_str][3]
					fodataof_datalist = client_data_all[requ_flag_str[5:]][msg_flag_str][4]
					requ_flag_bytes = requ_flag_str[5:].encode('utf-8')
#					print('全部消息：',client_data_all)
#					print(requ_flag_bytes,requ_flag_str[5:],msg_flag_str.encode('utf-8'),b'commd_back',timeof_datalist,frdataof_datalist,sedataof_datalist,thdataof_datalist,fodataof_datalist)
					server_send_client = [requ_flag_bytes,msg_flag_str.encode('utf-8'),b'commd_back',timeof_datalist,frdataof_datalist,sedataof_datalist,thdataof_datalist,fodataof_datalist]
					server_send_clientpack = struct.pack('!5s10s10sq4f',requ_flag_bytes,msg_flag_str.encode('utf-8'),b'commd_back',timeof_datalist,frdataof_datalist,sedataof_datalist,thdataof_datalist,fodataof_datalist)
#					print('发送数据长度：',len(server_send_clientpack))
					client.send(server_send_clientpack)
				else:
					print('接受的信息指令类型不在列表中！')
			elif msg_flag_str not in msg_flag_list:
				print('接受到的信息指令目标飞机不在列表中！')
		elif U_ID_str[0:4] == 'UAV_':
			client_data_all[U_ID_str] = new_client_add
			print('added',client_data_all[U_ID_str])
		else:
			print('接受的飞机ID不在列表内，并且不符合U_ID命名标准:UAV_n')
		if len(re_bytes) == 0:  #s设置心跳包判断客户端是否在线
			client.close()
			client_conn_pool.remove(client)
			print('客户端下线了')

if __name__ == '__main__':
	init()
	thread = Thread(target=accept_client)
	thread.setDaemon(True)
	thread.start()
	while True:
		use_cmd = input('')
		if use_cmd =='1':
			print('----当前在线人数：',len(client_conn_pool))
		elif use_cmd =='2':
			exit()
