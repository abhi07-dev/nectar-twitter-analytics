import sys
from nectar import ec2_conn

ec2_conn.delete_volume(sys.argv[1])
