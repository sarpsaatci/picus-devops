import sys
import argparse

parser = argparse.ArgumentParser(description='PICUS DevOps Challenge')

parser.add_argument('customerId', metavar='cid', type=int, nargs='+', help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const', const=sum, default=max, help='sum the integers (default: find the max)')

params = sys.argv

print(params)
