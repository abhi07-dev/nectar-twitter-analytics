import time
import os

from nectar import ec2_conn

volumes = {
    'webservers': [
        {
            'instance_id': 'ami-00003837',
            'key_name': 'g55cloud',
            'instance_type': 'm2.small',
            # 'placement': 'melbourne-qh2',
            'security_groups': ['ssh', 'ftp', 'open', 'http', 'front-end']
        }
    ],
    'couchdbs': [
        {
            'instance_id': 'ami-00003837',
            'key_name': 'g55cloud',
            'instance_type': 'm2.small',
            # 'placement': 'melbourne-qh2',
            'security_groups': ['ssh', 'ftp', 'open']
        }
    ]
}

script_dir = os.path.dirname(__file__)

# Update Ansible hosts file
rel_path = "../ansible/inventory/inventory.ini"
abs_file_path = os.path.join(script_dir, rel_path)
file = open(abs_file_path, 'w+')
abs_key_path = '~/Documents/nectar-twitter-analytics/key/'

for role, instances in volumes.items():
    file.write('[' + role + ']\n')
    print('Creating instances with role: ' + role)
    i = 1
    for instance_data in instances:
        print('Instance #' + str(i) + ' is being created')
        # Create instance command
        reservation = ec2_conn.run_instances(instance_data['instance_id'],
                                             key_name=instance_data['key_name'],
                                             instance_type=instance_data['instance_type'],
                                             # placement=instance_data['placement'],
                                             security_groups=instance_data['security_groups'])
        instance = reservation.instances[0]
        # Check if the instance is ready to do further actions
        while instance.update() != 'running':
            print('Instance state: ' + instance.state)
            time.sleep(5)
        print('Instance successfully created.')
        print("Instance id: " + instance.id)
        print("Instance place: " + instance.placement)
        print("Instance ip: " + instance.private_ip_address)


        # Create volume if necessary
        if 'volume_size' in instance_data:
            print('Creating volume for instance ' + instance.id)
            vol_req = ec2_conn.create_volume(instance_data['volume_size'], instance.placement)
            print("Volume id: " + vol_req.id)

            curr_vol = ec2_conn.get_all_volumes([vol_req.id])[0]
            while curr_vol.status != 'available':
                print('Volume status: ' + curr_vol.status)
                time.sleep(5)
                curr_vol = ec2_conn.get_all_volumes([vol_req.id])[0]
            print('Volume status: ' + curr_vol.status)

            try:
                ec2_conn.attach_volume(vol_req.id, instance.id, '/dev/vdc')
                print(vol_req.id + ' is attached to instance ' + instance.id)
            except Exception as e:
                print('Volume can not be attached to instance: ' + e)
                print('Now deleting all crated instances and volumes.')
                ec2_conn.terminate_instances([instance.id])
                ec2_conn.delete_volume(vol_req.id)
        file.write(str(instance.private_ip_address) + ' ansible_ssh_private_key_file=' +
                   abs_key_path + instance_data['key_name'] + '.key' + '\n')
        i += 1
        print
    file.write('\n')
file.close()
print("All instances are successfully created and ansible hosts file is updated. Yaaay!!!")

'''
volume snapshot code
snapshot = ec2_conn.create_snapshot(vol_req.id,	'Snapshot1')
new_vol	= snapshot.create_volume('melbourne-qh2')
ec2_conn.delete_snapshot(snapshot.id)
'''
