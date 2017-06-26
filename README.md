# timetrack
Timetracking for hiwis at TU Darmstadt

## Install
Run `python setup.py` as root or with the `--user` flag.

It will install and generate a config file in `$HOME/.config/timetrack` for you to edit.

## Usage
```
usage: timetrack [-h] {print,pdf,add,delete,generate} ...

positional arguments:
  {print,pdf,add,delete,generate}
    print               Print hours for a job
    pdf                 Generate PDF
    add                 Add working hours, format (1-24) (1-24)
    delete              Remove worked hours from schedule
    generate            Generates random hours for a certain month

optional arguments:
  -h, --help            show this help message and exit
```
