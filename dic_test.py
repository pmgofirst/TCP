client_data_all = {'UAV_1': {'pose_posin':[0,0.0,0.0,0.0],'pose_orien':[1,0.0,0.0,0.0],
							'set_positn':[3,0.0,0.0,0.0],'set_orietn':[2,0.0,0.0,0.0],
							'vel_angula':[7,0.0,0.0,0.0],'vel_linear':[5,0.0,0.0,0.0],
							'set_angula':[4,0.0,0.0,0.0],'set_linear':[6,0.0,0.0,0.0],},
				  'UAV_2': {'pose_posin':[0,0.0,0.0,0.0],'pose_orien':[0,0.0,0.0,0.0],
							'set_positn':[0,0.0,0.0,0.0],'set_orietn':[0,0.0,0.0,0.0],
							'vel_angula':[0,0.0,0.0,0.0],'vel_linear':[0,0.0,0.0,0.0],
							'set_angula':[0,0.0,0.0,0.0],'set_linear':[0,0.0,0.0,0.0],},
				  'UAV_3': {'pose_posin':[0,0.0,0.0,0.0],'pose_orien':[0,0.0,0.0,0.0],
							'set_positn':[0,0.0,0.0,0.0],'set_orietn':[0,0.0,0.0,0.0],
							'vel_angula':[0,0.0,0.0,0.0],'vel_linear':[0,0.0,0.0,0.0],
							'set_angula':[0,0.0,0.0,0.0],'set_linear':[0,0.0,0.0,0.0],},
				  'UAV_4': {'pose_posin':[0,0.0,0.0,0.0],'pose_orien':[0,0.0,0.0,0.0],
							'set_positn':[0,0.0,0.0,0.0],'set_orietn':[0,0.0,0.0,0.0],
							'vel_angula':[0,0.0,0.0,0.0],'vel_linear':[0,0.0,0.0,0.0],
							'set_angula':[0,0.0,0.0,0.0],'set_linear':[0,0.0,0.0,0.0],},}
U_ID = (0,'UAV_1')
client_data_all['UAV_1']['pose_posin'][0] = [0.0,0.2]
#client_data_all = []
print(list(enumerate(client_data_all)))
if U_ID in list(enumerate(client_data_all)):
	print('yes',type(client_data_all),len(client_data_all),client_data_all['UAV_1']['pose_posin'][1])
else:
	print('no')