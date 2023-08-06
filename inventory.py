#!/usr/bin/env python

import boto3
import json

def get_aws_ec2_inventory():
    ec2 = boto3.client('ec2', region_name='your_aws_region')

    response = ec2.describe_instances()
    instances = response['Reservations']

    inventory = {'_meta': {'hostvars': {}}}

    for instance in instances:
        for i in instance['Instances']:
            instance_id = i['InstanceId']
            private_ip = i['PrivateIpAddress']
            public_ip = i.get('PublicIpAddress', None)
            instance_tags = {tag['Key']: tag['Value'] for tag in i.get('Tags', [])}

            # Define your own host/group naming logic here
            hostname = instance_tags.get('Name', instance_id)

            inventory.setdefault('aws_instances', []).append(hostname)
            inventory['_meta']['hostvars'][hostname] = {
                'ansible_host': private_ip,
                'public_ip': public_ip
            }

    return inventory

if __name__ == '__main__':
    inventory = get_aws_ec2_inventory()
    print(json.dumps(inventory, indent=2))
