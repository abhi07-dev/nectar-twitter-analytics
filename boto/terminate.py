import sys
from nectar import ec2_conn

ec2_conn.terminate_instances([sys.argv[1]])