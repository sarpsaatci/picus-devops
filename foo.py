import sys
import os
import boto3

# import argparse

# parser = argparse.ArgumentParser(description='PICUS DevOps Challenge')

# parser.add_argument('customerId', metavar='cid', type=string, nargs='+', help='customer id for aws')
# parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')

params = sys.argv
pubKey = os.getenv('PICUS_PUBKEY', "pubkey not assigned")
ec2 = boto3.resource('ec2')

def create(customerId):
    print(customerId)
    if params[4] == "--node-type" and params[5] == "Manager":
        instance = ec2.create_instances(
            ImageId='ami-1e299d7e',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro')
    else if params[4] == "--node-type" and params[5] == "Peer":
        instance = ec2.create_instances(
            ImageId='ami-1e299d7e',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro')
    print instance[0].id
    # print(os.environ)

def listNodes(customerId):
    print(customerId)
    for instance in ec2.instances.all():
        print instance.id, instance.state

def listAll():
    print("all")

if len(params) > 3:
    if params[1] == "create" and params[2] == "--customer-id":
        create(params[3])
    else if params[1] == "list-nodes" and params[2] == "--customer-id":
        listNodes(params[3])
    else if params[1] == "list-all":
        listAll()
else:
    print("invalid arguments")
