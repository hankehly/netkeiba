import boto3
import paramiko

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    instance_id = os.environ.get('INSTANCE_ID')
    instance = ec2.Instance(instance_id)

    instance.start()
    instance.wait_until_running()
    instance_ip = instance.public_ip_address

    s3 = boto3.resource('s3')
    bucket_name = os.environ.get('S3_BUCKET')
    s3_path = os.environ('EC2_SSH_KEY_S3_PATH')
    keypair_path = '/tmp/keypair.pem'
    s3.Object(bucket_name, s3_path).download_file(keypair_path)
    key = paramiko.RSAKey.from_private_key_file(keypair_path)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=instance_ip, username='ubuntu', pkey=key)

        cmd = '. /home/ubuntu/src/netkeiba/.env; /home/ubuntu/src/netkeiba/.venv-3.6.7/bin/python /home/ubuntu/src/netkeiba/manage.py pipeline'
        stdin, stdout, stderr = client.exec_command(cmd)
        print(stdout.read())
    except Exception as e:
        print(e)
    finally:
        client.close()

