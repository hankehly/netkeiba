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
    s3_path = os.environ.get('EC2_SSH_KEY_S3_PATH')
    pkey_path = '/tmp/pkey.pem'
    s3.Object(bucket_name, s3_path).download_file(pkey_path)
    pkey = paramiko.RSAKey.from_private_key_file(pkey_path)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(hostname=hostname, username='ubuntu', pkey=pkey)
        channel = client.get_transport().open_session()
        command = _build_command_string(event.get('shutdown'), event.get('min_date'))
        channel.exec_command(command)
    except Exception as e:
        print(e)
    finally:
        client.close()


def _build_command_string(shutdown=None, min_date=None):
    if shutdown is None:
        shutdown = False

    app_dir = '/home/ubuntu/src/netkeiba'
    env_file = os.path.join(app_dir, '.env')
    python_bin = os.path.join(app_dir, '.venv-3.6.7', 'bin', 'python')
    manage_bin = os.path.join(app_dir, 'manage.py')

    activate_env_command_args = ['.', env_file]
    run_pipeline_command_args = ['nohup', python_bin, manage_bin, 'pipeline']

    if shutdown:
        run_pipeline_command_args.append('--shutdown')

    if min_date:
        run_pipeline_command_args.extend(['--min-date', min_date])

    run_pipeline_command_args.append('&')

    activate_env_command = ' '.join(activate_env_command_args)
    run_pipeline_command = ' '.join(run_pipeline_command_args)

    return '; '.join([activate_env_command, run_pipeline_command])
