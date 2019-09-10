from nectar import ec2_conn

reservations = ec2_conn.get_all_reservations()


for i in range(len(reservations)):
	for j in range(len(reservations[i].instances)):
		print('\nID: {}\tIP: {}\tPlacement: {}'.format(reservations[i].id,
 reservations[i].instances[j].private_ip_address,
 reservations[i].instances[j].placement))
 
 
curr_vols = ec2_conn.get_all_volumes()
for i in range(len(curr_vols)):
	print('Volume	status:	{},	volume	AZ:	{}'.format(curr_vols[i].status,	
curr_vols[i].zone))