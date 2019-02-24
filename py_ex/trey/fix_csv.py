#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

# import sys
import csv
from argparse import ArgumentParser

# old_filename = sys.argv[1]
# new_filename = sys.argv[2]

# old_filename, new_filename = sys.argv[1:]

parser = ArgumentParser()
parser.add_argument('old_filename')
parser.add_argument('new_filename')
parser.add_argument('--in-delimiter', dest='delim', default='|')
parser.add_argument('--in-quote', dest='quote', default='"')
args = parser.parse_args()

# old_file = open(old_filename)
# rows = [line.split('|') for line in old_file.read().splitlines()]

# new_file = open(new_filename, mode='wt', newline='\r\n')
# print('\n'.join(','.join(row) for row in rows), file=new_file)

# old_file.close()
# new_file.close()

# with open(old_filename, newline='') as old_file:
#     # reader = csv.reader(old_file, delimiter='|')
#     # rows = [line for line in reader]
#     rows = list(csv.reader(old_file, delimiter='|'))

with open(args.old_filename, newline='') as old_file:
    # quotechar = '"'
    # delimiter = '|'
    # if args.delim:
    #     delimiter = args.delim
    # if args.quote:
    #     quotechar = args.quote
    reader = csv.reader(old_file, delimiter=args.delim,
                        quotechar=args.quote)
    rows = list(reader)

# with open(new_filename, mode='wt', newline='') as new_file:
#     # writer = csv.writer(new_file)
#     # writer.writerows(rows)
#     csv.writer(new_file).writerows(rows)

with open(args.new_filename, mode='wt', newline='') as new_file:
    writer = csv.writer(new_file)
    writer.writerows(rows)
