import os

import boto3
import paramiko


def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    instance_id = os.environ.get('INSTANCE_ID')
    instance = ec2.Instance(instance_id)

    instance.start()
    instance.wait_until_running()
    hostname = instance.public_ip_address

    s3 = boto3.resource('s3')
    bucket_name = os.environ.get('S3_BUCKET')
    s3_path = os.environ('EC2_SSH_KEY_S3_PATH')
    pkey_path = '/tmp/pkey.pem'
    s3.Object(bucket_name, s3_path).download_file(pkey_path)
    pkey = paramiko.RSAKey.from_private_key_file(pkey_path)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=hostname, username='ubuntu', pkey=pkey)

        app_dir = '/home/ubuntu/src/netkeiba'
        command = f'. {app_dir}/.env; nohup {app_dir}/.venv-3.6.7/bin/python {app_dir}/manage.py pipeline --shutdown &'

        client.exec_command(command)
    except Exception as e:
        print(e)
    finally:
        client.close()
