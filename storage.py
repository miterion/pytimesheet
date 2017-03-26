import csv
from pathlib import Path
from datetime import datetime

JOBSPATH = "job"

def newjob(job):
    folder = Path(JOBSPATH).joinpath(job)
    folder.mkdir(exist_ok=True)

def newmonth(job, month):
    folder = Path(JOBSPATH).joinpath(job, str(month))
    folder.mkdir(exist_ok=True)

def writedata(job, month, data):
    hours = datetime.strptime(data['end'], '%H:%M') - datetime.strptime(data['start'], '%H:%M')
    newmonth(job, month)
    with Path(JOBSPATH).joinpath(job, str(month), str(month)  + '.csv').open('a') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow([data['day'], data['start'], data['end'], hours])

def readdata(job, month, ordered=True):
    path = Path(JOBSPATH).joinpath(job, str(month), str(month)  + '.csv') 
    if not path.exists():
        return None
    with Path(JOBSPATH).joinpath(job, str(month) + '.csv').open() as f:
        fieldnames = ['day', 'start', 'end', 'hours']
        workdays = list(csv.DictReader(f, fieldnames))
        if ordered:
            return sorted(workdays, key=lambda entry: int(entry['day'])) 
        return workdays
