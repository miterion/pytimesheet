import csv
from pathlib import Path
from datetime import datetime
from os.path import exists
from os import makedirs

from pytimesheet.utils import get_config_path
JOBSPATH = Path(get_config_path()).joinpath('job')


def newjobfolder():
    if not exists(JOBSPATH):
        makedirs(JOBSPATH, exist_ok=True)


def newjob(job):
    folder = Path(JOBSPATH).joinpath(job)
    folder.mkdir(exist_ok=True)


def newmonth(job, month):
    newjobfolder()
    newjob(job)
    folder = Path(JOBSPATH).joinpath(job, str(month))
    folder.mkdir(exist_ok=True)


def writedata(job, month, data):
    hours = datetime.strptime(
        data['end'], '%H:%M') - datetime.strptime(data['start'], '%H:%M')
    newmonth(job, month)
    with Path(JOBSPATH).joinpath(job, str(month), str(month) + '.csv').open('a') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow([data['day'], data['start'], data['end'], hours])


def writerawdata(job, month, rawdata):
    newmonth(job, month)
    with Path(JOBSPATH).joinpath(job, str(month), str(month) + '.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=['day', 'start', 'end', 'hours'])
        writer.writerows(rawdata)


def readdata(job, month, ordered=True):
    path = Path(JOBSPATH).joinpath(job, str(month), str(month) + '.csv')
    if not path.exists():
        return None
    with path.open() as f:
        fieldnames = ['day', 'start', 'end', 'hours']
        workdays = list(csv.DictReader(f, fieldnames))
        if ordered:
            return sorted(workdays, key=lambda entry: int(entry['day']))
        return workdays
