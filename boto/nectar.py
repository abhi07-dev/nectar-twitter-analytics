import boto

accesskey = '8092852be4e7461a8f4a828fe9209a23'
secretkey = 'bf0afa820fae4f40a4cfa4d84a8d77bd'

from boto.ec2.regioninfo import RegionInfo
region = RegionInfo(name='melbourne', endpoint='nova.rc.nectar.org.au')
ec2_conn = boto.connect_ec2(aws_access_key_id=accesskey,
 aws_secret_access_key=secretkey,
 is_secure=True,
 region=region,
 port=8773,
 path='/services/Cloud',
 validate_certs=False) 