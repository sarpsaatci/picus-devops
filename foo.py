import sys
import os
import boto3
import time

# import argparse

# parser = argparse.ArgumentParser(description='PICUS DevOps Challenge')

# parser.add_argument('customerId', metavar='cid', type=string, nargs='+', help='customer id for aws')
# parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')

params = sys.argv
pubKey = os.getenv('PICUS_PUBKEY', "pubkey not assigned")
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

# customers = [{'customerId': "a11f4af4b693", "instances": []}]

for c in customers:
    print(c['customerId'])
    print(c['instances'])

def create(customerId):
    if params[4] == "--node-type" and params[5] == "Manager":
        instance = ec2.create_instances(
            ImageId='ami-4ae27e22',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.medium',
            BlockDeviceMappings=[{
                'DeviceName': '/dev/xvdb',
                'Ebs':{
                    'VolumeSize': 20
                }
            }])
    elif params[4] == "--node-type" and params[5] == "Peer":
        instance = ec2.create_instances(
            ImageId='ami-4ae27e22',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            BlockDeviceMappings=[{
                'DeviceName': '/dev/xvdb',
                'Ebs':{
                    'VolumeSize': 10
                }
            }])
    print instance[0].id

def listNodes(customerId):
    for i in ec2.instances.all():
        if i.state['Name'] != 'terminated' and i.public_ip_address is not None:
            print(i.id + '\t' + i.state['Name'] + '\t' + i.public_ip_address)

def createSnap(instanceId):
    for i in ec2.instances.all():
        if i.id == instanceId:
            snapshot = ec2.create_snapshot(
                VolumeId=i.block_device_mappings[0]['Ebs']['VolumeId'],
                Description='Trial snapshot'
            )
            snapshot.create_tags(Resources=[snapshot.id], Tags=[{'Key': 'Name', 'Value': 'snapshot-' + i.block_device_mappings[0]['Ebs']['VolumeId']}])
            print(snapshot.id)

def listBackups(instanceId):
    for i in ec2.instances.filter(Filters=[{'Name': 'instance-state-code', 'Values': ['0', '16', '32', '64', '80']}]):
        for s in ec2.snapshots.filter(Filters=[{'Name' : 'volume-id', 'Values' : [i.block_device_mappings[0]['Ebs']['VolumeId']]}]):
            if s.volume_id == i.block_device_mappings[0]['Ebs']['VolumeId']:
                print(s.id + '\t' + s.start_time.strftime("%Y-%m-%d %H:%M:%S"))

def rollBack(snapshotId, instanceId):
    if len(ec2.Instance(instanceId).block_device_mappings) >= 0:
        dev = ec2.Instance(instanceId).block_device_mappings[0]['DeviceName']
    ec2.Instance(instanceId).stop()
    while(ec2.Instance(instanceId).state['Name'] != 'stopped'):
        time.sleep(1)
    ec2.Instance(instanceId).detach_volume(VolumeId=ec2.Instance(instanceId).block_device_mappings[0]['Ebs']['VolumeId'], Device=dev)
    az = ec2.Instance(instanceId).placement['AvailabilityZone']
    volume = ec2.create_volume(SnapshotId=snapshotId, AvailabilityZone=az)
    while(volume.state != 'available'):
        volume.reload()
        time.sleep(1)
    ec2.Instance(instanceId).attach_volume(VolumeId=volume.id, Device=dev)
    ec2.Snapshot(snapshotId).delete()
    ec2.Instance(instanceId).start()
    print(ec2.Instance(instanceId).id)

def listAll():
    for i in ec2.instances.all():
        if i.state['Name'] != 'terminated' and i.public_ip_address is not None:
            print(i.id + '\t' + i.state['Name'] + '\t' + i.public_ip_address)

def executeScript(paramType, paramVal, scriptPath):
    if paramType == "--customer-id":
        print(paramType)
    elif paramType == "--node-type":
        print(paramType)

if len(params) > 3:
    if params[1] == "create" and params[2] == "--customer-id":
        for c in customers:
            if c['customerId'] == params[3]:
                create(params[3])
    elif params[1] == "list-nodes" and params[2] == "--customer-id":
        for c in customers:
            if c['customerId'] == params[3]:
                listNodes(params[3])
    elif params[1] == "backup" and params[2] == "--node-id":
        createSnap(params[3])
    elif params[1] == "list-backups" and params[2] == "--node-id":
        listBackups(params[3])
    elif params[1] == "rollback" and params[2] == "--backup-id":
        rollBack(params[3], params[5])
    elif params[1] == "execute" and (params[2] == "--customer-id" or params[2] == "--node-type") and params[4] == "--script":
        executeScript(params[2], params[3], params[5])
elif params[1] == "list-all":
    listAll()
else:
    print("invalid arguments")
