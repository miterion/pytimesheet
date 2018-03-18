import argparse
from datetime import date
import calendar
from datetime import timedelta
from sys import argv
from collections import namedtuple
import random

from pytimesheet.utils import get_config
from pytimesheet import storage, generate


def print_hours(args):
    days, workmonth = get_hours_or_die(args.job, args.month)
    if days is None:
        return
    print(
        'Worked hours in {}, {}'.format(
            workmonth.strftime('%B'),
            workmonth.year))
    print('Day\tStart\tEnd\tDuration')
    total_duration = timedelta()
    for day in days:
        total_duration = total_duration + \
            timedelta(hours=int(day['hours'].split(':')[0]))
        value = ''
        for key, values in day.items():
            value += values + '\t'
        print(value)
    print('Total worked hours: {}'.format(
        total_duration.total_seconds() / 60**2))


def generate_pdf(args):
    days, workmonth = get_hours_or_die(args.job, args.month)
    if days is None:
        return
    weekday, endday = calendar.monthrange(workmonth.year, workmonth.day)
    period = {'start': workmonth.strftime('%d.%m.%Y'),
              'end': workmonth.strftime('{}.%m.%Y').format(endday)
              }
    for day in days:
        fulldate = date(date.today().year, args.month, int(day['day']))
        day['day'] = fulldate.strftime('%d.%m.%Y')

    generate.pdf(args.job, args.month, period, days)


def add_hours(args):
    storage.writedata(args.job,
                      args.month,
                      {'day': args.day,
                       'start': str(args.hours[0]) + ':00',
                       'end': str(args.hours[1]) + ':00'
                       })


def delete_hours(args):
    days, workmonth = get_hours_or_die(args.job, args.month)
    if days is None:
        return
    print(
        'Worked hours in {}, {}'.format(
            workmonth.strftime('%B'),
            workmonth.year))
    print('Number\tDay\tStart\tEnd\tDuration')
    counter = 1
    for day in days:
        value = '{}\t'.format(counter)
        for key, values in day.items():
            value += values + '\t'
        print(value)
        counter += 1
    print('\nWhich one should be deleted (Use , as a seperator)')
    selection = input()
    newdays = [
        days[i] for i in range(
            len(days) -
            1) if i +
        1 not in map(
            int,
            selection.split(','))]
    storage.writerawdata(args.job, args.month, newdays)


def get_hours_or_die(job, month):
    days = storage.readdata(job, str(month))
    workmonth = date(date.today().year, month, 1)
    if days is None:
        print('No hours worked for {} in {}, {}'.format(
            job, workmonth.strftime('%B'), workmonth.year))
    return days, workmonth


def generate_hours(args):
    days, workmonth = get_hours_or_die(args.job, args.month)
    if days is None:
        total_duration = timedelta(hours=0)
        free_days = [
            x for x in calendar.Calendar().itermonthdays2(
                workmonth.year, workmonth.month)]
    else:
        worked_hours = map(
            lambda day: timedelta(
                hours=int(
                    day['hours'].split(':')[0])),
            days)
        total_duration = sum(worked_hours, timedelta())
        if total_duration.seconds * 3600 >= int(args.conf[args.job]['hours']):
            print('You worked enough already')
            return
        free_days = [
            x for x in calendar.Calendar().itermonthdays2(
                workmonth.year,
                workmonth.month) if x[0] not in map(
                lambda x: int(
                    x['day']),
                days)]
    needed_hours = int(args.conf[args.job]['hours']) - \
        total_duration / timedelta(hours=1)
    # remove weekends from day list
    free_days = filter(lambda x: x[1] not in (5, 6) and x[0] != 0, free_days)
    # remove weekday from tuple
    free_days = [x for x,_ in free_days]
    jobtuple = namedtuple('jobtuple', ['job', 'month', 'day', 'hours'])
    jobtuple.job = args.job
    jobtuple.month = args.month
    # calculate the already worked days based on average working hours
    needed_days = max(round(needed_hours / 4) + random.randrange(1,5), len(free_days))
    # first generate the working hours, max 4h, min 1h
    working_hours = [min(max(round(random.gauss(4, 0.5)), 1),4) for _ in range(needed_days)]
    # now generate the start time
    start_times = [min(max(round(random.gauss(14, 3)), 7), 18) for _ in range(needed_days)]
    # check whether there are enough or too much hours generated
    overdraft = round(needed_hours) - sum(working_hours)
    if overdraft != 0:
        if overdraft < 0:
            # too much hours, need to reduce
            too_much = True
        elif overdraft > 0:
            # need more hours
            too_much = False
##        for i in sorted(working_hours, reverse=too_much):
#            index = working_hours.index(i) 
#            if too_much:
#                working_hours[index] -= 1
#            else:
#                working_hours[index] += 1
        while overdraft != 0:
            index = random.randrange(len(working_hours))
            if too_much and working_hours[index] > 0:
                working_hours[index] -= 1
                overdraft += 1
            elif not too_much and working_hours[index] < 5:
                working_hours[index] += 1
                overdraft -= 1
    # get work days
    work_days = random.sample(list(free_days), needed_days)
    # match the start hours with the worked hours and add to storage
    for i, day in enumerate(work_days):
        jobtuple.day = day
        jobtuple.hours = [start_times[i], start_times[i] + working_hours[i]]
        add_hours(jobtuple)
    print('Hours generated')
    print_hours(args)



def is_standard_or_only_job(config):
    jobs = config.sections()[1:]
    if 'default_job' in config['Default']:
        return jobs, config['Default']['default_job']
    if len(jobs) == 1:
        return jobs, jobs[0]
    return jobs, jobs


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    conffile = get_config()

    jobs, default = is_standard_or_only_job(conffile)

    # Parent parser for job/month selection
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('job',
                               help='Job',
                               choices=jobs,
                               default=default,
                               nargs='?')
    parent_parser.add_argument(
        '--month',
        '-m',
        type=int,
        help='Restrict to specific month (Default current Month)',
        default=date.today().month)

    # Print Command
    parser_print = subparsers.add_parser(
        'print',
        help='Print hours for a job',
        parents=[parent_parser])
    parser_print.set_defaults(func=print_hours)

    # Generate PDF
    parser_pdf = subparsers.add_parser(
        'pdf', help='Generate PDF', parents=[parent_parser])
    parser_pdf.set_defaults(func=generate_pdf)

    # Add hours
    parser_add = subparsers.add_parser(
        'add',
        help='Add working hours, format (1-24) (1-24)',
        parents=[parent_parser])
    parser_add.add_argument(
        'hours',
        help='Start and end hour in 24h format',
        nargs=2,
        type=int)
    parser_add.add_argument(
        '--day',
        '-d',
        help='Specify a different day from today',
        type=int,
        default=date.today().day)
    parser_add.set_defaults(func=add_hours)

    # Delete hours
    parser_delete = subparsers.add_parser(
        'delete',
        help='Remove worked hours from schedule',
        parents=[parent_parser])
    parser_delete.set_defaults(func=delete_hours)

    # Generate hours
    parser_generate = subparsers.add_parser(
        'generate',
        help='Generates random hours for a certain month',
        parents=[parent_parser])
    parser_generate.set_defaults(func=generate_hours, conf=conffile)

    if len(argv) == 1:
        parser.print_help()
        return
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
