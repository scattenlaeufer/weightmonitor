#!/usr/bin/python3

import argparse, json, os, datetime
from matplotlib import pyplot as pyplot
from matplotlib import dates as dates

parser = argparse.ArgumentParser(description='A program to monitor my weight and nicly plot it.')
parser.add_argument('-a','--analyze-only',action='store_true',default=False,help='Only analyze existing data without adding new datapoints.')
parser.add_argument('-w','--weight',metavar='WEIGHT',type=float,default=None,help='the weight to be loged. If WEIGHT == 0, the existing data will only be analyzed.')
parser.add_argument('-b','--blood-pressure',metavar='BLOODPRESSURE',type=int,nargs=2,default=None,help='Blood pressure with SYS beeing systolic and DIAS being diastolic blood pressure')
parser.add_argument('-d','--date',metavar='DATE',type=str,default=None,help='Specify the date. If none, the current date will be used. Format: YYYY-MM-DD-hhmm')
parser.add_argument('-t','--testing',action='store_true',default=False,help='Only use dummy data.')

args = parser.parse_args()
print(args)

data_path = os.path.split(os.path.abspath(__file__))[0]

if args.testing:
	data_file = os.path.join(data_path,'data_test')
else:
	data_file = os.path.join(data_path,'data')

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

data_point = {'date':date_value}

if args.weight:
	data_point['weight'] = args.weight
if args.blood_pressure:
	data_point['blood_pressure'] = args.blood_pressure
if (args.weight or args.blood_pressure) and not args.analyze_only:
	data.append(data_point)

json_out = json.dumps(data,sort_keys=False,indent=2)

if args.testing:
	print(json_out)

with open(data_file,'w') as out_file:
	out_file.write(json_out)

weight_time_list = []
weight_list = []

bp_time_list = []
bp_sys_list = []
bp_dias_list = []

for data_point in data:
	if 'weight' in data_point.keys() and data_point['weight']:
		weight_time_list.append(datetime.datetime.fromtimestamp(data_point['date']))
		weight_list.append(data_point['weight'])
	if 'blood_pressure' in data_point.keys() and data_point['blood_pressure']:
		bp_time_list.append(datetime.datetime.fromtimestamp(data_point['date']))
		bp_sys_list.append(data_point['blood_pressure'][0])
		bp_dias_list.append(data_point['blood_pressure'][1])

#date_list = [datetime.datetime.fromtimestamp(ts) for ts in weight_time_list]

#print(weight_time_list)
#print(weight_list)
#print(bp_time_list)
#print(bp_sys_list)
#print(bp_dias_list)

fig, ax = pyplot.subplots()

ax.xaxis.set_major_locator(dates.AutoDateLocator())
ax.xaxis.set_major_formatter(dates.AutoDateFormatter(ax.xaxis.get_major_locator()))
ax.set_ylabel('Gewicht (kg)')

ax.plot(dates.date2num(weight_time_list),weight_list)
#ax.grid(True)

ax2 = ax.twinx()
#ax2.grid(True)
ax2.set_ylabel('Blutdruck (mmHg)')

ax2.plot(dates.date2num(bp_time_list),bp_sys_list,'r')
ax2.plot(dates.date2num(bp_time_list),bp_dias_list,'g')

fig.autofmt_xdate()

pyplot.show()
