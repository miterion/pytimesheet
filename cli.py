import argparse
from configparser import ConfigParser
from datetime import date
import calendar
from collections import OrderedDict

import storage, generate


def print_hours(args):
    hours = storage.readdata(args.job, str(args.month))
    if hours is None:
        print('There are no hours recorded for this month')
        return
    workmonth = date(date.today().year, args.month, 1)
    print('Worked hours in {}, {}'.format(workmonth.strftime('%B'), workmonth.year))
    print('Day\tStart\tEnd\tDuration')
    for hour in hours:
        value = ''
        for key, values in hour.items():
            value += values + '\t'
        print(value)

def generate_pdf(args):
    days = storage.readdata(args.job, str(args.month))
    workmonth = date(date.today().year, args.month, 1)
    if days is None:
        print('No hours worked for {} in {}, {}'.format(args.job, workmonth.strftime('%B'), workmonth.year))
        return
    weekday ,endday = calendar.monthrange(workmonth.year, workmonth.day)
    period = {'start': workmonth.strftime('%d.%m.%Y'),
            'end': workmonth.strftime('{}.%m.%Y').format(endday)
            }
    for day in days:
        fulldate = date(date.today().year, args.month, int(day['day']))
        day['day'] = fulldate.strftime('%d.%m.%Y')

    generate.pdf(args.job, period, days)
     


def add_hours(args):
    storage.writedata(args.job, 
            args.month, 
            {'day': args.day,
                'start': str(args.hours[0]) + ':00',
                'end' : str(args.hours[1]) + ':00'
                })



def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    conffile = ConfigParser()
    conffile.read('config.ini')
    config = conffile['Default']

    #Parent parser for job/month selection
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('job', help='Job',
            choices=(config['jobs'].strip(',').split(',')))
    parent_parser.add_argument('--month', '-m', 
            type = int, 
            help='Restrict to specific month (Default current Month)', 
            default = date.today().month)

    #Print Command
    parser_print = subparsers.add_parser('print', help='Print hours for a job', parents=[parent_parser])
    parser_print.set_defaults(func=print_hours)

    #Generate PDF
    parser_pdf = subparsers.add_parser('pdf', help='Generate PDF', parents=[parent_parser])
    parser_pdf.set_defaults(func=generate_pdf)
    
    #Add hours
    parse_hour = subparsers.add_parser('add', help='Add working hours, format (1-24) (1-24)', parents=[parent_parser])
    parse_hour.add_argument('hours', help='Start and end hour in 24h format', nargs=2, type=int)
    parse_hour.add_argument('--day', '-d', help='Specify a different day from today', type=int, default = date.today().day)
    parse_hour.set_defaults(func=add_hours)
    
    #Delete hours
    #TODO

    #Start working
    #TODO


    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
