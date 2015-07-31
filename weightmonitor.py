#!/usr/bin/python3

import argparse, json, os, datetime

parser = argparse.ArgumentParser(description='A program to monitor my weight and nicly plot it.')
parser.add_argument('weight',metavar='WEIGHT',type=float,help='the weight to be loged.')
parser.add_argument('-d','--date',metavar='DATE',type=str,default=None,help='Specify the date. If none, the current date will be used. Format: YYYY-MM-DD-hhmm')

args = parser.parse_args()

print(args)

data_path = os.path.split(os.path.abspath(__file__))[0]

data_file = os.path.join(data_path,'data_test')
data_file = os.path.join(data_path,'data')
print(data_file)

if os.path.isfile(data_file):
	with open(data_file,'r') as in_file:
		json_in = in_file.read()
	data = json.loads(json_in)
else:
	data = []

if args.date:
	raw_date = args.date.split('-')
	raw_time = raw_date[-1].split(':')
	if len(raw_date) != 4:
		print('Error: wrong date format! It must be YYYY-MM-DD-hh:mm')
		exit()
	date = datetime.datetime(int(raw_date[0]),int(raw_date[1]),int(raw_date[2]),int(raw_time[0]),int(raw_time[1]))
else:
	date = datetime.datetime.now()

date_value = int(date.strftime('%s'))

data_point = {'date':date_value,'weight':args.weight}
data.append(data_point)

json_out = json.dumps(data,sort_keys=False,indent=2)

with open(data_file,'w') as out_file:
	out_file.write(json_out)
